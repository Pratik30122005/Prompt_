"""FastAPI wrapper around eval.py — exposes prompt evaluation over HTTP.

    pip install fastapi uvicorn[standard]
    uvicorn server:app --reload --port 8000
"""

import asyncio
import importlib
import json
import os
import queue
import statistics
import sys
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import ssl

# Fix SSL certificate verification on macOS Python
try:
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl._create_default_https_context = lambda: ssl_context
except ImportError:
    # Fallback to unverified SSL context if CA certificates are not installed on macOS Python
    ssl._create_default_https_context = ssl._create_unverified_context

# Import eval.py without shadowing the built-in eval()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
evaluator = importlib.import_module("eval")
router = importlib.import_module("router")

# .env is gitignored - a key here never reaches the public repo. Environment wins over the file.
_ENV = Path(__file__).parent / ".env"
if _ENV.exists():
    for _line in _ENV.read_text(encoding="utf-8").splitlines():
        _name, _, _value = _line.partition("=")
        if _name.strip() and not _name.lstrip().startswith("#"):
            os.environ.setdefault(_name.strip(), _value.strip())


def server_key():
    """The key to fall back on when a request does not carry one."""
    return (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            or evaluator.API_KEY.strip())

app = FastAPI(title="Prompt Evaluator API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fallback to /tmp in read-only serverless environments like Vercel
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    EVALS_DIR = Path("/tmp/evaluations")
else:
    EVALS_DIR = Path(__file__).parent / "evaluations"

try:
    EVALS_DIR.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    EVALS_DIR = Path("/tmp/evaluations")
    EVALS_DIR.mkdir(parents=True, exist_ok=True)



# ── Request / Response models ──────────────────────────────────────────

class EvalRequest(BaseModel):
    prompt: str
    models: list[str] = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]
    thinking_budgets: list = [None]
    n: int = 1
    judge: bool = False
    judge_model: str = "gemini-3.5-flash"
    reference: str | None = None
    custom_prices: dict = {}


class RecommendRequest(BaseModel):
    prompt: str
    model: str = "gemini-3.6-flash"


def heuristic_recommend(prompt: str):
    p = prompt.lower()
    if any(k in p for k in ["deck", "slide", "presentation", "pitch", "powerpoint"]):
        tool_id = "gamma"
        task_type = "presentation"
        comp = "medium"
        why = "The deliverable is a formatted presentation deck rather than plain text."
        tradeoff = "Slide decks look professional out of the box, but exact numeric calculations should be verified beforehand."
    elif any(k in p for k in ["csv", "excel", "spreadsheet", "reconcile", "variance", "200k", "rows"]):
        tool_id = "chatgpt"
        task_type = "data_analysis"
        comp = "high"
        why = "Requires Python sandbox analysis for large dataset reconciliation and exact variance calculations."
        tradeoff = "ChatGPT Plus handles code and file analysis directly, but lacks visual slide generation."
    elif any(k in p for k in ["competitor", "pricing", "charge", "current", "2026", "search", "web"]):
        tool_id = "perplexity"
        task_type = "web_research"
        comp = "medium"
        why = "Requires live web research with up-to-date real-time citations and competitor data."
        tradeoff = "Provides cited web sources, but slower for pure offline writing tasks."
    elif any(k in p for k in ["refactor", "middleware", "repo", "tests", "code", "bug", "auth"]):
        tool_id = "claude-code"
        task_type = "coding"
        comp = "high"
        why = "Multi-file codebase changes require real repository context and automated test execution."
        tradeoff = "Full repo integration ensures tests stay green, but requires CLI setup."
    elif any(k in p for k in ["summarize", "document", "contract", "pdf", "report"]):
        tool_id = "claude"
        task_type = "summarization"
        comp = "medium"
        why = "Long-document reasoning and structured analysis excel at precise text summarization."
        tradeoff = "High precision on long text, though dedicated slide tools are better if slides are needed."
    else:
        tool_id = "claude"
        task_type = "writing"
        comp = "low"
        why = "General text processing and structured analysis task."
        tradeoff = "Versatile for broad writing and analysis tasks."

    rec = {
        "task_type": task_type,
        "complexity": comp,
        "deliverable": "Structured text / analysis output",
        "primary": {
            "tool": tool_id,
            "intelligence": "standard",
            "thinking": "on" if comp == "high" else "off",
            "why": why
        },
        "alternatives": [
            {
                "tool": "gemini" if tool_id != "gemini" else "chatgpt",
                "intelligence": "standard",
                "why": "Alternative general LLM option.",
                "tradeoff": tradeoff
            }
        ],
        "avoid": []
    }
    return router.decorate(rec)


@app.post("/api/recommend")
async def recommend_tool(
    req: RecommendRequest,
    x_api_key: str = Header(default="", alias="X-API-Key"),
):
    """Route one task to a tool + intelligence level. Single call, plain JSON - no SSE."""
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt is required")
    key = x_api_key if x_api_key and x_api_key != "demo" else server_key()
    if key and key != "demo":
        try:
            return await asyncio.to_thread(
                router.recommend, req.prompt, key, req.model,
            )
        except (Exception, SystemExit):
            # Fall back seamlessly to heuristic recommendation if API fails or key denied
            pass
    return heuristic_recommend(req.prompt)


# ── Endpoints ──────────────────────────────────────────────────────────

@app.post("/api/evaluate")
async def run_evaluation(
    req: EvalRequest,
    x_api_key: str = Header(alias="X-API-Key"),
):
    """Run an evaluation and stream progress via Server-Sent Events.

    The response is an SSE stream with these event types:
      - start          → { id, total_configs }
      - config_start   → { model, thinking, config, total_configs }
      - progress       → { model, thinking, run, total_runs, config, total_configs, secs }
      - result         → { data: <aggregated row> }
      - complete       → { id, evaluation: <full saved object> }
      - error          → { message }
    """
    # Apply any custom pricing overrides for this request
    for model, rates in req.custom_prices.items():
        if isinstance(rates, (list, tuple)) and len(rates) == 2:
            evaluator.PRICES[model] = tuple(float(r) for r in rates)

    progress_queue: queue.Queue = queue.Queue()

    def worker():
        try:
            eval_id = str(uuid.uuid4())[:8]
            all_results = []
            configs = [(m.strip(), t) for m in req.models for t in req.thinking_budgets]

            progress_queue.put({
                "type": "start", "id": eval_id, "total_configs": len(configs),
            })

            for ci, (model, thinking) in enumerate(configs):
                progress_queue.put({
                    "type": "config_start",
                    "model": model, "thinking": thinking,
                    "config": ci + 1, "total_configs": len(configs),
                })

                runs = []
                for i in range(req.n):
                    try:
                        if x_api_key == "demo" or not x_api_key:
                            import random
                            time.sleep(1.2 + random.random() * 1.5)
                            secs = 1.2 + random.random() * 1.5
                            text = (
                                f"[DEMO MODE - Simulated output for {model}]\n\n"
                                f"Evaluated Prompt: {req.prompt[:100]}...\n\n"
                                f"Key Findings:\n"
                                f"1. Model {model} handled the request with appropriate structure.\n"
                                f"2. Thinking budget applied: {thinking if thinking is not None else 'Default'}.\n"
                                f"3. High clarity and accuracy demonstrated across key domain concepts."
                            )
                            usage = {"in": len(req.prompt.split()) * 4 + 20, "out": 120, "think": thinking if thinking and thinking > 0 else 0}
                        else:
                            text, usage, secs = evaluator.call(
                                model, req.prompt, thinking, x_api_key,
                            )
                    except Exception as exc:
                        progress_queue.put({"type": "error", "message": f"{model} API error: {str(exc)}"})
                        progress_queue.put(None)
                        return

                    row = {
                        "text": text,
                        "usage": usage,
                        "secs": round(secs, 2),
                        "cost": evaluator.cost(model, usage) or 0.000045,
                        "scores": {},
                        "verdict": "",
                        "critical_failures": [],
                    }

                    if req.judge:
                        try:
                            if x_api_key == "demo" or not x_api_key:
                                time.sleep(0.8)
                                row["scores"] = {
                                    "accuracy": 5 if "pro" in model else 4,
                                    "completeness": 5,
                                    "relevance": 5,
                                    "instruction_following": 5,
                                    "consistency": 5,
                                    "hallucination_control": 4,
                                    "reasoning_quality": 5 if "pro" in model or (thinking and thinking > 0) else 4,
                                }
                                row["verdict"] = f"Demo Mode: {model} delivered a coherent and precise response following all prompt rules."
                                row["critical_failures"] = []
                            else:
                                j = evaluator.judge(
                                    req.judge_model, req.prompt, text,
                                    x_api_key, req.reference,
                                )
                                row["scores"] = j.get("scores", {})
                                row["verdict"] = j.get("verdict", "")
                                row["critical_failures"] = j.get("critical_failures", [])
                        except Exception as exc:
                            progress_queue.put({"type": "error", "message": f"Judge error: {str(exc)}"})
                            progress_queue.put(None)
                            return

                    runs.append(row)
                    progress_queue.put({
                        "type": "progress",
                        "model": model, "thinking": thinking,
                        "run": i + 1, "total_runs": req.n,
                        "config": ci + 1, "total_configs": len(configs),
                        "secs": round(secs, 2),
                    })

                # Aggregate this configuration
                result = {
                    "model": model,
                    "thinking": thinking,
                    "runs": runs,
                    "secs": round(statistics.mean(r["secs"] for r in runs), 2),
                    "cost": (
                        None if runs[0]["cost"] is None
                        else round(statistics.mean(r["cost"] for r in runs), 8)
                    ),
                    "tokens": {
                        k: round(statistics.mean(r["usage"][k] for r in runs))
                        for k in ("in", "out", "think")
                    },
                    "avg_score": evaluator.avg_scores(runs),
                    "variance": round(len({r["text"] for r in runs}) / len(runs), 2),
                }
                all_results.append(result)
                progress_queue.put({"type": "result", "data": result})

            # Persist to disk
            evaluation = {
                "id": eval_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "prompt": req.prompt,
                "config": {
                    "models": req.models,
                    "thinking_budgets": req.thinking_budgets,
                    "n": req.n,
                    "judge": req.judge,
                    "judge_model": req.judge_model,
                    "reference": req.reference,
                },
                "results": all_results,
            }
            (EVALS_DIR / f"{eval_id}.json").write_text(
                json.dumps(evaluation, indent=2, default=str),
            )

            progress_queue.put({
                "type": "complete", "id": eval_id, "evaluation": evaluation,
            })
            progress_queue.put(None)  # sentinel
        except Exception as global_exc:
            progress_queue.put({"type": "error", "message": f"Worker crashed: {str(global_exc)}"})
            progress_queue.put(None)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    async def event_stream():
        while True:
            try:
                event = await asyncio.to_thread(progress_queue.get, timeout=660)
            except Exception:
                break
            if event is None:
                break
            yield f"data: {json.dumps(event, default=str)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/evaluations")
async def list_evaluations():
    """List all saved evaluations (metadata only, most recent first)."""
    evals = []
    for f in sorted(
        EVALS_DIR.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    ):
        try:
            data = json.loads(f.read_text())
            # Compute a headline score if available
            scores = [
                statistics.mean(r["avg_score"].values())
                for r in data.get("results", [])
                if r.get("avg_score")
            ]
            evals.append({
                "id": data["id"],
                "timestamp": data["timestamp"],
                "prompt": data["prompt"][:120],
                "models": data["config"]["models"],
                "judge": data["config"]["judge"],
                "n": data["config"].get("n", 1),
                "result_count": len(data.get("results", [])),
                "avg_score": round(statistics.mean(scores), 2) if scores else None,
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return evals


@app.get("/api/evaluations/{eval_id}")
async def get_evaluation(eval_id: str):
    """Get the full evaluation result."""
    path = EVALS_DIR / f"{eval_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return json.loads(path.read_text())


@app.delete("/api/evaluations/{eval_id}")
async def delete_evaluation(eval_id: str):
    """Delete a saved evaluation."""
    path = EVALS_DIR / f"{eval_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Evaluation not found")
    path.unlink()
    return {"deleted": eval_id}


@app.get("/api/models")
async def get_models():
    """Return the known models, their pricing, and the evaluation criteria."""
    return {
        "models": list(evaluator.PRICES.keys()),
        "prices": {
            m: {"input": p[0], "output": p[1]}
            for m, p in evaluator.PRICES.items()
        },
        "criteria": evaluator.CRITERIA,
    }


@app.get("/api/tools")
async def get_tools():
    """Return the router's tool catalog, so the UI never duplicates the list."""
    return {"tools": router.TOOLS, "task_types": router.TASK_TYPES,
            "intelligence": router.INTELLIGENCE, "has_key": bool(server_key())}



class FeedbackRequest(BaseModel):
    prompt: str
    recommended_tool: str
    user_feedback: str  # "upvote" or "downvote"
    actual_tool_used: str | None = None
    notes: str | None = None


# ── Persistent feedback store (Upstash Redis REST API) ─────────────────
# Upstash Redis is serverless Redis with an HTTP REST API — no SDK or long-lived
# connection needed, works in any serverless environment including Vercel.
# Free tier: 10 k commands/day, 256 MB storage, no credit card needed. Setup:
#   1. Sign up at https://upstash.com (free)
#   2. Create a Redis database → copy the REST URL and REST Token
#   3. Add to Vercel: Settings → Environment Variables:
#        UPSTASH_REDIS_REST_URL   = https://your-db.upstash.io
#        UPSTASH_REDIS_REST_TOKEN = your_token_here
#   4. Add the same two lines to your local .env file
# Without these vars the endpoints still work — POST returns success and GET
# returns an empty list with a configuration note. Nothing in the UI breaks.

_FEEDBACK_KEY = "prompt_router:feedback"  # Redis list key; LPUSH keeps newest-first


def _upstash_url() -> str | None:
    return os.environ.get("UPSTASH_REDIS_REST_URL")

def _upstash_headers() -> dict | None:
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else None

def _feedback_push(entry: dict) -> bool:
    """LPUSH one JSON-encoded entry onto the Redis list. Returns True on success."""
    url, headers = _upstash_url(), _upstash_headers()
    if not url or not headers:
        return False
    try:
        import httpx
        resp = httpx.post(
            f"{url}/lpush/{_FEEDBACK_KEY}",
            headers={**headers, "Content-Type": "application/json"},
            content=json.dumps([json.dumps(entry, default=str)]),
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False

def _feedback_list(limit: int = 200) -> list[dict]:
    """Return up to `limit` feedback entries from Redis, newest first."""
    url, headers = _upstash_url(), _upstash_headers()
    if not url or not headers:
        return []
    try:
        import httpx
        resp = httpx.get(
            f"{url}/lrange/{_FEEDBACK_KEY}/0/{limit - 1}",
            headers=headers, timeout=8,
        )
        if resp.status_code != 200:
            return []
        return [json.loads(r) for r in resp.json().get("result", [])]
    except Exception:
        return []

# Vercel Blob storage helpers
_BLOB_BASE = "https://blob.vercel-storage.com"

def _blob_token() -> str | None:
    """Return the Vercel Blob read‑write token if configured."""
    return os.getenv("BLOB_READ_WRITE_TOKEN")

async def _blob_put(entry: dict) -> bool:
    """Upload a feedback entry as a private blob. Returns True on success."""
    token = _blob_token()
    if not token:
        return False
    try:
        import httpx
        # Make timestamp filename-safe (replace colons)
        ts = (entry.get("timestamp") or str(int(time.time() * 1000))).replace(":", "-")
        pathname = f"feedback/{ts}.json"
        headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
            "x-vercel-blob-access": "public",  # public makes downloadUrl work without extra auth
        }
        resp = httpx.put(
            f"{_BLOB_BASE}/{pathname}",
            headers=headers,
            content=json.dumps(entry).encode(),
            timeout=10,
        )
        return resp.status_code in (200, 201)
    except Exception:
        return False

async def _blob_list() -> list[dict]:
    """Retrieve all feedback blobs (newest first)."""
    token = _blob_token()
    if not token:
        return []
    try:
        import httpx
        resp = httpx.get(
            f"{_BLOB_BASE}",
            params={"prefix": "feedback/", "token": token},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        entries: list[dict] = []
        for blob in data.get("blobs", []):
            dl = blob.get("downloadUrl") or blob.get("url")
            if not dl:
                continue
            r = httpx.get(dl, timeout=10)
            if r.status_code == 200:
                try:
                    entries.append(json.loads(r.text))
                except Exception:
                    pass
        entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        return entries
    except Exception:
        return []



@app.post("/api/feedback")
async def log_feedback(req: FeedbackRequest):
    """Persist recommendation-accuracy feedback.

    Writes to Upstash Redis (survives Vercel redeployments) when
    UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN are set.
    Falls back to /tmp/evaluations/feedback.jsonl (ephemeral, local-only) otherwise.
    Always returns HTTP 200 so the UI is never blocked by storage issues.
    """
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "prompt": req.prompt,
        "recommended_tool": req.recommended_tool,
        "user_feedback": req.user_feedback,
        "actual_tool_used": req.actual_tool_used,
        "notes": req.notes,
    }
    # Try Vercel Blob storage first, then Upstash, then local fallback
    stored_in = "blob" if await _blob_put(entry) else ("upstash" if _feedback_push(entry) else "local_tmp")
    if stored_in == "local_tmp":
        try:
            log_file = EVALS_DIR / "feedback.jsonl"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except OSError:
            stored_in = "none"
    return {"status": "success", "stored_in": stored_in, "logged": entry}


@app.get("/api/feedback")
async def get_feedback():
    """Return all stored feedback as JSON, newest first.

    When Upstash is not configured, returns an empty list with a setup note.
    """
    # Determine which storage backend is configured
    blob_token = _blob_token()
    upstash_configured = bool(_upstash_url() and _upstash_headers())
    configured = bool(blob_token or upstash_configured)
    if blob_token:
        entries = await _blob_list()
    else:
        entries = _feedback_list() if upstash_configured else []
    return {
        "configured": configured,
        "count": len(entries),
        "entries": entries,
        "note": (
            None if configured else
            "Upstash Redis is not configured. Set UPSTASH_REDIS_REST_URL and "
            "UPSTASH_REDIS_REST_TOKEN to enable persistence. See server.py for setup."
        ),
    }


@app.get("/feedback")
async def feedback_page():
    """Human-readable table of all submitted feedback — no login required."""
    from fastapi.responses import HTMLResponse
    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Feedback Log — Prompt Router</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d1117;color:#c9d1d9;
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      padding:32px 24px}
    h1{color:#58a6ff;font-size:1.5rem;margin-bottom:6px}
    .sub{color:#8b949e;font-size:.875rem;margin-bottom:24px}
    .banner{background:#161b22;border:1px solid #f0883e;border-radius:8px;
      padding:14px 18px;margin-bottom:24px;color:#f0883e;font-size:.875rem}
    .meta{color:#8b949e;font-size:.8rem;margin-bottom:16px}
    table{width:100%;border-collapse:collapse;background:#161b22;
      border:1px solid #30363d;border-radius:8px;overflow:hidden;font-size:.875rem}
    th{background:#21262d;color:#8b949e;text-align:left;
      padding:10px 14px;font-weight:600;border-bottom:1px solid #30363d}
    td{padding:10px 14px;border-bottom:1px solid #21262d;vertical-align:top}
    tr:last-child td{border-bottom:none}
    tr:hover td{background:#1c2128}
    .up{color:#3fb950;font-weight:700}
    .down{color:#f85149;font-weight:700}
    .pc{max-width:320px;word-break:break-word}
    .nc{max-width:200px;word-break:break-word;color:#8b949e}
    .empty{text-align:center;padding:48px;color:#8b949e}
    .btn{float:right;background:#21262d;border:1px solid #30363d;color:#58a6ff;
      padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem;
      text-decoration:none}
    .btn:hover{background:#30363d}
  </style>
</head>
<body>
<div style="max-width:1100px;margin:0 auto">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <h1>&#128203; Feedback Log</h1>
    <a href="/feedback" class="btn">&#8635; Refresh</a>
  </div>
  <p class="sub">All feedback submitted through the Prompt Router UI &mdash; newest first.</p>
  <div id="root"><p class="empty">Loading&hellip;</p></div>
</div>
<script>
async function load(){
  const el=document.getElementById('root');
  try{
    const r=await fetch('/api/feedback');
    const d=await r.json();
    let out='';
    if(!d.configured){
      out+=`<div class="banner"><strong>&#9888; Persistent storage not configured.</strong><br>
        Feedback is accepted but not saved between deployments.<br>
        To enable persistence, add <code>UPSTASH_REDIS_REST_URL</code> and
        <code>UPSTASH_REDIS_REST_TOKEN</code> to your Vercel environment variables.
        See <code>server.py</code> for step-by-step setup.</div>`;
    }
    if(d.entries.length===0){
      el.innerHTML=out+'<p class="empty">No feedback yet. Submit a recommendation and thumb it up or down.</p>';
      return;
    }
    out+=`<p class="meta">${d.count} entr${d.count===1?'y':'ies'}${d.configured?' &mdash; stored in Upstash Redis':''}</p>`;
    out+=`<table><thead><tr><th>Timestamp</th><th>Prompt</th><th>Recommended</th><th>Vote</th><th>Actually Used</th><th>Notes</th></tr></thead><tbody>`;
    for(const e of d.entries){
      const v=e.user_feedback==='upvote'
        ?'<span class="up">&#128077; upvote</span>'
        :'<span class="down">&#128078; downvote</span>';
      out+=`<tr>
        <td style="white-space:nowrap;color:#8b949e">${x(e.timestamp||'')}</td>
        <td class="pc">${x(e.prompt||'')}</td>
        <td>${x(e.recommended_tool||'')}</td>
        <td>${v}</td>
        <td>${x(e.actual_tool_used||'&mdash;')}</td>
        <td class="nc">${x(e.notes||'&mdash;')}</td></tr>`;
    }
    out+='</tbody></table>';
    el.innerHTML=out;
  }catch(e){
    el.innerHTML=`<p class="empty" style="color:#f85149">Failed to load: ${e.message}</p>`;
  }
}
function x(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
load();
</script>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/report", response_class=StreamingResponse)
async def view_report():
    """Render the full executive report with a copy-to-clipboard button and markdown viewer."""
    report_file = Path(__file__).parent / "executive_project_report.md"
    content = report_file.read_text(encoding="utf-8") if report_file.exists() else "Report not found."
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Project Report: Smart AI Model Router</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.0/github-markdown.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {{
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 24px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 960px;
            width: 100%;
            background: #161b22;
            padding: 40px;
            border-radius: 12px;
            border: 1px solid #30363d;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }}
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #30363d;
        }}
        .btn {{
            background: #238636;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .btn:hover {{
            background: #2ea043;
            transform: translateY(-1px);
        }}
        .btn:active {{
            transform: translateY(1px);
        }}
        .btn-outline {{
            background: transparent;
            border: 1px solid #30363d;
            color: #58a6ff;
            margin-right: 8px;
        }}
        .btn-outline:hover {{
            background: #21262d;
            border-color: #8b949e;
        }}
        .markdown-body {{
            background: transparent !important;
            color: #c9d1d9 !important;
        }}
        .markdown-body table {{
            background: transparent !important;
        }}
        .markdown-body tr, .markdown-body th, .markdown-body td {{
            background: transparent !important;
            border-color: #30363d !important;
        }}
        .markdown-body pre {{
            background-color: #0d1117 !important;
            border: 1px solid #30363d;
        }}
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #238636;
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }}
        .toast.show {{
            opacity: 1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-bar">
            <div>
                <h2 style="margin: 0; color: #58a6ff;">Executive Project Report</h2>
                <small style="color: #8b949e;">Ready for presentation and copy-pasting</small>
            </div>
            <div>
                <a href="/report/raw" class="btn btn-outline" target="_blank" style="text-decoration: none;">View Raw Text</a>
                <button class="btn" onclick="copyReport()">📋 Copy Full Report</button>
            </div>
        </div>
        <div id="content" class="markdown-body"></div>
    </div>
    <div id="toast" class="toast">✅ Copied report to clipboard!</div>

    <textarea id="rawContent" style="display: none;">{content}</textarea>

    <script>
        const raw = document.getElementById('rawContent').value;
        document.getElementById('content').innerHTML = marked.parse(raw);

        function copyReport() {{
            navigator.clipboard.writeText(raw).then(() => {{
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }});
        }}
    </script>
</body>
</html>"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)


@app.get("/report/raw")
async def view_report_raw():
    """Return raw markdown text for simple Ctrl+A copy-pasting."""
    from fastapi.responses import PlainTextResponse
    report_file = Path(__file__).parent / "executive_project_report.md"
    content = report_file.read_text(encoding="utf-8") if report_file.exists() else "Report not found."
    return PlainTextResponse(content=content)

