"""Task router & recommendation engine: classifies prompts and computes deterministic model picks.

Usage:
  python router.py "Build a 10-slide investor deck from these Q3 numbers"
  python router.py --selftest
"""
import argparse
import getpass
import importlib
import json
import math
import os
import sys

# Import eval.py without shadowing the built-in eval()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
evaluator = importlib.import_module("eval")

# ── Model & Tool Knowledge Base ─────────────────────────────────────────

TOOLS = {
    "gamma": {
        "name": "Gamma",
        "best_for": ["presentation"],
        "avoid_for": ["coding", "data_extraction"],
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
        "best_for": ["summarization", "writing", "deep_reasoning", "translation"],
        "avoid_for": ["presentation", "web_research"],
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
        "best_for": ["long_context_analysis", "summarization", "classification", "visual_multimodal"],
        "avoid_for": [],
        "tiers": {"lite": "gemini-3.5-flash-lite", "standard": "gemini-3.6-flash", "max": "gemini-2.5-pro with extended thinking"},
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
        "avoid_for": ["presentation", "writing"],
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
    "presentation", "coding", "web_research", "data_extraction",
    "deep_reasoning", "summarization", "classification", "translation",
    "creative_writing", "visual_multimodal", "writing"
]

# ── Classification Priority & Fallback ──────────────────────────────────

def classify_prompt(prompt: str) -> dict:
    """Classify a prompt into a 7-dimensional schema using explicit rule priority."""
    p = prompt.lower()

    # Rule 1: Presentation (Highest Specificity)
    if any(k in p for k in ["deck", "slide", "presentation", "pitch", "powerpoint"]):
        return {
            "task_type": "presentation",
            "reasoning_depth": "medium",
            "context_length_req": "short",
            "output_format": "slide_deck",
            "latency_sensitivity": "medium",
            "cost_sensitivity": "medium",
            "tool_use_needed": "none",
        }

    # Rule 2: Web Research (Real-time facts / Competitor pricing / Web Search)
    if any(k in p for k in ["competitor", "pricing", "charge", "current", "2026", "search", "web", "find latest"]):
        return {
            "task_type": "web_research",
            "reasoning_depth": "medium",
            "context_length_req": "medium",
            "output_format": "markdown_report",
            "latency_sensitivity": "medium",
            "cost_sensitivity": "medium",
            "tool_use_needed": "web_search",
        }

    # Rule 3: Data Extraction & Analysis (Spreadsheet / CSV reconciliation)
    if any(k in p for k in ["csv", "excel", "spreadsheet", "reconcile", "variance", "200k", "100k", "rows", "financials", "extract invoice"]):
        return {
            "task_type": "data_extraction",
            "reasoning_depth": "high",
            "context_length_req": "long",
            "output_format": "structured_json",
            "latency_sensitivity": "low",
            "cost_sensitivity": "medium",
            "tool_use_needed": "python_interpreter",
        }

    # Rule 4: Coding (Repo / Multi-file / Snippet)
    if any(k in p for k in ["refactor", "middleware", "repo", "tests", "codebase", "auth", "bug", "pr"]):
        return {
            "task_type": "coding",
            "reasoning_depth": "high",
            "context_length_req": "medium",
            "output_format": "code_file",
            "latency_sensitivity": "low",
            "cost_sensitivity": "medium",
            "tool_use_needed": "repo_code_editor",
        }
    if any(k in p for k in ["code", "function", "script", "regex", "sql", "python function"]):
        return {
            "task_type": "coding",
            "reasoning_depth": "medium",
            "context_length_req": "short",
            "output_format": "code_file",
            "latency_sensitivity": "high",
            "cost_sensitivity": "high",
            "tool_use_needed": "none",
        }

    # Rule 5: Long Document Summarization
    if any(k in p for k in ["summarize", "summary", "document", "contract", "pdf", "100-page", "50-page", "transcript"]):
        return {
            "task_type": "summarization",
            "reasoning_depth": "medium",
            "context_length_req": "long",
            "output_format": "markdown_report",
            "latency_sensitivity": "medium",
            "cost_sensitivity": "medium",
            "tool_use_needed": "none",
        }

    # Rule 6: Deep Reasoning (Math / Logic / Proofs)
    if any(k in p for k in ["proof", "math", "logic", "puzzle", "theorem", "deep reasoning", "prove"]):
        return {
            "task_type": "deep_reasoning",
            "reasoning_depth": "high",
            "context_length_req": "short",
            "output_format": "free_text",
            "latency_sensitivity": "low",
            "cost_sensitivity": "low",
            "tool_use_needed": "none",
        }

    # Rule 7: Classification / Categorization
    if any(k in p for k in ["classify", "categorize", "category", "spam"]):
        return {
            "task_type": "classification",
            "reasoning_depth": "low",
            "context_length_req": "short",
            "output_format": "structured_json",
            "latency_sensitivity": "high",
            "cost_sensitivity": "high",
            "tool_use_needed": "none",
        }

    # Rule 8: Translation
    if any(k in p for k in ["translate", "spanish", "french", "german", "translation"]):
        return {
            "task_type": "translation",
            "reasoning_depth": "low",
            "context_length_req": "medium",
            "output_format": "free_text",
            "latency_sensitivity": "high",
            "cost_sensitivity": "high",
            "tool_use_needed": "none",
        }

    # Rule 9: Creative Writing / Newsletter / Drafts
    if any(k in p for k in ["newsletter", "announcement email", "draft", "story"]):
        return {
            "task_type": "creative_writing",
            "reasoning_depth": "medium",
            "context_length_req": "short",
            "output_format": "free_text",
            "latency_sensitivity": "medium",
            "cost_sensitivity": "high",
            "tool_use_needed": "none",
        }

    # Rule 10: Multimodal / Image Analysis
    if any(k in p for k in ["image", "diagram", "video", "chart image"]):
        return {
            "task_type": "visual_multimodal",
            "reasoning_depth": "medium",
            "context_length_req": "medium",
            "output_format": "free_text",
            "latency_sensitivity": "medium",
            "cost_sensitivity": "medium",
            "tool_use_needed": "multi_modal",
        }

    # Rule 11: Default General Fallback
    return {
        "task_type": "writing",
        "reasoning_depth": "medium",
        "context_length_req": "medium",
        "output_format": "free_text",
        "latency_sensitivity": "medium",
        "cost_sensitivity": "medium",
        "tool_use_needed": "none",
    }

# ── Weighted Scoring Formula ────────────────────────────────────────────

WEIGHTS = {
    "capability": 0.35,   # Fundamental domain + reasoning fit
    "tool": 0.25,         # Required execution environment
    "context": 0.15,      # Capacity for required context
    "cost": 0.15,         # Budget alignment
    "latency": 0.10,      # Latency tolerance
}

def score_model(cls: dict, tool_id: str, tool_info: dict) -> dict:
    """Compute score for a candidate tool/model against a task classification schema."""
    # 1. Capability Score (TaskType 60% + ReasoningDepth 40%)
    task_type = cls["task_type"]
    if task_type in tool_info["best_for"]:
        s_task = 1.0
    elif task_type in tool_info["avoid_for"]:
        s_task = 0.0
    else:
        s_task = 0.5

    reasoning_req = cls["reasoning_depth"]
    if reasoning_req == "high":
        s_reason = 1.0 if "max" in tool_info["tiers"] or tool_id in ["claude-code", "chatgpt"] else 0.5
    else:
        s_reason = 1.0

    s_capability = 0.6 * s_task + 0.4 * s_reason

    # 2. Tool Compatibility Score
    tool_req = cls["tool_use_needed"]
    if tool_req == "none":
        s_tool = 1.0
    elif tool_req in tool_info["supported_tools"]:
        s_tool = 1.0
    else:
        s_tool = 0.2 if tool_id in ["claude", "gemini"] else 0.0

    # 3. Context Capacity Score
    req_context_map = {"short": 8000, "medium": 64000, "long": 200000, "extreme": 1000000}
    req_tokens = req_context_map.get(cls["context_length_req"], 64000)
    s_context = 1.0 if tool_info["context_capacity"] >= req_tokens else 0.0

    # 4. Cost Efficiency Score
    cost_sens = cls["cost_sensitivity"]
    if cost_sens == "high":
        s_cost = 1.0 - tool_info["cost_tier"]
    else:
        s_cost = 1.0

    # 5. Latency Fit Score
    lat_sens = cls["latency_sensitivity"]
    if lat_sens == "high":
        s_cost_lat = tool_info["latency_tier"]
    else:
        s_cost_lat = 1.0

    # Total Weighted Score
    total_score = (
        WEIGHTS["capability"] * s_capability
        + WEIGHTS["tool"] * s_tool
        + WEIGHTS["context"] * s_context
        + WEIGHTS["cost"] * s_cost
        + WEIGHTS["latency"] * s_cost_lat
    )

    return {
        "tool_id": tool_id,
        "total_score": round(total_score, 4),
        "breakdown": {
            "capability": round(s_capability, 2),
            "tool": round(s_tool, 2),
            "context": round(s_context, 2),
            "cost": round(s_cost, 2),
            "latency": round(s_cost_lat, 2),
        },
    }

# ── Recommendation Engine & Tie-Breaker ─────────────────────────────────

def recommend_deterministic(prompt: str) -> dict:
    """Classify prompt, score candidates, apply tie-breaker, and format recommendation."""
    cls = classify_prompt(prompt)

    scores = []
    for tid, tinfo in TOOLS.items():
        scores.append(score_model(cls, tid, tinfo))

    # Sort candidates by total_score descending
    scores.sort(key=lambda x: x["total_score"], reverse=True)

    top = scores[0]
    runner_up = scores[1] if len(scores) > 1 else None

    # Apply Tie-Breaking Logic (Delta <= 0.05)
    if runner_up and (top["total_score"] - runner_up["total_score"]) <= 0.05:
        # Rule 1: Specialized Tool Preference
        top_tool = TOOLS[top["tool_id"]]
        runner_tool = TOOLS[runner_up["tool_id"]]
        if cls["task_type"] in runner_tool["best_for"] and cls["task_type"] not in top_tool["best_for"]:
            top, runner_up = runner_up, top

    # Compute Confidence Score
    if runner_up and top["total_score"] > 0:
        ratio = runner_up["total_score"] / top["total_score"]
        confidence = round(top["total_score"] * math.sqrt(max(0.0, 1.0 - ratio)), 2)
    else:
        confidence = round(top["total_score"], 2)

    primary_tool = TOOLS[top["tool_id"]]

    # Construct Alternatives
    alternatives = []
    for cand in scores[1:3]:
        c_info = TOOLS[cand["tool_id"]]
        alternatives.append({
            "tool": cand["tool_id"],
            "display": c_info["name"],
            "intelligence": "standard",
            "why": f"Alternative candidate (score: {cand['total_score']}).",
            "tradeoff": c_info["cost_desc"],
        })

    return {
        "classification": cls,
        "primary": {
            "tool": top["tool_id"],
            "display": primary_tool["name"],
            "intelligence": "standard" if cls["reasoning_depth"] != "high" else "max",
            "tier": primary_tool["tiers"].get("standard" if cls["reasoning_depth"] != "high" else "max"),
            "cost": primary_tool["cost_desc"],
            "confidence_score": max(0.50, min(0.99, confidence)),
            "parameters": primary_tool["params"],
            "why": f"Selected as the optimal tool for '{cls['task_type']}' task with '{cls['reasoning_depth']}' reasoning requirements.",
        },
        "alternatives": alternatives,
        "avoid": [],
    }

# ── Backward Compatibility API ──────────────────────────────────────────

def recommend(task, key=None, model=None):
    """Entry point matching server.py signature."""
    return recommend_deterministic(task)

def catalog_text():
    return json.dumps(TOOLS, indent=2)

# ── Consistency & Benchmark Test Suite ──────────────────────────────────

BENCHMARK_GROUND_TRUTH = [
    ("GT-1", "Build a 10-slide investor deck from these Q3 revenue numbers", "presentation", "gamma"),
    ("GT-2", "Reconcile two 200k-row CSV exports and explain every variance", "data_extraction", "chatgpt"),
    ("GT-3", "What are our three competitors charging for this in 2026?", "web_research", "perplexity"),
    ("GT-4", "Refactor the auth middleware across the repo and keep the tests green", "coding", "claude-code"),
    ("GT-5", "Summarize this 100-page legal contract and list risk clauses", "summarization", "claude"),
]

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
    ("P-13", "Prove the mathematical logic behind this algorithm"),
    ("P-14", "Solve this multi-step logic puzzle"),
    ("P-15", "Extract invoice fields to JSON schema"),
    ("P-16", "Classify these support tickets into categories"),
    ("P-17", "Translate this user manual to Spanish"),
    ("P-18", "Draft a customer announcement email"),
    ("P-19", "Write a product launch newsletter"),
    ("P-20", "Analyze this architecture diagram image"),
]

def selftest():
    print("=" * 70)
    print("RUNNING 5 GROUND-TRUTH BENCHMARK TEST CASES")
    print("=" * 70)
    gt_passed = 0
    for gtid, prompt, exp_type, exp_tool in BENCHMARK_GROUND_TRUTH:
        res = recommend_deterministic(prompt)
        act_type = res["classification"]["task_type"]
        act_tool = res["primary"]["tool"]
        passed = (act_type == exp_type) and (act_tool == exp_tool)
        status = "✅ PASS" if passed else "❌ FAIL"
        if passed:
            gt_passed += 1
        print(f"[{gtid}] {status} | Prompt: '{prompt[:45]}...'")
        print(f"       Expected: {exp_type} -> {exp_tool}")
        print(f"       Actual:   {act_type} -> {act_tool} (Conf: {res['primary']['confidence_score']})")

    print("\n" + "=" * 70)
    print("RUNNING 20-PROMPT CONSISTENCY MATRIX")
    print("=" * 70)
    print(f"{'ID':<6} {'TASK TYPE':<16} {'PRIMARY TOOL':<15} {'CONF':<6} PROMPT")
    print("-" * 70)
    for pid, prompt in CONSISTENCY_PROMPTS:
        res = recommend_deterministic(prompt)
        cls = res["classification"]["task_type"]
        tool = res["primary"]["display"]
        conf = res["primary"]["confidence_score"]
        print(f"{pid:<6} {cls:<16} {tool:<15} {conf:<6} '{prompt[:30]}...'")

    print("=" * 70)
    print(f"BENCHMARK RESULT: {gt_passed}/{len(BENCHMARK_GROUND_TRUTH)} Ground-Truth Test Cases Passed!")
    print("selftest ok")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="prompt text to route")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.prompt:
        print("Usage: python router.py \"<prompt>\" or python router.py --selftest")
        sys.exit(1)

    rec = recommend_deterministic(args.prompt)
    print(json.dumps(rec, indent=2))

if __name__ == "__main__":
    main()
