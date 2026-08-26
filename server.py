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
