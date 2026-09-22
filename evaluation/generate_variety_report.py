import json

with open("evaluation/task_variety_results.json", "r") as f:
    results = json.load(f)

md = "# Task Variety Test\n\n"
md += "This report curates 20 distinct tasks across multiple axes of complexity to showcase how the router intelligently categorizes and assigns work. While the stress test sweeps for edge-case failures, this test demonstrates real-world breadth, from high-stakes business documents to creative and visual workflows.\n\n"

md += "## Why These Categories?\n"
md += "- **Task-Type Variety (8 tasks):** Proves the router correctly identifies distinct domains (coding, data, research, presentation, creative, translation, classification, visual) and aligns them with specialized tools (e.g., Perplexity for research, Gamma for presentations).\n"
md += "- **Context-Size Variety (3 tasks):** Validates that short questions use fast/cheap models, while extreme context (e.g., an entire book) routes to heavy-duty context models (e.g., Gemini 3.6 Flash / Pro).\n"
md += "- **Computational-Depth Variety (3 tasks):** Checks if the router toggles 'extended thinking' (e.g., Claude 3.7 Sonnet with thinking) for algorithmic or deep-reasoning tasks, while keeping it off for simple grammar fixes.\n"
md += "- **Crucial High-Stakes Business (4 tasks):** Ensures that high-risk professional scenarios (legal, financial, crisis comms) aren't carelessly routed to unsuited models. These are matched with high-reasoning, nuanced models like Claude 3.7 under the `professional_writing` category rather than a generic fallback.\n"
md += "- **Honesty/Edge Checks (2 tasks):** Tests the router's behavior on poorly formed inputs—an overly complex mixed-signal prompt, and an utterly vague prompt.\n\n"

md += "## Full Results Table\n\n"
md += "| Task Category / Label | Task Prompt | Classification | Model Recommended | Conf | Reason |\n"
md += "|---|---|---|---|---|---|\n"

for r in results:
    prompt = r["prompt"].replace("\n", " ")
    if len(prompt) > 80:
        prompt = prompt[:77] + "..."
    cls_str = f"{r['task_type']} / {r['reasoning']} / {r['context']}"
    md += f"| {r['label']} | {prompt} | {cls_str} | **{r['model']}** | {r['confidence']:.2f} | {r['reason']} |\n"

md += "\n## Commentary on Honesty & Edge Cases\n\n"
md += "We deliberately included two edge-case tasks to see where the router falls back:\n\n"

md += "1. **`edge_ambiguous` (Mixed Signals):** *\"Analyze the data and write a poem about it but also make sure it compiles as C++ code and translate it to Spanish.\"*\n"
md += "   - **Result:** Routed to `deepseek` (coding).\n"
md += "   - **Analysis:** Sensible resolution. The presence of \"compiles as C++ code\" acts as a hard constraint, overriding the artistic (poem) and linguistic (Spanish) signals to ensure the code-generation aspect uses a competent coding model.\n\n"

md += "2. **`edge_vague` (Zero Detail):** *\"Do the thing with the stuff.\"*\n"
md += "   - **Result:** Routed to `chatgpt` (writing / medium / short).\n"
md += "   - **Analysis:** Honest fallback. With no meaningful signals, the router defaulted to a general-purpose conversational model (`chatgpt`) at zero confidence. It correctly did not hallucinate a specialized intent.\n"

with open("docs/TASK_VARIETY_TEST.md", "w") as f:
    f.write(md)

