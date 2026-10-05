# Token Prediction: Prompts & Model Recommender Pre-Execution Estimates

This document records the exact test prompts submitted to the **Prompt Router & Model Recommender**, detailing the recommended model selection, effort level, extended thinking status, and the pre-execution predicted token envelope.

---

## 1. Summary of Prompts & Predicted Token Envelopes

| Task ID | Domain / Category | Task Prompt | Suggested Model | Effort Level | Extended Thinking | Predicted Input Tokens | Predicted Thinking Tokens | Predicted Output (Min / Exp / Max) | Predicted Total Tokens (Min / Exp / Max) |
|---|---|---|---|---|---|---|---|---|---|
| **TASK-1** | Coding & Automation | *Write a Python script to parse a 10GB JSON file asynchronously and stream results to PostgreSQL.* | **DeepSeek V4 (Flash / Pro)** | `medium` | `on` | `21` | `1,024` | 350 / **650** / 1,400 | 1,395 / **~1,695** / 2,445 |
| **TASK-2** | Summarization (Constraint) | *Summarize the key points of the 2026 EU AI Act compliance guidelines in 4 concise bullet points.* | **Perplexity Pro** | `medium` | `on` | `23` | `1,024` | 400 / **850** / 2,200 | 1,447 / **~1,897** / 3,247 |
| **TASK-3** | Web Research & Analysis | *What are the latest developments in generative AI hardware architecture in 2026?* | **Perplexity Pro** | `medium` | `on` | `16` | `1,024` | 400 / **850** / 2,200 | 1,440 / **~1,890** / 3,240 |
| **TASK-4** | Math & Computation | *Calculate the compound interest on $50,000 at 7.2% annual rate compounded monthly for 15 years.* | **ChatGPT (GPT-4o / GPT-5.1)** | `medium` | `on` | `27` | `1,024` | 100 / **350** / 850 | 1,151 / **~1,401** / 1,901 |
| **TASK-5** | Creative Writing (Constraint) | *Write a 300-word bedtime story about a friendly dragon who is afraid of the dark.* | **Claude 3.7 Sonnet** | `medium` | `on` | `22` | `1,024` | 319 / **399** / 498 | 1,365 / **~1,445** / 1,544 |

---

## 2. Detailed Task Specification & Recommender Output

### TASK-1: Coding & Automation
* **Prompt:** `"Write a Python script to parse a 10GB JSON file asynchronously and stream results to PostgreSQL."`
* **Inferred Classification:** `coding` / `code_file` / `medium` reasoning depth
* **Primary Recommendation:** DeepSeek V4 (Flash / Pro)
* **Effort Level:** `medium` | **Extended Thinking:** `on`
* **Predicted Token Bounds:**
  * Input Tokens ($T_{\text{in}}$): `21`
  * Thinking Tokens ($T_{\text{think}}$): `1,024`
  * Output Tokens ($T_{\text{out}}$): `350 (min)` / `650 (exp)` / `1,400 (max)`
  * **Total Predicted Tokens ($T_{\text{total}}$):** `1,395 (min)` / `~1,695 (expected)` / `2,445 (max)`

---

### TASK-2: Summarization (Constraint)
* **Prompt:** `"Summarize the key points of the 2026 EU AI Act compliance guidelines in 4 concise bullet points."`
* **Inferred Classification:** `web_research` / `markdown_report` / `medium` reasoning depth
* **Primary Recommendation:** Perplexity Pro
* **Effort Level:** `medium` | **Extended Thinking:** `on`
* **Predicted Token Bounds:**
  * Input Tokens ($T_{\text{in}}$): `23`
  * Thinking Tokens ($T_{\text{think}}$): `1,024`
  * Output Tokens ($T_{\text{out}}$): `400 (min)` / `850 (exp)` / `2,200 (max)`
  * **Total Predicted Tokens ($T_{\text{total}}$):** `1,447 (min)` / `~1,897 (expected)` / `3,247 (max)`

---

### TASK-3: Web Research & Analysis
* **Prompt:** `"What are the latest developments in generative AI hardware architecture in 2026?"`
* **Inferred Classification:** `web_research` / `markdown_report` / `medium` reasoning depth
* **Primary Recommendation:** Perplexity Pro
* **Effort Level:** `medium` | **Extended Thinking:** `on`
* **Predicted Token Bounds:**
  * Input Tokens ($T_{\text{in}}$): `16`
  * Thinking Tokens ($T_{\text{think}}$): `1,024`
  * Output Tokens ($T_{\text{out}}$): `400 (min)` / `850 (exp)` / `2,200 (max)`
  * **Total Predicted Tokens ($T_{\text{total}}$):** `1,440 (min)` / `~1,890 (expected)` / `3,240 (max)`

---

### TASK-4: Math & Computation
* **Prompt:** `"Calculate the compound interest on $50,000 at 7.2% annual rate compounded monthly for 15 years."`
* **Inferred Classification:** `writing` / `free_text` / `medium` reasoning depth
* **Primary Recommendation:** ChatGPT (GPT-4o / GPT-5.1)
* **Effort Level:** `medium` | **Extended Thinking:** `on`
* **Predicted Token Bounds:**
  * Input Tokens ($T_{\text{in}}$): `27`
  * Thinking Tokens ($T_{\text{think}}$): `1,024`
  * Output Tokens ($T_{\text{out}}$): `100 (min)` / `350 (exp)` / `850 (max)`
  * **Total Predicted Tokens ($T_{\text{total}}$):** `1,151 (min)` / `~1,401 (expected)` / `1,901 (max)`

---

### TASK-5: Creative Writing (Constraint)
* **Prompt:** `"Write a 300-word bedtime story about a friendly dragon who is afraid of the dark."`
* **Inferred Classification:** `creative_writing` / `free_text` / `medium` reasoning depth
* **Primary Recommendation:** Claude 3.7 Sonnet
* **Effort Level:** `medium` | **Extended Thinking:** `on`
* **Predicted Token Bounds:**
  * Input Tokens ($T_{\text{in}}$): `22`
  * Thinking Tokens ($T_{\text{think}}$): `1,024`
  * Output Tokens ($T_{\text{out}}$): `319 (min)` / `399 (exp)` / `498 (max)`
  * **Total Predicted Tokens ($T_{\text{total}}$):** `1,365 (min)` / `~1,445 (expected)` / `1,544 (max)`
