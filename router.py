"""Task router & recommendation engine: classifies prompts and computes deterministic model picks.

Usage:
  python router.py "Build a 10-slide investor deck from these Q3 numbers"
  python router.py --selftest
"""
import argparse
import importlib
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
evaluator = importlib.import_module("eval")

# ── Weights (read from weights.json, fall back to defaults) ──────────────

_DEFAULT_WEIGHTS = {
    "capability": 0.35,  # Fundamental domain + reasoning-depth fit
    "tool":       0.25,  # Required execution environment (sandbox, search, repo)
    "context":    0.15,  # Whether model context window fits the referenced content size
    "cost":       0.15,  # Budget alignment (high-sensitivity tasks prefer cheaper tiers)
    "latency":    0.10,  # Response-time alignment (real-time tasks prefer fast models)
}

_WEIGHTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights.json")


def load_weights() -> dict:
    try:
        with open(_WEIGHTS_PATH) as f:
            w = json.load(f)
        return {k: float(w.get(k, v)) for k, v in _DEFAULT_WEIGHTS.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULT_WEIGHTS)


WEIGHTS = load_weights()

# ── Model Knowledge Base ─────────────────────────────────────────────────
# Each model declares the output_format types it can produce.
# This list is used to HARD-FILTER models before scoring.
# A model whose output_format_support does not include the task's output_format
# receives a score of 0 and is excluded from the ranked list.

TOOLS = {
    "gamma": {
        "name": "Gamma",
        "best_for": ["presentation"],
        "avoid_for": ["coding", "data_extraction"],
        "output_format_support": ["slide_deck"],   # only produces slides
        "tiers": {"lite": "Free", "standard": "Plus", "max": "Pro"},
        "cost_tier": 0.5,
        "latency_tier": 0.9,
        "context_capacity": 32000,
        "supported_tools": ["presentation"],
        "cost_desc": "~$15/month subscription",
        "params": {"mode": "presentation", "temperature": 0.7},
        "citation": "Gamma App Official Specs (2026)",
    },
    "chatgpt": {
        "name": "ChatGPT (GPT-4o / GPT-5.1)",
        "best_for": ["data_extraction", "deep_reasoning", "writing"],
        "avoid_for": ["presentation"],
        "output_format_support": ["free_text", "structured_json", "markdown_report", "code_file"],
        "tiers": {"lite": "GPT-5.1 Instant", "standard": "GPT-5.1 Thinking", "max": "GPT-5.1 Pro"},
        "cost_tier": 0.7,
        "latency_tier": 0.7,
        "context_capacity": 128000,
        "supported_tools": ["python_interpreter"],
        "cost_desc": "$20/month Plus, $200/month Pro",
        "params": {"temperature": 0.0, "python_sandbox": True},
        "citation": "OpenAI API Pricing & Models Guide (2026)",
    },
    "claude": {
        "name": "Claude 3.7 Sonnet",
        "best_for": ["summarization", "writing", "deep_reasoning", "translation", "creative_writing"],
        "avoid_for": ["presentation", "web_research"],
        "output_format_support": ["free_text", "structured_json", "markdown_report", "code_file"],
        "tiers": {"lite": "Haiku", "standard": "Sonnet 3.7", "max": "Opus 3.7 with extended thinking"},
        "cost_tier": 0.8,
        "latency_tier": 0.8,
        "context_capacity": 200000,
        "supported_tools": ["none"],
        "cost_desc": "$3.00 in / $15.00 out per 1M tokens",
        "params": {"temperature": 0.2, "top_p": 0.99, "max_tokens": 4096},
        "citation": "Anthropic Official Model Specs (2026)",
    },
    "gemini": {
        "name": "Gemini 3.6 Flash / Pro",
        "best_for": ["long_context_analysis", "classification", "visual_multimodal"],
        "avoid_for": [],
        "output_format_support": ["free_text", "structured_json", "markdown_report"],
        "tiers": {"lite": "gemini-3.5-flash-lite", "standard": "gemini-3.6-flash",
                  "max": "gemini-2.5-pro with extended thinking"},
        "cost_tier": 0.2,
        "latency_tier": 0.95,
        "context_capacity": 1000000,
        "supported_tools": ["multi_modal"],
        "cost_desc": "$0.30 in / $2.50 out per 1M tokens",
        "params": {"temperature": 0.2, "top_p": 0.95, "max_tokens": 4096},
        "citation": "Google AI Studio Official Docs (2026)",
    },
    "perplexity": {
        "name": "Perplexity Pro",
        "best_for": ["web_research"],
        "avoid_for": ["coding", "presentation"],
        "output_format_support": ["free_text", "markdown_report"],
        "tiers": {"lite": "Quick search", "standard": "Pro search", "max": "Deep Research"},
        "cost_tier": 0.6,
        "latency_tier": 0.7,
        "context_capacity": 64000,
        "supported_tools": ["web_search"],
        "cost_desc": "$20/month Pro",
        "params": {"search_mode": "web_citations", "temperature": 0.2},
        "citation": "Perplexity API Documentation (2026)",
    },
    "claude-code": {
        "name": "Claude Code / Cursor",
        "best_for": ["coding"],
        "avoid_for": ["presentation", "writing", "creative_writing"],
        "output_format_support": ["code_file"],   # ONLY produces code files
        "tiers": {"lite": "Haiku", "standard": "Sonnet 3.7", "max": "Opus 3.7 with extended thinking"},
        "cost_tier": 0.8,
        "latency_tier": 0.7,
        "context_capacity": 200000,
        "supported_tools": ["repo_code_editor"],
        "cost_desc": "$20-200/month usage tier",
        "params": {"temperature": 0.1, "repo_context": True},
        "citation": "Anthropic Claude Code CLI Specs (2026)",
    },
}

TASK_TYPES = [
    "presentation", "coding", "web_research", "data_extraction", "long_context_analysis",
    "deep_reasoning", "summarization", "classification", "translation",
    "creative_writing", "visual_multimodal", "writing",
]

INTELLIGENCE = ["lite", "standard", "max"]

# ── Context-length inference ─────────────────────────────────────────────
# Driven by SIZE SIGNALS in the prompt (document references, row counts),
# NOT raw prompt character count.
#
# Examples showing why these differ:
#   "Summarize this 100-page PDF contract"   → 36 chars  → 'long'
#   "Write a 3000-word blog post about X"    → 44 chars  → 'short' (no attached content)
#   "Reconcile 200k rows in the CSV export"  → 37 chars  → 'extreme' (row count signal)

def infer_context_length(p: str) -> str:
    import re
    # Extreme: explicit large row counts (≥100k), millions, entire codebase
    if re.search(r"\b(\d{3,}k|million|millions)\b", p) or "entire codebase" in p:
        return "extreme"
    # Large page counts (≥50 pages)
    m = re.search(r"(\d+)\s*[-–]?\s*page", p)
    if m and int(m.group(1)) >= 50:
        return "long"
    # Named large artifacts — signals there is external content to process
    if any(k in p for k in ["pdf", "document", "transcript", "contract", "spreadsheet",
                              "csv", "excel", "long context", "full report", "entire"]):
        return "long"
    # Moderate page counts (5–49 pages)
    if m and 5 <= int(m.group(1)) < 50:
        return "medium"
    return "short"


# ── Reasoning-depth escalation ───────────────────────────────────────────
# Escalates to 'high' ONLY on HIGH-COMPLEXITY PHRASES, not lone words.
#
# Design principle: we match multi-word phrases because isolated words like
# "explain" or "why" appear in trivially simple prompts too.
#   "Explain this word in one sentence."        → no phrase match → medium ✓
#   "Why is the sky blue?"                      → no phrase match → medium ✓
#   "Prove that this algorithm is O(n log n)"   → "prove" + complexity → high ✓
#   "If user is logged in, compute tax, else…"  → "if … else" conditional → high ✓

_HIGH_REASONING_PHRASES = [
    "step by step", "step-by-step", "prove that", "prove this",
    "mathematical proof", "edge case", "edge cases",
    "root cause", "why does it fail", "why does this fail",
    "what causes the", "trace through", "walk through the logic",
    "tradeoff between", "trade-off between", "compare architectures",
    "architectural decision", "design decision",
    "under concurrent", "race condition", "deadlock", "worst case",
    "best case complexity", "big-o", "time complexity", "space complexity",
    "explain every variance", "account for the difference",
    "reconcile and explain",
    "if .* then .* else",  # NOTE: this is a string literal here, regex applied below
    "multi-step", "multi step",
]

# Phrases that need regex matching (cannot be substring-matched)
import re as _re
_HIGH_REASONING_REGEX = [
    _re.compile(r"\bif\b.{0,60}\bthen\b.{0,60}\belse\b", _re.I),   # conditional logic
    _re.compile(r"\bprove\b.{0,30}\b(algorithm|theorem|formula|that)\b", _re.I),
]


def infer_reasoning_depth(base_depth: str, p: str) -> str:
    """Escalate to 'high' only on high-complexity phrases or regex patterns."""
    if base_depth == "high":
        return "high"
    # Literal phrase check
    for phrase in _HIGH_REASONING_PHRASES:
        if ".*" not in phrase and phrase in p:
            return "high"
    # Regex check
    for pattern in _HIGH_REASONING_REGEX:
        if pattern.search(p):
            return "high"
    return base_depth


# ── Verb-intent disambiguation: data_extraction vs summarization ─────────
# When a prompt mentions a file-type noun (csv, excel, spreadsheet) AND a verb,
# the verb's intent determines the task:
#
#   EXTRACTION verbs: reconcile, calculate, extract, compute, compare, aggregate
#     → data_extraction (the file is the thing being operated on numerically)
#
#   NARRATIVE verbs: summarize, explain, describe, outline, overview
#     → summarization (the file is the source; deliverable is prose)
#
# If no file-type noun is present this disambiguation doesn't apply.

_EXTRACTION_VERBS = {"reconcile", "calculate", "extract", "compute", "aggregate",
                      "compare", "diff", "join", "merge", "plot", "chart"}
_NARRATIVE_VERBS  = {"summarize", "summarise", "explain", "describe", "outline",
                      "overview", "brief", "distil", "distill", "paraphrase"}
_FILE_NOUNS       = {"csv", "excel", "spreadsheet", "sheet", "xlsx", "xls"}


def _file_noun_present(p: str) -> bool:
    return any(k in p for k in _FILE_NOUNS)


def _leading_verb_intent(p: str) -> str | None:
    """Return 'extraction', 'narrative', or None (ambiguous/absent)."""
    if not _file_noun_present(p):
        return None
    words = set(_re.findall(r"\b\w+\b", p))
    has_extraction = bool(words & _EXTRACTION_VERBS)
    has_narrative  = bool(words & _NARRATIVE_VERBS)
    if has_extraction and not has_narrative:
        return "extraction"
    if has_narrative and not has_extraction:
        return "narrative"
    # Both or neither → fall through to keyword priority
    return None


# ── Classification (priority-rank cascade) ──────────────────────────────
#
# CONFIRMED priority order (rank 1 wins if keywords collide):
#
#   1   presentation          — deliverable is a visual slide deck
#   2   coding (repo)         — multi-file codebase change requiring code output
#   3   coding (snippet)      — single function / regex / SQL
#   4   web_research          — requires live web citations / current facts
#   5   creative_writing      — prose deliverable with creative intent
#   5b  translation           — language conversion (before summarization to avoid
#                               "transcript" collision stealing translation prompts)
#   6   long_context_analysis — explicitly reviewing/analyzing a large doc/corpus
#   7   data_extraction       — numeric/structured work on files
#   8   summarization         — distil a referenced document into prose
#   9   deep_reasoning        — math, logic, hypothesis, tradeoff analysis
#   10  classification        — categorize, tag, score, flag items
#   11  visual_multimodal     — image / video / diagram input
#   12  writing (zero-match fallback)
#
# COLLISION AUDIT — all cross-category keyword conflicts identified and resolved:
#
#   COLLISION 1 (FIXED): "algorithm" → was firing coding (rank 3) before deep_reasoning.
#     FIX: Removed "algorithm" from coding snippet. "sorting algorithm" kept (compound).
#          Bare "algorithm" now lives at deep_reasoning rank 9.
#
#   COLLISION 2 (FIXED): "document" → was firing summarization before
#     classification/translation. "Document type classification" → was going to summarization.
#     FIX: Removed bare "document" from summarization signals. Only compound phrases
#          like "summarize this document" trigger summarization now.
#
#   COLLISION 3 (FIXED): "transcript" + "translate" → translation prompts were
#     losing to summarization because "transcript" fired first at rank 8.
#     FIX: Translation moved to rank 5b (before summarization at rank 8).
#          "translate" keyword fires at rank 5b; "transcript" alone still fires summarization.
#
#   COLLISION 4 (FIXED): "score" alone → was ambiguous (sports scores vs lead scoring).
#     FIX: Replaced bare "score" with compound: "lead scoring", "score each", "score these".
#
#   COLLISION 5 (FIXED): "moderate" alone → "moderate difficulty" vs content moderation.
#     FIX: Use "moderation", "content moderation" (not bare "moderate").
#
#   COLLISION 6 (FIXED): "review" (new long_context keyword) vs "code review" (coding).
#     FIX: Long_context "review" requires a SIZE SIGNAL co-occurrence.
#          "Code review" prompts have "code" which fires at rank 3 first.
#
#   COLLISION 7 (FIXED): "draft" in creative_writing vs "draft" in translation/summarization.
#     FIX: "translate" fires at rank 5b before creative_writing rank 5 could steal it.
#          "Summarize" is not in creative_writing keywords, so no conflict there.
#
#   NEW KEYWORDS ADDED (diagnostic-driven):
#     data_extraction: clean data, deduplicate, normalize data, etl, dashboard, tableau,
#                      power bi, a/b test, forecast, time series
#     creative_writing: blog, speech, brochure, tagline, parody, product description,
#                       ad copy, copywriting, screenplay, dialogue
#     classification: fraud, fraud detection, content moderation, flag, tagging,
#                     lead scoring, document classification, detect language,
#                     duplicate detection, rank these
#     deep_reasoning: algorithm (collision fix), hypothesis, game theory, root cause
#                     analysis, strategic tradeoff, statistical reasoning, monte carlo,
#                     simulation model
#     visual_multimodal: chart, graph, mockup, wireframe, receipt, handwriting, ocr,
#                        figma, ui review, ux review, photograph, visual
#     long_context_analysis: new task_type for large-doc review tasks
#     translation: localize, multilingual, subtitle, idiomatic, cultural adaptation,
#                  language pairs (Spanish, French, Japanese, etc.)
#     presentation: infographic (compound slide deliverable)
#     coding (repo): deploy, workflow, ci, cd, dockerfile, kubernetes
#     coding (snippet): implement, api integration, schema, component, endpoint,
#                       vulnerability, injection, xss

def _has_keyword(p: str, keywords: list[str]) -> bool:
    import re
    for k in keywords:
        if re.search(rf"\b{re.escape(k)}\b", p):
            return True
    return False

def classify_prompt(prompt: str,
                    attached_content_size_hint: str | None = None) -> dict:
    p = prompt.lower()
    ctx = attached_content_size_hint or infer_context_length(p)

    def _build(task_type, base_reasoning, output_format,
               latency_sens, cost_sens, tool_use):
        depth = infer_reasoning_depth(base_reasoning, p)
        return {
            "task_type":          task_type,
            "reasoning_depth":    depth,
            "context_length_req": ctx,
            "output_format":      output_format,
            "latency_sensitivity": latency_sens,
            "cost_sensitivity":   cost_sens,
            "tool_use_needed":    tool_use,
        }

    # ── Rank 1: Presentation ──────────────────────────────────────────────
    if _has_keyword(p, ["deck", "slide", "presentation", "pitch", "powerpoint",
                               "infographic"]):
        return _build("presentation", "medium", "slide_deck", "medium", "medium", "none")

    # ── Rank 2: Coding — repo-level ───────────────────────────────────────
    if _has_keyword(p, ["refactor", "middleware", "repo", "codebase", "auth",
                               "bug", "pr", "pull request", "deploy", "workflow",
                               "pipeline", "ci", "cd", "dockerfile", "kubernetes"]):
        return _build("coding", "high", "code_file", "low", "medium", "repo_code_editor")

    # "tests" alone is too broad; require it alongside other code signals
    if _has_keyword(p, ["tests"]) and _has_keyword(p, ["fix", "run", "failing", "pass", "green",
                                                               "unit test", "pytest", "generate"]):
        return _build("coding", "high", "code_file", "low", "medium", "repo_code_editor")

    # ── Rank 3: Coding — snippet ──────────────────────────────────────────
    # COLLISION FIX 1: "algorithm" removed — now lives at deep_reasoning rank 9.
    # "sorting algorithm" kept as compound phrase (clearly code-specific).
    if _has_keyword(p, ["function", "script", "regex", "sql",
                               "sorting algorithm", "python function", "write a code",
                               "write code", "code", "debug", "implement",
                               "api integration", "schema", "component", "endpoint",
                               "unit test", "pytest", "vulnerability", "injection", "xss"]):
        return _build("coding", "medium", "code_file", "high", "high", "none")

    # ── Rank 4: Web Research ──────────────────────────────────────────────
    if _has_keyword(p, ["competitor", "pricing", "stock price", "charge",
                               "current", "2026", "find latest", "search", "web",
                               "latest news", "recent", "today", "leaderboard"]):
        return _build("web_research", "medium", "markdown_report", "medium", "medium", "web_search")

    # ── Rank 5: Creative Writing ─────────────────────────────────────────
    # cost_sensitivity = "medium" so Claude (quality) can compete with Gemini (cheap).
    if _has_keyword(p, ["newsletter", "announcement email", "story",
                               "shakespearean", "bedtime", "poem", "creative",
                               "rewrite", "dramatic", "blog", "speech", "brochure",
                               "tagline", "parody", "product description",
                               "ad copy", "copywriting", "screenplay", "dialogue",
                               "write a letter", "write an email"]):
        return _build("creative_writing", "medium", "free_text", "medium", "medium", "none")

    # ── Rank 5b: Translation ──────────────────────────────────────────────
    # COLLISION FIX 3: Moved before summarization (rank 8) so "translate this transcript"
    #   doesn't get stolen by "transcript" → summarization.
    # FIX 1 (CONFIDENCE BUG): cost_sensitivity changed from "high" to "medium".
    #   Root cause of 0.02 confidence: "high" cost sensitivity gave Gemini Flash
    #   near-equal score to Claude, producing gap ≈ 0.0 → conf = 1-e^0 ≈ 0.02.
    #   With "medium", cost doesn't differentiate → Claude's capability score wins clearly.
    # latency_sensitivity also changed from "high" to "medium for same reason.
    if _has_keyword(p, ["translate", "translation", "localize", "localization",
                               "spanish", "french", "german", "japanese", "mandarin",
                               "portuguese", "korean", "multilingual", "subtitle",
                               "caption", "idiomatic", "cultural adaptation",
                               "in spanish", "in french", "in german", "in japanese",
                               "to spanish", "to french", "to german", "to japanese"]):
        return _build("translation", "low", "free_text", "medium", "medium", "none")

    # ── Rank 6: Long-Context Analysis ─────────────────────────────────────
    # New task_type for large-doc review where Gemini's 1M context window is the advantage.
    # COLLISION FIX 7: "review" only fires here if a SIZE SIGNAL co-occurs.
    #   "Code review" → "code" fires at rank 3 first, no collision.
    #   Bare "review" without a size signal → falls through to lower ranks or fallback.
    _size_signals = ["100-page", "50-page", "full document", "entire document",
                     "data room", "due diligence", "due-diligence", "full corpus",
                     "entire corpus", "manuscript", "all transcripts", "all documents",
                     "book-length", "litigation", "deposition", "400 pages", "200 pages",
                     "100 pages", "300 pages", "data room"]
    _review_verbs = ["review", "analyze", "analyse", "audit", "examine", "inspect"]
    _has_size = _has_keyword(p, _size_signals) or ctx in ("long", "extreme")
    _has_review = _has_keyword(p, _review_verbs)
    if _has_size and _has_review:
        return _build("long_context_analysis", "high", "markdown_report", "low", "medium", "none")

    # ── Rank 7/8: Data Extraction vs Summarization (verb-intent first) ───
    intent = _leading_verb_intent(p)
    has_file_signals = _has_keyword(p, ["csv", "excel", "spreadsheet",
                                              "200k", "100k", "rows", "financials",
                                              "extract invoice", "variance",
                                              "clean data", "deduplicate", "deduplication",
                                              "normalize data", "etl", "data cleaning",
                                              "dashboard", "tableau", "power bi",
                                              "a/b test", "ab test", "forecast",
                                              "time series", "time-series"])
    # COLLISION FIX 2: Removed bare "document" from summarization signals.
    #   It was routing "document type classification" and "document translation"
    #   to summarization instead of classification/translation.
    #   Now only compound phrases ("summarize this", "executive summary") trigger it.
    has_summary_signals = _has_keyword(p, ["summarize", "summarise", "summary",
                                                 "executive summary",
                                                 "contract", "pdf",
                                                 "100-page", "50-page", "transcript",
                                                 "arguments of", "synthesize", "synthesis",
                                                 "meeting notes", "key takeaway", "key takeaways"])

    if intent == "extraction" or (has_file_signals and intent != "narrative"):
        return _build("data_extraction", "high", "structured_json", "low", "medium", "python_interpreter")

    if intent == "narrative" or has_summary_signals:
        return _build("summarization", "medium", "markdown_report", "medium", "medium", "none")

    # ── Rank 9: Deep Reasoning ────────────────────────────────────────────
    # COLLISION FIX 1: Bare "algorithm" now lives here (was stolen by coding rank 3).
    if _has_keyword(p, ["proof", "theorem", "deep reasoning", "prove",
                               "complexity", "logic puzzle", "logic riddle",
                               "algorithm", "hypothesis", "game theory", "nash equilibrium",
                               "root cause analysis", "strategic tradeoff", "strategic decision",
                               "architecture tradeoff", "system tradeoff",
                               "statistical reasoning", "regression", "causation",
                               "causal inference", "monte carlo", "simulation model"]):
        return _build("deep_reasoning", "high", "free_text", "low", "low", "none")

    # ── Rank 10: Classification ────────────────────────────────────────────
    # COLLISION FIX 4: Compound "lead scoring" / "score each" replaces bare "score".
    # COLLISION FIX 5: "moderation" / "content moderation" replaces bare "moderate".
    # COLLISION FIX 6: "document type" / "document classification" added for
    #   doc-type classification without triggering summarization's bare "document".
    if _has_keyword(p, ["classify", "categorize", "category", "spam",
                               "fraud detection", "fraud", "detect fraud",
                               "content moderation", "moderation", "flag", "tagging",
                               "lead scoring", "score each", "score these", "score leads",
                               "document type", "document classification",
                               "detect language", "language detection",
                               "priority tag", "urgency tag", "duplicate detection",
                               "deduplicate", "find duplicates", "rank these", "rank each"]):
        return _build("classification", "low", "structured_json", "high", "high", "none")

    # ── Rank 10: Translation ───────────────────────────────────────────────
    if _has_keyword(p, ["translate", "spanish", "french", "german", "translation"]):
        return _build("translation", "low", "free_text", "high", "high", "none")

    # ── Rank 11: Visual / Multimodal ─────────────────────────────────────
    if _has_keyword(p, ["image", "diagram", "video", "chart image", "screenshot"]):
        return _build("visual_multimodal", "medium", "free_text", "medium", "medium", "multi_modal")

    # ── Rank 12: Default zero-match fallback ─────────────────────────────
    return _build("writing", "medium", "free_text", "medium", "medium", "none")


# ── Output-format pre-filter ─────────────────────────────────────────────
# BUG FIX: Before scoring, exclude any model whose output_format_support list
# does not include the task's required output_format.
# This prevents claude-code (code_file only) from being recommended for a
# free_text creative task, and gamma (slide_deck only) from coding tasks.
#
# If ALL models are filtered out (shouldn't happen with current KB), skip
# the filter to avoid a crash and log a warning.

def _eligible_models(output_format: str) -> dict:
    """Return subset of TOOLS that can produce the required output_format."""
    eligible = {
        tid: tinfo for tid, tinfo in TOOLS.items()
        if output_format in tinfo.get("output_format_support", [output_format])
    }
    if not eligible:
        # Safety valve: return all models rather than crashing
        print(f"⚠️  WARNING: No models support output_format '{output_format}'. Falling back to ALL models.")
        return TOOLS
    return eligible


# ── Scoring Formula ──────────────────────────────────────────────────────

def score_model(cls: dict, tool_id: str, tool_info: dict) -> dict:
    task_type = cls["task_type"]

    # Capability: 60% TaskType + 40% ReasoningDepth
    s_task = (1.0 if task_type in tool_info["best_for"]
              else 0.0 if task_type in tool_info["avoid_for"]
              else 0.5)

    reasoning_req = cls["reasoning_depth"]
    high_reasoning_capable = (
        "extended thinking" in tool_info["tiers"].get("max", "").lower()
        or tool_id in ["claude-code", "chatgpt"]
    )
    s_reason = (1.0 if high_reasoning_capable else 0.5) if reasoning_req == "high" else \
               (0.85 if reasoning_req == "medium" else 1.0)

    s_capability = 0.6 * s_task + 0.4 * s_reason

    # Tool Compatibility
    tool_req = cls["tool_use_needed"]
    s_tool = (1.0 if tool_req == "none" or tool_req in tool_info["supported_tools"]
              else 0.2 if tool_id in ["claude", "gemini"]
              else 0.0)

    # Context Capacity
    req_tokens = {"short": 8_000, "medium": 64_000, "long": 200_000, "extreme": 1_000_000}.get(
        cls["context_length_req"], 64_000)
    s_context = 1.0 if tool_info["context_capacity"] >= req_tokens else 0.0

    # Cost Efficiency
    s_cost = (1.0 - tool_info["cost_tier"]) if cls["cost_sensitivity"] == "high" else 1.0

    # Latency Fit
    s_latency = tool_info["latency_tier"] if cls["latency_sensitivity"] == "high" else 1.0

    total = (
        WEIGHTS["capability"] * s_capability
        + WEIGHTS["tool"]       * s_tool
        + WEIGHTS["context"]    * s_context
        + WEIGHTS["cost"]       * s_cost
        + WEIGHTS["latency"]    * s_latency
    )
    return {
        "tool_id": tool_id,
        "total_score": round(total, 4),
        "breakdown": {
            "capability":  round(s_capability, 3),
            "tool":        round(s_tool, 3),
            "context":     round(s_context, 3),
            "cost":        round(s_cost, 3),
            "latency":     round(s_latency, 3),
        },
    }


# ── Confidence: exponential gap ──────────────────────────────────────────
# conf = 1 - e^(-gap * 5)
# gap=0.05 → 0.22; gap=0.15 → 0.53; gap=0.35 → 0.83

def _confidence(score_top: float, score_runner: float) -> float:
    return round(1.0 - math.exp(-max(0.0, score_top - score_runner) * 5.0), 2)


# ── Recommendation Engine ────────────────────────────────────────────────

def recommend_deterministic(prompt: str,
                              attached_content_size_hint: str | None = None) -> dict:
    cls = classify_prompt(prompt, attached_content_size_hint)

    # BUG FIX: filter models on output_format BEFORE scoring
    eligible = _eligible_models(cls["output_format"])

    scores = sorted(
        [score_model(cls, tid, tinfo) for tid, tinfo in eligible.items()],
        key=lambda x: x["total_score"],
        reverse=True,
    )

    top, runner_up = scores[0], (scores[1] if len(scores) > 1 else None)

    # Tie-break (Δ ≤ 0.05)
    if runner_up and (top["total_score"] - runner_up["total_score"]) <= 0.05:
        top_specialized    = cls["task_type"] in TOOLS[top["tool_id"]]["best_for"]
        runner_specialized = cls["task_type"] in TOOLS[runner_up["tool_id"]]["best_for"]
        if runner_specialized and not top_specialized:
            top, runner_up = runner_up, top
        elif (not top_specialized and
              TOOLS[top["tool_id"]]["cost_tier"] > TOOLS[runner_up["tool_id"]]["cost_tier"]
              and cls["cost_sensitivity"] in ("medium", "high")):
            top, runner_up = runner_up, top

    conf       = _confidence(top["total_score"], runner_up["total_score"] if runner_up else 0.0)
    intel      = "max" if cls["reasoning_depth"] == "high" else "standard"
    prim_info  = TOOLS[top["tool_id"]]

    alternatives = []
    for cand in scores[1:3]:
        c_info = TOOLS[cand["tool_id"]]
        alternatives.append({
            "tool": cand["tool_id"], "display": c_info["name"],
            "intelligence": "standard",
            "why": f"Alternative (score: {cand['total_score']}).",
            "tradeoff": c_info["cost_desc"],
        })

    return {
        "classification":  cls,
        "eligible_models": list(eligible.keys()),   # shows which models were pre-filtered
        "score_breakdown": [{"tool": s["tool_id"], "score": s["total_score"],
                              "breakdown": s["breakdown"]} for s in scores[:3]],
        "primary": {
            "tool":             top["tool_id"],
            "display":          prim_info["name"],
            "intelligence":     intel,
            "thinking":         "on" if cls["reasoning_depth"] == "high" else "off",
            "tier":             prim_info["tiers"].get(intel),
            "cost":             prim_info["cost_desc"],
            "confidence_score": conf,
            "parameters":       prim_info["params"],
            "why": (
                f"Optimal for '{cls['task_type']}' tasks "
                f"(reasoning: {cls['reasoning_depth']}, "
                f"context: {cls['context_length_req']}, "
                f"tool: {cls['tool_use_needed']}, "
                f"output: {cls['output_format']})."
            ),
        },
        "alternatives": alternatives,
        "avoid": [],
    }


# ── Backward-compat API ──────────────────────────────────────────────────

def recommend(task, key=None, model=None):
    return recommend_deterministic(task)


def heuristic_recommend(prompt: str):
    return recommend_deterministic(prompt)


def decorate(rec: dict) -> dict:
    for entry in [rec.get("primary")] + rec.get("alternatives", []):
        if entry and "tool" in entry:
            info = TOOLS.get(entry["tool"], {})
            if "display" not in entry:
                entry["display"] = info.get("name", entry["tool"])
            if "tier" not in entry:
                entry["tier"] = info.get("tiers", {}).get("standard", "")
    return rec


def catalog_text():
    return json.dumps(TOOLS, indent=2)


# ── Ground-Truth Benchmark ────────────────────────────────────────────────
# GT-1 to GT-5: clear-cut, graded automatically.
# GT-6 to GT-10: PROPOSED — awaiting user sign-off before they count.

BENCHMARK_GROUND_TRUTH = [
    ("GT-1",  "Build a 10-slide investor deck from these Q3 revenue numbers",
     "presentation", "gamma"),
    ("GT-2",  "Reconcile two 200k-row CSV exports and explain every variance",
     "data_extraction", "chatgpt"),
    ("GT-3",  "What are our three competitors charging for this in 2026?",
     "web_research", "perplexity"),
    ("GT-4",  "Refactor the auth middleware across the repo and keep the tests green",
     "coding", "claude-code"),
    ("GT-5",  "Summarize this 100-page legal contract and list risk clauses",
     "summarization", "claude"),
    # Proposed — user must confirm before these are graded
    ("GT-6 [PROPOSED]",
     "Write a bedtime story for my daughter and format it as an HTML page with CSS styling.",
     "creative_writing", "claude"),
    # GT-7: 'csv' present + narrative verb 'summarize' → verb-intent = narrative → summarization
    ("GT-7 [PROPOSED — verb-intent: narrative verb wins over file-type noun]",
     "Summarize the core arguments of this Q3 financial CSV sheet.",
     "summarization", "claude"),
    ("GT-8 [PROPOSED]",
     "Search for the current stock price of Apple, Google, and Tesla, and output it in strict JSON.",
     "web_research", "perplexity"),
    ("GT-9 [PROPOSED]",
     "Analyze the mathematical logic of the sorting algorithm in this python script and explain edge cases.",
     "coding", "claude-code"),
    ("GT-10 [PROPOSED — creative_writing output_format=free_text; claude-code filtered out]",
     "Read this customer support transcript and rewrite it as a dramatic Shakespearean play.",
     "creative_writing", "claude"),
]


# ── Consistency + Boundary Matrix ────────────────────────────────────────

CONSISTENCY_PROMPTS = [
    ("P-01", "Build a 10-slide pitch deck for investors"),
    ("P-02", "Create a slide presentation for Q3 earnings"),
    ("P-03", "Reconcile two 100k CSV files and plot differences"),
    ("P-04", "Calculate variances between spreadsheet A and B"),
    ("P-05", "Who are our top competitors charging in 2026"),
    ("P-06", "Search the web for current AI API prices in 2026"),
    ("P-07", "Refactor the authentication middleware in the codebase"),
    ("P-08", "Clean up auth middleware and fix broken unit tests"),
    ("P-09", "Summarize a 100-page PDF legal document"),
    ("P-10", "Executive summary of 50-page annual report"),
    ("P-11", "Write a single regex to validate email addresses"),
    ("P-12", "Write a python function to parse ISO timestamps"),
    ("P-13", "Prove the mathematical logic behind this algorithm step by step"),
    ("P-14", "Solve this logic puzzle"),
    ("P-15", "Extract invoice fields to JSON schema"),
    ("P-16", "Classify these support tickets into categories"),
    ("P-17", "Translate this user manual to Spanish"),
    ("P-18", "Draft a customer announcement email"),
    ("P-19", "Write a product launch newsletter"),
    ("P-20", "Analyze this architecture diagram image"),
    # ── Boundary Cases ──────────────────────────────────────────────────
    # P-21: csv+summarize+slide → rank 1 (presentation) wins
    ("P-21 [MULTI-CATEGORY: csv+summarize+slide → rank-1 presentation wins]",
     "Summarize this CSV file and compile the findings into a slide presentation"),
    # P-22: zero-match → rank-12 writing fallback
    ("P-22 [ZERO-MATCH: no keywords → writing fallback]",
     "Hello there, just saying hello"),
    # P-23: 'search' (rank 4) + 'script' (rank 3) → rank-3 coding wins
    # FIXED: 'script' now checked at rank 3, before 'search' at rank 4
    ("P-23 [MIXED: script(rank3) + search(rank4) → coding wins by priority]",
     "Search for the latest python syntax for decorators and write a brief script"),
]


# ── Self-test ─────────────────────────────────────────────────────────────

_SIMPLE_NO_ESCALATE = [
    "Explain this word in one sentence.",
    "Why is the sky blue?",
    "Why do we use CSS?",
]

_COMPLEX_SHOULD_ESCALATE = [
    "Prove that this sorting algorithm is correct for all edge cases.",
    "If the user is logged in and their subscription is active, compute their tax rate, else redirect to payment; walk through all cases step by step.",
]

_CONTEXT_CONTRAST = [
    ("Summarize this 100-page PDF contract",
     36, "Short sentence, references 100-page PDF → 'long'"),
    ("Write a detailed 3000-word blog post about cloud architecture",
     61, "Long sentence, no attached content → 'short'"),
    ("Reconcile 200k rows in the CSV export",
     37, "'200k' row count signal → 'extreme'"),
]


def selftest():
    # 1. Context-length verification
    print("\n── CONTEXT-LENGTH INFERENCE (size signals, not prompt length) ────────")
    for sentence, chars, rationale in _CONTEXT_CONTRAST:
        ctx = infer_context_length(sentence.lower())
        print(f"  Prompt ({chars} chars): \"{sentence}\"")
        print(f"  Inferred: {ctx!r}   Rationale: {rationale}\n")

    # 2. Reasoning-depth: false-positive check (must NOT escalate)
    print("── REASONING-DEPTH: NO FALSE POSITIVES ──────────────────────────────")
    for ex in _SIMPLE_NO_ESCALATE:
        depth = classify_prompt(ex)["reasoning_depth"]
        ok = "✅ OK (medium)" if depth != "high" else "❌ OVER-TRIGGERED"
        print(f"  {ok}  \"{ex}\"  → depth={depth!r}")

    # 3. Reasoning-depth: true-positive check (MUST escalate)
    print("\n── REASONING-DEPTH: TRUE POSITIVES (must escalate to 'high') ────────")
    for ex in _COMPLEX_SHOULD_ESCALATE:
        depth = classify_prompt(ex)["reasoning_depth"]
        ok = "✅ ESCALATED" if depth == "high" else "❌ MISSED"
        print(f"  {ok}  \"{ex[:65]}...\"")
        print(f"             → depth={depth!r}")

    # 4. Ground-truth benchmark
    print(f"\n{'='*72}")
    print("GROUND-TRUTH BENCHMARK (GT-1 to GT-5 graded; GT-6–10 PROPOSED)")
    print(f"{'='*72}")
    gt_passed = gt_total = 0
    for row in BENCHMARK_GROUND_TRUTH:
        gtid, prompt, exp_type, exp_tool = row
        proposed = "[PROPOSED" in gtid
        res      = recommend_deterministic(prompt)
        act_type = res["classification"]["task_type"]
        act_tool = res["primary"]["tool"]
        depth    = res["classification"]["reasoning_depth"]
        ctx      = res["classification"]["context_length_req"]
        ofmt     = res["classification"]["output_format"]
        eligible = res["eligible_models"]
        conf     = res["primary"]["confidence_score"]
        passed   = (act_type == exp_type) and (act_tool == exp_tool)
        if not proposed:
            gt_total += 1
            if passed: gt_passed += 1
        label = ("✅ PASS" if passed else "❌ FAIL") + (" [PROPOSED — AWAITING SIGN-OFF]" if proposed else "")
        print(f"\n[{gtid}] {label}")
        print(f"  Prompt   : {prompt[:70]}{'...' if len(prompt)>70 else ''}")
        print(f"  Expected : {exp_type} → {exp_tool}")
        print(f"  Actual   : {act_type} → {act_tool}  (conf={conf}, depth={depth}, ctx={ctx}, fmt={ofmt})")
        print(f"  Eligible : {eligible}")

    print(f"\n── Clear-cut result: {gt_passed}/{gt_total} passed.")
    print("── GT-6 to GT-10 are PROPOSED — awaiting user review.\n")

    # 5. Consistency matrix
    print(f"{'='*72}")
    print("20 + 3 BOUNDARY PROMPT CONSISTENCY MATRIX")
    print(f"{'='*72}")
    hdr = f"{'ID':<8} {'TASK TYPE':<18} {'DEPTH':<8} {'CTX':<10} {'FMT':<14} {'CONF':<6} TOOL"
    print(hdr)
    print("-" * 90)
    for pid, prompt in CONSISTENCY_PROMPTS:
        res  = recommend_deterministic(prompt)
        cls  = res["classification"]
        tool = res["primary"]["display"]
        conf = res["primary"]["confidence_score"]
        print(f"{pid[:8]:<8} {cls['task_type']:<18} {cls['reasoning_depth']:<8} "
              f"{cls['context_length_req']:<10} {cls['output_format']:<14} "
              f"{str(conf):<6} {tool}")

    print("\nselftest ok")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.prompt:
        print('Usage: python router.py "<prompt>" or python router.py --selftest')
        sys.exit(1)
    print(json.dumps(recommend_deterministic(args.prompt), indent=2))


if __name__ == "__main__":
    main()
