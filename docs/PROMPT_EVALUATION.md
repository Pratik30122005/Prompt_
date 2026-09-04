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

---

## Evaluation Toolkit Coverage

> **Note on scope:** The automated evaluation toolkit (`eval.py` + `evaluation/prompt_iteration.py` + `evaluation/thinking_roi.py`) currently tests **Gemini and DeepSeek models directly via their APIs**. The router's other recommendable tools — Claude, ChatGPT, Perplexity, and Gamma — are part of the recommendation knowledge base and appear in routing decisions, but they are **not yet wired into this automated judge pipeline**. Scores and transcripts in this document reflect Gemini models only. Extending the pipeline to cover those tools would require their respective API credentials and provider-specific call/extract logic in `eval.py`.

---

## Full Transcripts

Real captured output from the command below — exact prompts sent, full model responses, and full (untruncated) judge verdicts for all five versions.

```bash
python evaluation/prompt_iteration.py evaluation/examples/prompt_versions_example.json \
  --model gemini-3.6-flash --judge-model gemini-3.5-flash-lite \
  --input "Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%" \
  --show-text
```

---

### v1 — bare instruction

**Prompt sent:**
```
Summarize this: Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%
```

**Full response:**
```
Here is a summary of the Q1 report:

* **Revenue:** $2.3M (up 8% quarter-over-quarter)
* **Enterprise Deals:** 3 closed
* **Churn Rate:** 4.1%
* **Support Tickets:** Volume increased by 15%
```

**Full judge verdict:**
```
The model failed to use the required sections (Highlights, Risks, Next Steps) and did not treat the support ticket increase as a risk.
```

---

### v2 — + audience/length/tone

**Prompt sent:**
```
Summarize this for a board of directors in under 150 words, formal tone: Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%
```

**Full response:**
```
**Executive Summary: Q1 Financial & Operational Performance**

During the first quarter, the company demonstrated solid top-line growth, generating **$2.3 million in revenue**, representing an **8% increase quarter-over-quarter**. Expansion was largely driven by commercial momentum in higher-value segments, highlighted by the successful execution of **three major enterprise deals**.

Customer retention remained stable, with quarterly **churn standing at 4.1%**. Operationally, the business experienced a **15% increase in support ticket volume**, reflecting heightened user engagement aligned with customer growth.

Overall, Q1 reflects strong financial progress. Management remains focused on sustaining revenue momentum while optimizing support capacity to efficiently serve our expanding client base.
```

**Full judge verdict:**
```
The response missed the required three labeled sections and speculated on the support ticket volume rather than treating it as a risk.
```

---

### v3 — + explicit constraints

**Prompt sent:**
```
Summarize this for a board of directors in under 150 words, formal tone. You must call out revenue and churn explicitly, must not speculate beyond what the data shows, and must flag any missing data points instead of guessing: Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%
```

**Full response:**
```
**Q1 Executive Summary**

During Q1, total **revenue** reached $2.3M, representing an 8% quarter-over-quarter increase. Customer **churn** was recorded at 4.1%. Additional operational outcomes include closing 3 enterprise deals and experiencing a 15% increase in support ticket volume.

**Flagged Missing Data Points:**
To conduct a complete assessment, the board should note the following missing metrics:
* **Enterprise Deal Value:** Total contract value and financial impact of the 3 closed deals are unstated.
* **Churn Context:** Historical churn benchmarks, trend lines, and distinction between logo and revenue churn are absent.
* **Support Volume Metrics:** Absolute ticket counts and the specific comparison period (QoQ vs. YoY) for the 15% increase are omitted.
* **Annual Metrics:** Year-over-Year (YoY) revenue figures are not provided.

No further inferences have been drawn beyond these reported metrics.
```

**Full judge verdict:**
```
The response fails the word count limit and misses the structured sections requested in the reference guidelines.
```

---

### v4 — + output format

**Prompt sent:**
```
Summarize this for a board of directors in under 150 words, formal tone. You must call out revenue and churn explicitly, must not speculate beyond what the data shows, and must flag any missing data points instead of guessing. Respond in exactly three sections with these headers: Highlights, Risks, Next Steps: Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%
```

**Full response:**
```
**Highlights**
Q1 revenue reached $2.3M, representing an 8% growth quarter-over-quarter. The company successfully closed 3 enterprise deals during this period.

**Risks**
Q1 customer churn stood at 4.1%, and support ticket volume increased by 15%.
*Missing Data:* The report lacks historical context or targets to evaluate whether the 4.1% churn rate aligns with projections, as well as qualitative data explaining the rise in support ticket volume.

**Next Steps**
*Missing Data:* The source report specifies no operational next steps, forward guidance, or strategic initiatives. Management must provide baseline targets, year-over-year comparisons, and a corrective action plan to address rising support tickets.
```

**Full judge verdict:**
```
The response perfectly follows all length, section, tone, and explicit data constraints.
```

---

### v5 — + few-shot example

**Prompt sent:**
```
Summarize this for a board of directors in under 150 words, formal tone. You must call out revenue and churn explicitly, must not speculate beyond what the data shows, and must flag any missing data points instead of guessing. Respond in exactly three sections with these headers: Highlights, Risks, Next Steps.

Example:
Input: Q1 report, revenue $2M (+5%), churn 3%, no support-ticket data available.
Output:
Highlights: Revenue grew 5% to $2M.
Risks: Churn holding at 3%; support-ticket volume unavailable this quarter, so satisfaction trend cannot be confirmed.
Next Steps: Restore support-ticket reporting before next board cycle.

Now do the same for:
Q1 report: revenue $2.3M (+8% QoQ), churn 4.1%, 3 enterprise deals closed, support ticket volume up 15%
```

**Full response:**
```
Highlights:
Q1 revenue reached $2.3M, representing an 8% quarter-over-quarter increase. The period also saw 3 enterprise deals closed.

Risks:
Quarterly churn stood at 4.1%. Additionally, support ticket volume increased by 15%. Root-cause analysis for the churn, resolution metrics for support tickets, and customer satisfaction data are missing from this report.

Next Steps:
Investigate the operational drivers behind the 15% support ticket surge and the 4.1% churn rate, and ensure complete ticket resolution and customer retention data are included in the subsequent cycle.
```

**Full judge verdict:**
```
The response followed all constraints, included exact metrics, maintained a formal tone, and correctly used the three required headers.
```
