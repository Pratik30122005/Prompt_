"""Prompt evaluation: score successive versions of ONE prompt to prove that a specific
prompt-engineering technique measurably improved the output, not just changed it.

This is deliberately narrower than eval.py's model-comparison mode. Model, task, and (usually)
reference answer are held FIXED across every row; only the prompt text changes, one added
technique at a time, so any score movement is attributable to that one change.

Usage:
  export GEMINI_API_KEY=...
  python evaluation/prompt_iteration.py versions.json --model gemini-3.6-flash --judge-model gemini-3.5-flash

versions.json format - TWO shapes are accepted:

  1) A bare list (each version graded against ITS OWN stated requirements - see caveat below):
[
  {"label": "v1 - bare instruction", "prompt": "Summarize this report."},
  {"label": "v2 + audience/length/tone", "prompt": "Summarize this report for a board audience in under 150 words, formal tone."}
]

  2) An object with a SHARED reference every version is graded against, regardless of what that
     version's own prompt asked for (RECOMMENDED - see caveat below):
{
  "reference": "An ideal answer explicitly states X, Y, Z, in under 150 words, in three labeled sections...",
  "versions": [ {"label": "...", "prompt": "..."}, ... ]
}

CAVEAT - read this before trusting a flat/unchanging score table:
The judge's accuracy/completeness/instruction_following/relevance criteria are defined relative
to "the task" it is given. If you pass each version's own prompt as its only task description
(shape 1, no reference), a VAGUER prompt has an EASIER bar to clear, not a harder one - "Summarize
this" has almost no stated requirements, so a vague summary trivially "completes" it. That
produces misleadingly flat, uniformly-high scores across versions and defeats the whole point of
this script. Use shape (2) with one fixed, detailed reference so every version is graded against
the same yardstick and only response quality actually varies. A per-version "reference" key still
overrides the shared one if a later version's expected shape genuinely changes (e.g. once you
require sections, the reference should show those sections).
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval as e  # reuse call(), judge(), cost(), CRITERIA - do not reimplement scoring


HEADLINE = ["accuracy", "completeness", "instruction_following"]  # the 3 a prompt edit should move


def run_versions(versions, model, judge_model, key, task_input, n, shared_reference=None):
    """task_input: the fixed underlying content/data every version is applied to, so 'the task'
    stays constant and only prompt phrasing/structure varies.

    shared_reference: one fixed external quality bar applied to every version unless that
    version defines its own "reference" override. Without this, each version is graded against
    its OWN stated requirements, which biases toward flat/misleadingly-high scores for vague
    prompts - see the module docstring caveat."""
    rows = []
    for v in versions:
        full_prompt = v["prompt"].format(input=task_input) if "{input}" in v["prompt"] else v["prompt"]
        reference = v.get("reference", shared_reference)
        runs = []
        for i in range(n):
            text, usage, secs = e.call(model, full_prompt, key=key)
            j = e.judge(judge_model, full_prompt, text, key, reference)
            runs.append({"text": text, "scores": j.get("scores", {}),
                         "critical_failures": j.get("critical_failures", []),
                         "verdict": j.get("verdict", "")})
            print("  %s run %d/%d" % (v["label"], i + 1, n), file=sys.stderr)
        rows.append({
            "label": v["label"], "prompt": full_prompt, "runs": runs,
            "avg_score": e.avg_scores(runs), "graded_against_shared_ref": reference is not None,
        })
    return rows


def report(rows, show_verdicts=True, show_text=False):
    if rows and not any(r["graded_against_shared_ref"] for r in rows):
        print("\n*** WARNING: no shared reference was supplied - every version was graded "
              "against its OWN stated requirements, not one fixed bar. A vaguer prompt gets an "
              "EASIER bar to clear this way, which typically produces misleadingly flat/high "
              "scores across versions. Add a top-level \"reference\" to your versions.json "
              "(see the module docstring) and re-run before trusting this table. ***")

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

    all_scores = {v for r in rows for v in r["avg_score"].values() if v is not None}
    if len(rows) > 1 and len(all_scores) == 1:
        print("\n*** WARNING: every version scored EXACTLY the same across every criterion. "
              "That's a sign the judge isn't discriminating between versions - not a sign every "
              "version is equally good. Check the reference/rubric before trusting this. ***")

    if show_verdicts and not show_text:
        print("\njudge verdicts (first run of each version, truncated to 100 chars):")
        for r in rows:
            print("  %-32s %s" % (r["label"], r["runs"][0].get("verdict", "")[:100]))

    if show_text:
        print("\n" + "=" * 70)
        print("FULL PROMPT / RESPONSE / VERDICT PER VERSION (first run of each)")
        print("=" * 70)
        for r in rows:
            print("\n--- %s ---" % r["label"])
            print("\n[PROMPT SENT]\n" + r["prompt"])
            print("\n[FULL RESPONSE]\n" + r["runs"][0].get("text", "<no text captured>"))
            print("\n[FULL JUDGE VERDICT]\n" + r["runs"][0].get("verdict", "<no verdict captured>"))

    fails = {f for r in rows for run in r["runs"] for f in run["critical_failures"]}
    if fails:
        print("\ncritical failures seen across versions: " + ", ".join(sorted(fails)))


def parse_versions_data(data):
    """Accept either file shape: a bare list, or {"reference": ..., "versions": [...]}.
    Returns (versions_list, shared_reference_or_None). Pulled out of main() so this parsing
    logic is unit-testable without going through argparse/file I/O."""
    if isinstance(data, dict):
        return data["versions"], data.get("reference")
    return data, None


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
    p.add_argument("--show-text", action="store_true",
                   help="Print the full prompt, full response, and full (untruncated) judge "
                        "verdict for every version - not just the score table.")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.versions_file:
        p.error("versions_file is required unless --selftest")

    versions = json.load(open(args.versions_file, encoding="utf-8"))
    versions, shared_reference = parse_versions_data(versions)
    key = e.gather_keys([args.model, args.judge_model])
    rows = run_versions(versions, args.model, args.judge_model, key, args.input, args.n,
                         shared_reference)
    report(rows, show_text=args.show_text)


def selftest():
    """Pure-logic checks - no API calls. Confirms report()/aggregation work before spending
    real API budget, and that this module never redefines eval.py's scoring contract."""
    # must reuse eval.py's exact criteria set, never fork its own
    assert e.ALL_JUDGED == e.CRITERIA + e.EXTENDED_CRITERIA + e.CONTEXTUAL_CRITERIA

    fake_rows = [
        {"label": "v1 bare", "prompt": "p1", "graded_against_shared_ref": True,
         "runs": [{"text": "a", "scores": {c: 2 for c in e.CRITERIA}, "critical_failures": [],
                   "verdict": "weak"}]},
        {"label": "v2 + detail", "prompt": "p2", "graded_against_shared_ref": True,
         "runs": [{"text": "b", "scores": {c: 5 for c in e.CRITERIA}, "critical_failures": [],
                   "verdict": "strong"}]},
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

    # --- shared-reference fix: this is the bug that produced flat 5.0-everywhere scores ---
    # bare-list shape still works, with no shared reference (the old, bug-prone default)
    v, ref = parse_versions_data([{"label": "a", "prompt": "p"}])
    assert ref is None and v == [{"label": "a", "prompt": "p"}]

    # new object shape: shared reference is extracted correctly
    v, ref = parse_versions_data({"reference": "GOLD STANDARD", "versions": [{"label": "a", "prompt": "p"}]})
    assert ref == "GOLD STANDARD" and v == [{"label": "a", "prompt": "p"}]

    # per-version reference overrides the shared one; versions without their own fall back to it
    versions3 = [{"label": "a", "prompt": "p"}, {"label": "b", "prompt": "p", "reference": "SPECIFIC"}]
    assert versions3[0].get("reference", "SHARED") == "SHARED"   # falls back
    assert versions3[1].get("reference", "SHARED") == "SPECIFIC"  # overrides

    # report() must warn when nothing in the batch was graded against a shared reference -
    # that's exactly the silent condition that produced the flat-5.0 result
    import io, contextlib
    buf = io.StringIO()
    no_ref_rows = [{**r, "graded_against_shared_ref": False} for r in fake_rows]
    with contextlib.redirect_stdout(buf):
        report(no_ref_rows, show_verdicts=False)
    assert "no shared reference was supplied" in buf.getvalue()

    # and must warn when every version scores identically (the symptom actually observed),
    # even if a reference WAS supplied - catches a lazy/non-discriminating judge too
    flat_rows = [
        {"label": "a", "prompt": "p", "graded_against_shared_ref": True,
         "runs": [{"text": "x", "scores": {c: 5 for c in e.CRITERIA}, "critical_failures": [], "verdict": ""}]},
        {"label": "b", "prompt": "p", "graded_against_shared_ref": True,
         "runs": [{"text": "y", "scores": {c: 5 for c in e.CRITERIA}, "critical_failures": [], "verdict": ""}]},
    ]
    for r in flat_rows:
        r["avg_score"] = e.avg_scores(r["runs"])
    buf2 = io.StringIO()
    with contextlib.redirect_stdout(buf2):
        report(flat_rows, show_verdicts=False)
    assert "scored EXACTLY the same" in buf2.getvalue()

    # a batch with genuine variation triggers NEITHER warning
    buf3 = io.StringIO()
    with contextlib.redirect_stdout(buf3):
        report(fake_rows, show_verdicts=False)
    assert "no shared reference" not in buf3.getvalue()
    assert "scored EXACTLY the same" not in buf3.getvalue()

    # --show-text prints the full prompt, full response, and full (untruncated) verdict -
    # not just a 100-char-truncated verdict line
    text_rows = [{**fake_rows[0], "prompt": "FULL PROMPT TEXT HERE"}]
    text_rows[0]["runs"][0]["text"] = "FULL RESPONSE TEXT HERE, arbitrarily long"
    text_rows[0]["runs"][0]["verdict"] = "A" * 150  # longer than the old 100-char truncation
    buf4 = io.StringIO()
    with contextlib.redirect_stdout(buf4):
        report(text_rows, show_text=True)
    out4 = buf4.getvalue()
    assert "FULL PROMPT TEXT HERE" in out4
    assert "FULL RESPONSE TEXT HERE, arbitrarily long" in out4
    assert "A" * 150 in out4  # the full, untruncated verdict is present, not cut at 100 chars

    print("prompt_iteration selftest ok")


if __name__ == "__main__":
    main()
