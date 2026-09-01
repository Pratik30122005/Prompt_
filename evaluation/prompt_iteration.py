"""Prompt evaluation: score successive versions of ONE prompt to prove that a specific
prompt-engineering technique measurably improved the output, not just changed it.

This is deliberately narrower than eval.py's model-comparison mode. Model, task, and (usually)
reference answer are held FIXED across every row; only the prompt text changes, one added
technique at a time, so any score movement is attributable to that one change.

Usage:
  export GEMINI_API_KEY=...
  python evaluation/prompt_iteration.py versions.json --model gemini-3.6-flash --judge-model gemini-3.5-flash

versions.json format:
[
  {"label": "v1 - bare instruction", "prompt": "Summarize this report."},
  {"label": "v2 + audience/length/tone", "prompt": "Summarize this report for a board audience in under 150 words, formal tone."},
  {"label": "v3 + explicit constraints", "prompt": "... must include revenue and churn, exclude speculation, flag missing data explicitly."},
  {"label": "v4 + output format", "prompt": "... Respond in three sections: Highlights, Risks, Next Steps."},
  {"label": "v5 + few-shot example", "prompt": "... Example:\\nInput: ...\\nOutput: ..."}
]

Each version can also carry its own "reference" if the expected answer changes shape as the
prompt evolves (e.g. once you require sections, the reference should have those sections too).
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval as e  # reuse call(), judge(), cost(), CRITERIA - do not reimplement scoring


HEADLINE = ["accuracy", "completeness", "instruction_following"]  # the 3 a prompt edit should move


def run_versions(versions, model, judge_model, key, task_input, n):
    """task_input: the fixed underlying content/data every version is applied to, so 'the task'
    stays constant and only prompt phrasing/structure varies."""
    rows = []
    for v in versions:
        full_prompt = v["prompt"].format(input=task_input) if "{input}" in v["prompt"] else v["prompt"]
        runs = []
        for i in range(n):
            text, usage, secs = e.call(model, full_prompt, key=key)
            j = e.judge(judge_model, full_prompt, text, key, v.get("reference"))
            runs.append({"text": text, "scores": j.get("scores", {}),
                         "critical_failures": j.get("critical_failures", []),
                         "verdict": j.get("verdict", "")})
            print("  %s run %d/%d" % (v["label"], i + 1, n), file=sys.stderr)
        rows.append({
            "label": v["label"], "prompt": full_prompt, "runs": runs,
            "avg_score": e.avg_scores(runs),
        })
    return rows


def report(rows):
    cols = HEADLINE + [c for c in e.ALL_JUDGED if c not in HEADLINE]
    print("\n%-32s %s" % ("VERSION", "  ".join(c[:6] for c in cols)))
    prev = None
    for r in rows:
        sc = r["avg_score"]
        line = "  ".join("     -" if sc.get(c) is None else "%6.1f" % sc[c] for c in cols)
        print("%-32s %s" % (r["label"], line))
        if prev is not None:
            deltas = []
            for c in HEADLINE:
                a, b = prev.get(c), sc.get(c)
                if a is not None and b is not None and b != a:
                    deltas.append("%s %+.1f" % (c, b - a))
            if deltas:
                print("  -> " + ", ".join(deltas))
        prev = sc
    fails = {f for r in rows for run in r["runs"] for f in run["critical_failures"]}
    if fails:
        print("\ncritical failures seen across versions: " + ", ".join(sorted(fails)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("versions_file", nargs="?", help="JSON file of {label, prompt, reference?} objects")
    p.add_argument("--input", default="", help="Fixed underlying content/data, substituted into "
                   "any version's prompt that contains {input}")
    p.add_argument("-m", "--model", default="gemini-3.6-flash")
    p.add_argument("--judge-model", default="gemini-3.5-flash",
                   help="Free tier only covers Flash/Flash-Lite - Pro models require billing "
                        "and have no free quota at all as of Apr 2026. Override if you have a "
                        "paid project.")
    p.add_argument("-n", type=int, default=1, help="Repeats per version (>1 also shows variance)")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.versions_file:
        p.error("versions_file is required unless --selftest")

    versions = json.load(open(args.versions_file, encoding="utf-8"))
    key = e.gather_keys([args.model, args.judge_model])
    rows = run_versions(versions, args.model, args.judge_model, key, args.input, args.n)
    report(rows)


def selftest():
    """Pure-logic checks - no API calls. Confirms report()/aggregation work before spending
    real API budget, and that this module never redefines eval.py's scoring contract."""
    # must reuse eval.py's exact criteria set, never fork its own
    assert e.ALL_JUDGED == e.CRITERIA + e.EXTENDED_CRITERIA + e.CONTEXTUAL_CRITERIA

    fake_rows = [
        {"label": "v1 bare", "prompt": "p1",
         "runs": [{"text": "a", "scores": {c: 2 for c in e.CRITERIA}, "critical_failures": []}]},
        {"label": "v2 + detail", "prompt": "p2",
         "runs": [{"text": "b", "scores": {c: 5 for c in e.CRITERIA}, "critical_failures": []}]},
    ]
    for r in fake_rows:
        r["avg_score"] = e.avg_scores(r["runs"])
    assert fake_rows[0]["avg_score"]["accuracy"] == 2
    assert fake_rows[1]["avg_score"]["accuracy"] == 5

    # {input} substitution
    versions = [{"label": "t", "prompt": "Summarize: {input}"}]
    full = versions[0]["prompt"].format(input="XYZ") if "{input}" in versions[0]["prompt"] else versions[0]["prompt"]
    assert full == "Summarize: XYZ"

    # a version with no {input} passes through untouched
    versions2 = [{"label": "t2", "prompt": "Write a poem."}]
    full2 = versions2[0]["prompt"].format(input="ignored") if "{input}" in versions2[0]["prompt"] else versions2[0]["prompt"]
    assert full2 == "Write a poem."

    print("prompt_iteration selftest ok")


if __name__ == "__main__":
    main()
