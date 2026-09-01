"""Extended Thinking ROI: quantify what thinking actually buys you, and at what price, across
tasks of different difficulty. The point is not "thinking is better" - it's finding the
difficulty level where the quality gain stops justifying the extra cost/latency.

Usage:
  export GEMINI_API_KEY=...
  python evaluation/thinking_roi.py tasks.json --model gemini-3.5-flash --budgets 0,4096

tasks.json format (deliberately spans easy -> hard so the crossover point is visible):
[
  {"label": "easy - reformat this list", "prompt": "...", "difficulty": "easy"},
  {"label": "medium - summarize with tradeoffs", "prompt": "...", "difficulty": "medium"},
  {"label": "hard - multi-step architecture decision", "prompt": "...", "difficulty": "hard"}
]
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval as e  # reuse call(), judge(), cost() - thinking tokens already billed as output there


def run_budgets(tasks, model, judge_model, budgets, key, n):
    """NOTE: --budgets values are literal token budgets for Gemini (thinkingConfig.thinkingBudget)
    but only boolean on/off for DeepSeek (0 = disabled, any nonzero = enabled) - DeepSeek's API
    doesn't expose a numeric thinking budget as far as could be confirmed. Comparing budgets
    like 0,4096,8192 against a DeepSeek model will only ever show two distinct behaviors, not
    three - keep that in mind reading the table if you mix providers in one run."""
    rows = []
    for t in tasks:
        for b in budgets:
            runs = []
            for i in range(n):
                text, usage, secs = e.call(model, t["prompt"], thinking=b, key=key)
                j = e.judge(judge_model, t["prompt"], text, key, t.get("reference"))
                runs.append({
                    "text": text, "usage": usage, "secs": secs,
                    "cost": e.cost(model, usage), "scores": j.get("scores", {}),
                })
                print("  %s thinking=%s run %d/%d %.1fs" % (t["label"], b, i + 1, n, secs),
                      file=sys.stderr)
            rows.append({
                "label": t["label"], "difficulty": t.get("difficulty", "?"), "thinking": b,
                "secs": sum(r["secs"] for r in runs) / len(runs),
                "cost": None if runs[0]["cost"] is None else sum(r["cost"] for r in runs) / len(runs),
                "avg_score": e.avg_scores(runs),
            })
    return rows


def roi_table(rows):
    """Group by task, pair thinking-off against each thinking-on budget, compute score delta,
    cost delta, and score-gained-per-dollar - the actual ROI number, not a vibe."""
    by_label = {}
    for r in rows:
        by_label.setdefault(r["label"], []).append(r)

    print("\n%-38s %8s %8s %8s %9s %9s %10s" %
          ("TASK", "THINK", "SCORE", "COST$", "SEC", "d SCORE", "SCORE/$"))
    for label, group in by_label.items():
        group.sort(key=lambda r: (r["thinking"] is None, r["thinking"]))
        baseline = group[0]
        base_score = _headline(baseline["avg_score"])
        for r in group:
            score = _headline(r["avg_score"])
            print("%-38s %8s %8s %8s %9.1f" % (
                label, str(r["thinking"]),
                "-" if score is None else "%.1f" % score,
                "?" if r["cost"] is None else "%.5f" % r["cost"],
                r["secs"]), end="")
            if r is baseline:
                print("      (base)      -")
            else:
                d_score = None if score is None or base_score is None else score - base_score
                d_cost = None if r["cost"] is None or baseline["cost"] is None else r["cost"] - baseline["cost"]
                roi = (d_score / d_cost) if d_score is not None and d_cost not in (None, 0) else None
                print("   %+6s   %8s" % (
                    "-" if d_score is None else "%.1f" % d_score,
                    "-" if roi is None else "%.0f" % roi))


def _headline(avg_score):
    """One summary number per row: mean of accuracy + reasoning_quality, the two dimensions
    thinking should most plausibly move. Keeps the table readable; full breakdown still in avg_score."""
    vals = [avg_score[c] for c in ("accuracy", "reasoning_quality") if avg_score.get(c) is not None]
    return sum(vals) / len(vals) if vals else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tasks_file", nargs="?", help="JSON file of {label, prompt, difficulty, reference?}")
    p.add_argument("-m", "--model", default="gemini-3.5-flash",
                   help="Must support thinkingConfig. Kept off Pro models by default - they "
                        "have had no free-tier quota at all since Apr 2026. Flash models "
                        "support a thinking budget too; override if you have a paid project.")
    p.add_argument("--judge-model", default="gemini-3.5-flash")
    p.add_argument("--budgets", default="0,4096", help="Comma-separated thinking budgets to compare, "
                   "first one treated as the baseline")
    p.add_argument("-n", type=int, default=1)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.tasks_file:
        p.error("tasks_file is required unless --selftest")

    tasks = json.load(open(args.tasks_file, encoding="utf-8"))
    key = e.gather_keys([args.model, args.judge_model])
    budgets = [int(b) for b in args.budgets.split(",")]
    rows = run_budgets(tasks, args.model, args.judge_model, budgets, key, args.n)
    roi_table(rows)


def selftest():
    """Pure-logic checks - no API calls."""
    avg_off = {"accuracy": 3, "reasoning_quality": 3}
    avg_on = {"accuracy": 5, "reasoning_quality": 5}
    assert _headline(avg_off) == 3
    assert _headline(avg_on) == 5
    assert _headline({}) is None

    rows = [
        {"label": "easy", "difficulty": "easy", "thinking": 0, "secs": 1.0, "cost": 0.001,
         "avg_score": avg_off},
        {"label": "easy", "difficulty": "easy", "thinking": 4096, "secs": 3.0, "cost": 0.004,
         "avg_score": avg_on},
    ]
    # sanity: baseline is the lower/zero thinking budget, appears first after sort
    rows_sorted = sorted(rows, key=lambda r: (r["thinking"] is None, r["thinking"]))
    assert rows_sorted[0]["thinking"] == 0

    # ROI arithmetic: score moved +2 for +$0.003 -> ~667 score-per-dollar
    d_score = _headline(avg_on) - _headline(avg_off)
    d_cost = rows[1]["cost"] - rows[0]["cost"]
    assert abs(d_score - 2) < 1e-9
    assert abs(d_cost - 0.003) < 1e-9
    roi = d_score / d_cost
    assert abs(roi - 666.666) < 1

    print("thinking_roi selftest ok")


if __name__ == "__main__":
    main()
