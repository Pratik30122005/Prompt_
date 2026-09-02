# Prompt Evaluation — Methodology & Results

This document explains what "prompt evaluation" means in this project, how it's actually
implemented, and shows a real, run example — not a theoretical one.

## What this is (and isn't)

There are two different things that could be called "evaluation" in an AI project:

- **Model evaluation** — comparing different *models* on the same task (e.g. "is Gemini or
  DeepSeek better at this?"). That's a separate concern, handled by `eval.py`.
- **Prompt evaluation** — holding the model and the task fixed, and testing whether *changing
  the prompt itself* measurably changes the quality of the output. That's what this document
  and `evaluation/prompt_iteration.py` are about.

The method: pick one task, write a bare/simple version of the prompt, score the output. Then
improve the prompt step by step — add detail, add explicit conditions, add a required output
format, add a worked example (few-shot) — scoring the output again after each change. The goal
is to see, with real numbers, whether and when each technique actually helps.

## Why every version is graded against ONE fixed standard

The first version of this tool graded each prompt version against *its own* stated
requirements. That was a bug: a vague prompt has almost nothing to fail, so it trivially scored
well, making every version look equally good. The fix was to grade every version against one
fixed, detailed description of what a genuinely great answer looks like — supplied once, used
for every version, regardless of what that version's own prompt happened to ask for. Only then
does response quality — not the leniency of the version's own wording — drive the score.

See `evaluation/prompt_iteration.py`'s module docstring for the two supported input-file shapes
(a plain list, or an object with a shared `"reference"` — the second is the one to use).

## The grading engine

Every score below comes from the same "judge" prompt used everywhere else in this project — see
`eval.py`'s `JUDGE_SYSTEM` for the full text. In short: a second AI call grades one response
against the task on nine criteria (accuracy, completeness, relevance, instruction-following,
consistency, hallucination control, reasoning quality, safety, and business alignment — the last
one only when a business context is supplied), 1–5 each, with every score below 5 required to
trace back to a specific, named defect — not a vague impression.

## Real example: board-report summary

**Fixed reference (the standard every version is graded against):**

> An ideal response is a formal, board-ready summary of the report, under 150 words, using
> three clearly labeled sections: Highlights, Risks, Next Steps. It explicitly states the exact
> revenue figure and its percentage growth, explicitly states the churn percentage, notes the
> number of enterprise deals closed, and treats the rise in support-ticket volume as a flagged
> risk needing investigation rather than ignoring it or speculating about its cause. It does not
> invent numbers or context beyond what the input actually states.

**Fixed task data (same for every version):**

> Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket
> volume up 15%

**The five prompt versions:**

1. **v1 — bare instruction:** `Summarize this: {input}`
2. **v2 — + audience/length/tone:** `Summarize this for a board of directors in under 150
   words, formal tone: {input}`
3. **v3 — + explicit constraints:** adds "you must call out revenue and churn explicitly, must
   not speculate beyond what the data shows, and must flag any missing data points instead of
   guessing"
4. **v4 — + output format:** adds "Respond in exactly three sections with these headers:
   Highlights, Risks, Next Steps"
5. **v5 — + few-shot example:** adds one worked input/output example before the real input

(Full exact text of all five is in `evaluation/examples/prompt_versions_example.json`.)

**Real results (actual run, Gemini 3.6 Flash under test, Gemini 3.5 Flash Lite as judge):**

| Version | Accuracy | Completeness | Instr. Following | Relevance | Consistency | Halluc. Control | Reasoning | Safety |
|---|---|---|---|---|---|---|---|---|
| v1 — bare instruction | 3.0 | 2.0 | 2.0 | 3.0 | 5.0 | 3.0 | 3.0 | 5.0 |
| v2 + audience/tone | 5.0 | 3.0 | 2.0 | 4.0 | 5.0 | 5.0 | 4.0 | 5.0 |
| v3 + constraints | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |
| v4 + output format | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |
| v5 + few-shot | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |

**What actually happened, version to version:**
- v1 → v2: accuracy +2.0, completeness +1.0 — better, but still missed the word limit and used
  no sections.
- v2 → v3: completeness +2.0, instruction_following +3.0 — explicit "must/must not" rules
  pushed every score to the maximum.
- v3 → v4 → v5: no further change — v3 already satisfied the full reference, so later
  techniques had nothing left to improve on *this* task.

**Judge verdicts (one sentence each, first run):**
- v1: "Failed to use the required sections (Highlights, Risks, Next Steps) specified in the
  reference."
- v2: "Went over the 150-word limit and did not use the required sections."
- v3: "Perfectly follows all constraints, maintains a formal tone, explicitly mentions revenue
  and churn."
- v4: "Fully satisfies all content, formatting, tone, length, and constraint requirements."
- v5: "Followed all constraints, formatting rules, and word limits while accurately reflecting
  the data."

## How to reproduce or run a new example

```bash
export GEMINI_API_KEY=your_key
python evaluation/prompt_iteration.py evaluation/examples/prompt_versions_example.json \
  --input "your own task data here" --show-text
```

`--show-text` prints the full prompt, full model response, and full (untruncated) judge verdict
for every version — not just the score table — so a complete side-by-side record can be kept,
not just the numbers.

## Known limitation

This method needs an AI to write a good fixed reference *and* a well-designed set of prompt
versions to be meaningful — a badly written reference or a set of versions that don't actually
differ in quality will still produce a flat or misleading result. The two built-in warnings in
`report()` (no shared reference supplied; every version scored identically) catch the most
common failure modes automatically, but they don't replace judgment about whether the reference
and the versions were well-designed in the first place.
