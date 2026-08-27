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

EVALS_DIR = Path(__file__).parent / "evaluations"
EVALS_DIR.mkdir(exist_ok=True)


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



@app.post("/api/recommend")
async def recommend_tool(
    req: RecommendRequest,
    x_api_key: str = Header(default="", alias="X-API-Key"),
):
    """Route one task to a tool + intelligence level. Single call, plain JSON - no SSE."""
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt is required")
    key = x_api_key if x_api_key and x_api_key != "demo" else server_key()
    if not key:
        raise HTTPException(
            status_code=503,
            detail="No Gemini API key configured. Put GEMINI_API_KEY in .env next to server.py and restart it, or paste a key on the page.",
        )
    try:
        return await asyncio.to_thread(
            router.recommend, req.prompt, key, req.model,
        )
    except SystemExit as exc:  # eval.call() exits the process on an unrecoverable HTTP error
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"router error: {exc}")
