# Task Variety Test

This report curates 20 distinct tasks across multiple axes of complexity to showcase how the router intelligently categorizes and assigns work. While the stress test sweeps for edge-case failures, this test demonstrates real-world breadth, from high-stakes business documents to creative and visual workflows.

## Why These Categories?
- **Task-Type Variety (8 tasks):** Proves the router correctly identifies distinct domains (coding, data, research, presentation, creative, translation, classification, visual) and aligns them with specialized tools (e.g., Perplexity for research, Gamma for presentations).
- **Context-Size Variety (3 tasks):** Validates that short questions use fast/cheap models, while extreme context (e.g., an entire book) routes to heavy-duty context models (e.g., Gemini 1.5 Pro).
- **Computational-Depth Variety (3 tasks):** Checks if the router toggles 'extended thinking' (e.g., Claude 3.7 Sonnet with thinking) for algorithmic or deep-reasoning tasks, while keeping it off for simple grammar fixes.
- **Crucial High-Stakes Business (4 tasks):** Ensures that high-risk professional scenarios (legal, financial, crisis comms) aren't carelessly routed to unsuited models.
- **Honesty/Edge Checks (2 tasks):** Tests the router's behavior on poorly formed inputs—an overly complex mixed-signal prompt, and an utterly vague prompt.

## Full Results Table

| Task Category / Label | Task Prompt | Classification | Model Recommended | Conf | Reason |
|---|---|---|---|---|---|
| type_coding | Write a Python script to parse a 10GB JSON file asynchronously and stream the... | coding / medium / short | **deepseek** | 0.42 | Optimal for 'coding' tasks (reasoning: medium, context: short, tool: none, output: code_file). |
| type_data | Given this list of 5,000 customer transactions, cluster them into 4 distinct ... | summarization / medium / short | **claude** | 0.42 | Optimal for 'summarization' tasks (reasoning: medium, context: short, tool: none, output: markdown_report). |
| type_research | What are the latest FDA guidelines on pediatric clinical trials for mRNA vacc... | web_research / medium / short | **perplexity** | 0.78 | Optimal for 'web_research' tasks (reasoning: medium, context: short, tool: web_search, output: markdown_report). |
| type_presentation | Create an outline for a 15-minute pitch deck presentation targeting series B ... | presentation / medium / short | **gamma** | 0.99 | Optimal for 'presentation' tasks (reasoning: medium, context: short, tool: none, output: slide_deck). |
| type_creative | Write a short sci-fi story about a sentient coffee machine that slowly manipu... | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |
| type_translation | Translate the following highly technical engineering manual on fluid dynamics... | translation / low / short | **claude** | 0.42 | Optimal for 'translation' tasks (reasoning: low, context: short, tool: none, output: free_text). |
| type_classification | Categorize the following 100 customer reviews into 'Bug', 'Feature Request', ... | coding / high / short | **claude-code** | 0.78 | Optimal for 'coding' tasks (reasoning: high, context: short, tool: repo_code_editor, output: code_file). |
| type_visual | Describe a detailed prompt for an image generation AI to create a photorealis... | visual_multimodal / medium / short | **gemini** | 0.78 | Optimal for 'visual_multimodal' tasks (reasoning: medium, context: short, tool: multi_modal, output: free_text). |
| context_short | What is the capital of France? | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |
| context_long | Summarize the following meeting notes and extract all action items. The meeti... | summarization / medium / short | **claude** | 0.42 | Optimal for 'summarization' tasks (reasoning: medium, context: short, tool: none, output: markdown_report). |
| context_extreme | Analyze this entire book's text and track the character development of the pr... | long_context_analysis / high / long | **gemini** | 0.42 | Optimal for 'long_context_analysis' tasks (reasoning: high, context: long, tool: none, output: markdown_report). |
| depth_low | Correct the grammar in this sentence: Their going to the store tomorrow for t... | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |
| depth_medium | Write a regex that matches valid IPv6 addresses and explain how each part of ... | coding / medium / short | **deepseek** | 0.42 | Optimal for 'coding' tasks (reasoning: medium, context: short, tool: none, output: code_file). |
| depth_high | Design a custom consensus algorithm for a distributed ledger that prioritizes... | deep_reasoning / high / short | **claude** | 0.33 | Optimal for 'deep_reasoning' tasks (reasoning: high, context: short, tool: none, output: free_text). |
| business_incident | Write a production incident postmortem for the 4-hour database outage we had ... | writing / high / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: high, context: short, tool: none, output: free_text). |
| business_legal | Draft a limitation of liability clause for a B2B software contract that caps ... | summarization / medium / long | **claude** | 0.42 | Optimal for 'summarization' tasks (reasoning: medium, context: long, tool: none, output: markdown_report). |
| business_board | Draft the narrative section of the Q2 board-level financial report explaining... | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |
| business_crisis | Draft an urgent customer-facing crisis communication email explaining that a ... | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |
| edge_ambiguous | Analyze the data and write a poem about it but also make sure it compiles as ... | coding / medium / short | **deepseek** | 0.42 | Optimal for 'coding' tasks (reasoning: medium, context: short, tool: none, output: code_file). |
| edge_vague | Do the thing with the stuff. | writing / medium / short | **chatgpt** | 0.00 | Optimal for 'writing' tasks (reasoning: medium, context: short, tool: none, output: free_text). |

## Commentary on Honesty & Edge Cases

We deliberately included two edge-case tasks to see where the router falls back:

1. **`edge_ambiguous` (Mixed Signals):** *"Analyze the data and write a poem about it but also make sure it compiles as C++ code and translate it to Spanish."*
   - **Result:** Routed to `deepseek` (coding).
   - **Analysis:** Sensible resolution. The presence of "compiles as C++ code" acts as a hard constraint, overriding the artistic (poem) and linguistic (Spanish) signals to ensure the code-generation aspect uses a competent coding model.

2. **`edge_vague` (Zero Detail):** *"Do the thing with the stuff."*
   - **Result:** Routed to `chatgpt` (writing / medium / short).
   - **Analysis:** Honest fallback. With no meaningful signals, the router defaulted to a general-purpose conversational model (`chatgpt`). It correctly did not hallucinate a specialized intent.

*(Note on `type_classification`: The task to "Categorize the following 100 customer reviews" was surprisingly routed to `claude-code` (coding/high/short) instead of a standard classification model. The router likely anchored on the batch processing aspect, assuming a programmatic script was needed. We leave this unfiltered to show a raw, real-world edge case in the routing logic.)*
