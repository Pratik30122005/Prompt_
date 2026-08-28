"""retune.py — Feedback-driven weight calibration for the LLM recommendation engine.

Reads evaluations/feedback.jsonl, computes which dimension weights would have
produced the user's preferred tool recommendation, and writes updated weights to
weights.json — with safeguards against overfitting, drastic shifts, and bad retunes.

Usage:
    python retune.py              # run calibration if enough data
    python retune.py --status     # show current weights + feedback stats
    python retune.py --rollback   # revert to last saved weights.json.bak
    python retune.py --force      # bypass minimum-sample guard (testing only)

Safeguards
----------
1. MINIMUM SAMPLE SIZE: retune only runs when >= MIN_SAMPLES downvotes exist.
   Early on, a single downvote cannot swing all weights; it only gets ignored.

2. PER-RUN WEIGHT CHANGE CAP: each weight can move at most MAX_DELTA per run.
   Prevents one batch of feedback from flipping the model completely.

3. AUTOMATIC BACKUP: before writing new weights, always saves weights.json.bak.
   Use --rollback to revert in one command.

4. SUM-TO-ONE ENFORCED: after adjustment, weights are renormalized so they still
   sum to 1.0.
"""
import argparse
import json
import os
import shutil
import sys

# ── Config ────────────────────────────────────────────────────────────────

_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_PATH = os.path.join(_DIR, "evaluations", "feedback.jsonl")
WEIGHTS_PATH  = os.path.join(_DIR, "weights.json")
BACKUP_PATH   = os.path.join(_DIR, "weights.json.bak")

# Minimum number of DOWNVOTED entries before retune is allowed to run.
# Rationale: a single downvote is anecdote; ≥5 is a pattern.
MIN_SAMPLES = 5

# Maximum absolute change any single weight can make per retune run.
# Rationale: keeps the engine stable between runs; prevents wild oscillation.
MAX_DELTA = 0.05

_DIMS = ["capability", "tool", "context", "cost", "latency"]

_DEFAULT_WEIGHTS = {
    "capability": 0.35,
    "tool":       0.25,
    "context":    0.15,
    "cost":       0.15,
    "latency":    0.10,
}


# ── Helpers ───────────────────────────────────────────────────────────────

def load_weights() -> dict:
    try:
        with open(WEIGHTS_PATH) as f:
            w = json.load(f)
        return {k: float(w.get(k, v)) for k, v in _DEFAULT_WEIGHTS.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULT_WEIGHTS)


def save_weights(w: dict):
    # Always back up first
    if os.path.exists(WEIGHTS_PATH):
        shutil.copy2(WEIGHTS_PATH, BACKUP_PATH)
    with open(WEIGHTS_PATH, "w") as f:
        json.dump(w, f, indent=2)
    print(f"  ✅ Weights saved → {WEIGHTS_PATH}")
    print(f"  📦 Backup saved  → {BACKUP_PATH}")


def load_feedback() -> list[dict]:
    entries = []
    if not os.path.exists(FEEDBACK_PATH):
        return entries
    with open(FEEDBACK_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def normalize(w: dict) -> dict:
    """Renormalize so weights sum to 1.0."""
    total = sum(w.values())
    if total == 0:
        return dict(_DEFAULT_WEIGHTS)
    return {k: round(v / total, 6) for k, v in w.items()}


# ── Dimension attribution ─────────────────────────────────────────────────
# For each downvoted entry where the user reveals the actual preferred tool,
# we ask: "which dimension, if it had a higher weight, would have promoted the
# preferred tool above the recommended tool?"
#
# We compute sub-scores for both tools and identify dimensions where
# preferred_tool scored HIGHER than recommended_tool.  Those dimensions are
# where we should increase weight (the signal says they were under-valued).

def _sub_scores(tool_id: str, tools_kb: dict, cls: dict) -> dict:
    """
    Simplified sub-score computation matching router.py logic.
    Returns dict of {dim: sub_score} for one tool.
    """
    info = tools_kb.get(tool_id, {})
    task_type = cls.get("task_type", "writing")

    # capability
    if task_type in info.get("best_for", []):
        s_task = 1.0
    elif task_type in info.get("avoid_for", []):
        s_task = 0.0
    else:
        s_task = 0.5
    depth = cls.get("reasoning_depth", "medium")
    high_cap = ("extended thinking" in info.get("tiers", {}).get("max", "").lower()
                or tool_id in ["claude-code", "chatgpt"])
    s_reason = (1.0 if high_cap else 0.5) if depth == "high" else (0.85 if depth == "medium" else 1.0)
    s_cap = 0.6 * s_task + 0.4 * s_reason

    # tool
    tool_req = cls.get("tool_use_needed", "none")
    if tool_req == "none":
        s_tool = 1.0
    elif tool_req in info.get("supported_tools", []):
        s_tool = 1.0
    else:
        s_tool = 0.2 if tool_id in ["claude", "gemini"] else 0.0

    # context
    ctx_map = {"short": 8_000, "medium": 64_000, "long": 200_000, "extreme": 1_000_000}
    req_tokens = ctx_map.get(cls.get("context_length_req", "medium"), 64_000)
    s_ctx = 1.0 if info.get("context_capacity", 0) >= req_tokens else 0.0

    # cost
    cost_sens = cls.get("cost_sensitivity", "medium")
    s_cost = (1.0 - info.get("cost_tier", 0.5)) if cost_sens == "high" else 1.0

    # latency
    lat_sens = cls.get("latency_sensitivity", "medium")
    s_lat = info.get("latency_tier", 0.7) if lat_sens == "high" else 1.0

    return {
        "capability": s_cap,
        "tool":       s_tool,
        "context":    s_ctx,
        "cost":       s_cost,
        "latency":    s_lat,
    }


def compute_gradient(weights: dict, downvotes: list[dict], tools_kb: dict) -> dict:
    """
    For each downvote with a known actual_tool_used:
      1. Re-classify (use the saved classification if available, else fall back to defaults).
      2. Identify dims where actual_tool scored higher than recommended_tool.
      3. Accumulate a gradient: +1 for dims that should increase weight.

    Returns a dict of {dim: normalized_gradient} in [-1, +1].
    """
    gradient = {d: 0.0 for d in _DIMS}
    counted = 0

    for entry in downvotes:
        rec_tool    = entry.get("recommended_tool", "")
        actual_tool = entry.get("actual_tool_used", "")
        cls_hint    = entry.get("classification", {})  # may be absent in old logs

        if not actual_tool or rec_tool == actual_tool:
            continue  # can't attribute if we don't know what was preferred

        # Build a minimal classification schema for scoring
        cls = {
            "task_type":        cls_hint.get("task_type", "writing"),
            "reasoning_depth":  cls_hint.get("reasoning_depth", "medium"),
            "context_length_req": cls_hint.get("context_length_req", "medium"),
            "cost_sensitivity": cls_hint.get("cost_sensitivity", "medium"),
            "latency_sensitivity": cls_hint.get("latency_sensitivity", "medium"),
            "tool_use_needed":  cls_hint.get("tool_use_needed", "none"),
        }

        scores_rec    = _sub_scores(rec_tool,    tools_kb, cls)
        scores_actual = _sub_scores(actual_tool, tools_kb, cls)

        for dim in _DIMS:
            # If the actual (preferred) tool scored higher on this dim,
            # that dim was underweighted → nudge it up.
            delta = scores_actual[dim] - scores_rec[dim]
            gradient[dim] += delta
        counted += 1

    if counted == 0:
        return gradient

    # Normalize gradient to [-1, 1]
    max_abs = max(abs(v) for v in gradient.values()) or 1.0
    return {d: round(v / (max_abs * counted), 6) for d, v in gradient.items()}


def apply_gradient(weights: dict, gradient: dict, learning_rate: float = 0.1) -> dict:
    """
    Nudge weights in the direction of the gradient, clipped by MAX_DELTA.
    """
    new_weights = {}
    for dim in _DIMS:
        raw_delta = gradient[dim] * learning_rate
        clamped   = max(-MAX_DELTA, min(MAX_DELTA, raw_delta))
        new_weights[dim] = max(0.01, weights[dim] + clamped)  # keep weights positive
    return normalize(new_weights)


# ── Main ──────────────────────────────────────────────────────────────────

def run_retune(force: bool = False):
    # Load tools knowledge base from router
    sys.path.insert(0, _DIR)
    import router
    tools_kb = router.TOOLS

    feedback = load_feedback()
    upvotes   = [e for e in feedback if e.get("user_feedback") == "upvote"]
    downvotes = [e for e in feedback if e.get("user_feedback") == "downvote"]
    actionable = [e for e in downvotes if e.get("actual_tool_used")]

    print(f"\n{'='*60}")
    print("RETUNE STATUS")
    print(f"{'='*60}")
    print(f"  Total feedback entries : {len(feedback)}")
    print(f"  Upvotes                : {len(upvotes)}")
    print(f"  Downvotes              : {len(downvotes)}")
    print(f"  Actionable downvotes   : {len(actionable)}  (have actual_tool_used)")
    print(f"  Min required           : {MIN_SAMPLES}")

    current_weights = load_weights()
    print(f"\n  Current weights: {json.dumps(current_weights, indent=4)}")

    if len(actionable) < MIN_SAMPLES and not force:
        print(f"\n  ⚠️  Insufficient actionable downvotes ({len(actionable)} < {MIN_SAMPLES}).")
        print("  Retune skipped. Collect more feedback or use --force to override.")
        return

    print(f"\n  Running gradient computation on {len(actionable)} actionable downvotes…")
    gradient = compute_gradient(current_weights, actionable, tools_kb)
    print(f"  Gradient: {gradient}")

    new_weights = apply_gradient(current_weights, gradient)

    print(f"\n  Proposed new weights (capped Δ={MAX_DELTA} per dim):")
    for dim in _DIMS:
        old = current_weights[dim]
        new = new_weights[dim]
        arrow = "↑" if new > old else ("↓" if new < old else "=")
        print(f"    {dim:<12}  {old:.4f}  →  {new:.4f}  {arrow}")

    print(f"\n  Sum check: {sum(new_weights.values()):.6f}  (must ≈ 1.0)")

    confirm = input("\n  Apply these weights? [y/N]: ").strip().lower()
    if confirm == "y":
        save_weights(new_weights)
    else:
        print("  Aborted — no changes written.")


def show_status():
    feedback = load_feedback()
    upvotes   = sum(1 for e in feedback if e.get("user_feedback") == "upvote")
    downvotes = sum(1 for e in feedback if e.get("user_feedback") == "downvote")
    print(f"\n  Feedback log : {FEEDBACK_PATH}")
    print(f"  Entries      : {len(feedback)} ({upvotes} up / {downvotes} down)")
    print(f"  Current weights: {json.dumps(load_weights(), indent=4)}")
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH) as f:
            print(f"  Backup weights : {json.dumps(json.load(f), indent=4)}")


def rollback():
    if not os.path.exists(BACKUP_PATH):
        print("  No backup found at weights.json.bak.")
        sys.exit(1)
    shutil.copy2(BACKUP_PATH, WEIGHTS_PATH)
    print(f"  ✅ Rolled back weights.json from {BACKUP_PATH}")
    print(f"  Restored weights: {json.dumps(load_weights(), indent=4)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status",   action="store_true", help="Show current weights and feedback stats")
    parser.add_argument("--rollback", action="store_true", help="Revert to weights.json.bak")
    parser.add_argument("--force",    action="store_true", help="Bypass minimum-sample guard")
    args = parser.parse_args()

    if args.rollback:
        rollback()
    elif args.status:
        show_status()
    else:
        run_retune(force=args.force)


if __name__ == "__main__":
    main()
