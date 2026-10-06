# Actual Token Usage Results

> **Source:** `evaluation/actual_token_usage_results.json` | Tasks: TASK-1 to TASK-365

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | **365** |
| Live-executed (actual tokens verified) | **5** (TASK-1 – TASK-5) |
| Prediction-only entries | **360** (TASK-6 – TASK-365) |
| Average accuracy on live tasks | **75.0%** |
| Within predicted bounds (live) | **4 / 5** |

> **Note on PREDICTED_ONLY tasks:** The free Gemini API tier is capped at 20 requests/day.
> All 360 benchmark tasks have been run through the token predictor engine, but only 5
> have actual live API call results. A paid API plan enables full verification.

## Live-Executed Tasks — Actual vs Predicted

| Task | Category | Prompt (excerpt) | Model | Predicted Total | Actual Total | Accuracy | In Bounds | Latency |
|------|----------|-----------------|-------|----------------|-------------|----------|-----------|---------|
| TASK-1 | Coding & Automation | Write a Python script to parse a 10GB JSON file asynchronously an… | DeepSeek V4 (Flash / Pro) | 1,395–2,445 (exp 1,695) | 1,616 | 95.3% | ✅ | 9.69s |
| TASK-2 | Summarization (Constra | Summarize the key points of the 2026 EU AI Act compliance guideli… | Perplexity Pro | 1,447–3,247 (exp 1,897) | 658 | 34.7% | ⚠️ | 5.36s |
| TASK-3 | Web Research & Analysi | What are the latest developments in generative AI hardware archit… | Perplexity Pro | 1,440–3,240 (exp 1,890) | 1,777 | 94.0% | ✅ | 11.17s |
| TASK-4 | Math & Computation | Calculate the compound interest on $50,000 at 7.2% annual rate co… | ChatGPT (GPT-4o / GPT-5.1) | 1,151–1,901 (exp 1,401) | 1,018 | 72.7% | ✅ | 4.44s |
| TASK-5 | Creative Writing (Cons | Write a 300-word bedtime story about a friendly dragon who is afr… | Claude 3.7 Sonnet | 1,365–1,544 (exp 1,445) | 1,130 | 78.2% | ✅ | 6.03s |

## All 365 Tasks — Token Breakdown

| # | Task | Suite | Label | Model | Effort | Thinking | In | Think | Out (exp) | Total (exp) | Status |
|---|------|-------|-------|-------|--------|----------|-----|-------|-----------|------------|--------|
| 1 | TASK-1 | LIVE | Coding & Automation | DeepSeek V4 (Flash / Pro | medium | ON | 21 | 1,024 | 650 | 1,695 | 🟢 Live |
| 2 | TASK-2 | LIVE | Summarization (Constraint) | Perplexity Pro | medium | ON | 23 | 1,024 | 850 | 1,897 | 🟢 Live |
| 3 | TASK-3 | LIVE | Web Research & Analysis | Perplexity Pro | medium | ON | 16 | 1,024 | 850 | 1,890 | 🟢 Live |
| 4 | TASK-4 | LIVE | Math & Computation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 27 | 1,024 | 350 | 1,401 | 🟢 Live |
| 5 | TASK-5 | LIVE | Creative Writing (Constraint) | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 399 | 1,445 | 🟢 Live |
| 6 | TASK-6 | Comprehe | Basic arithmetic | ChatGPT (GPT-4o / GPT-5. | medium | ON | 27 | 1,024 | 350 | 1,401 | 🔵 Pred |
| 7 | TASK-7 | Comprehe | Matrix operations | ChatGPT (GPT-4o / GPT-5. | medium | ON | 16 | 1,024 | 350 | 1,390 | 🔵 Pred |
| 8 | TASK-8 | Comprehe | Statistical computation | ChatGPT (GPT-4o / GPT-5. | high | ON | 25 | 4,096 | 250 | 4,371 | 🔵 Pred |
| 9 | TASK-9 | Comprehe | Optimization problem | ChatGPT (GPT-4o / GPT-5. | medium | ON | 38 | 1,024 | 350 | 1,412 | 🔵 Pred |
| 10 | TASK-10 | Comprehe | Calculus | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 11 | TASK-11 | Comprehe | Probability calculation | Gamma | medium | ON | 30 | 1,024 | 850 | 1,904 | 🔵 Pred |
| 12 | TASK-12 | Comprehe | Physics computation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 34 | 1,024 | 350 | 1,408 | 🔵 Pred |
| 13 | TASK-13 | Comprehe | Financial modeling | ChatGPT (GPT-4o / GPT-5. | medium | ON | 37 | 1,024 | 350 | 1,411 | 🔵 Pred |
| 14 | TASK-14 | Comprehe | Combinatorics | ChatGPT (GPT-4o / GPT-5. | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 15 | TASK-15 | Comprehe | Differential equations | ChatGPT (GPT-4o / GPT-5. | medium | ON | 45 | 1,024 | 350 | 1,419 | 🔵 Pred |
| 16 | TASK-16 | Comprehe | Python function | DeepSeek V4 (Flash / Pro | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 17 | TASK-17 | Comprehe | SQL query | DeepSeek V4 (Flash / Pro | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 18 | TASK-18 | Comprehe | JavaScript async | DeepSeek V4 (Flash / Pro | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 19 | TASK-19 | Comprehe | Rust systems code | DeepSeek V4 (Flash / Pro | medium | ON | 33 | 1,024 | 350 | 1,407 | 🔵 Pred |
| 20 | TASK-20 | Comprehe | React component | DeepSeek V4 (Flash / Pro | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 21 | TASK-21 | Comprehe | Bash automation | DeepSeek V4 (Flash / Pro | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 22 | TASK-22 | Comprehe | API endpoint | DeepSeek V4 (Flash / Pro | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 23 | TASK-23 | Comprehe | Database migration | DeepSeek V4 (Flash / Pro | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 24 | TASK-24 | Comprehe | Unit tests | Claude Code / Cursor | high | ON | 27 | 4,096 | 700 | 4,823 | 🔵 Pred |
| 25 | TASK-25 | Comprehe | Regex pattern | DeepSeek V4 (Flash / Pro | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 26 | TASK-26 | Comprehe | Grammar correction | ChatGPT (GPT-4o / GPT-5. | medium | ON | 33 | 1,024 | 350 | 1,407 | 🔵 Pred |
| 27 | TASK-27 | Comprehe | Sentence completion | ChatGPT (GPT-4o / GPT-5. | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 28 | TASK-28 | Comprehe | Tone adjustment | Claude 3.7 Sonnet | medium | ON | 16 | 1,024 | 550 | 1,590 | 🔵 Pred |
| 29 | TASK-29 | Comprehe | Text expansion | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 665 | 1,712 | 🔵 Pred |
| 30 | TASK-30 | Comprehe | Text simplification | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 550 | 1,596 | 🔵 Pred |
| 31 | TASK-31 | Comprehe | Formal rewriting | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 550 | 1,594 | 🔵 Pred |
| 32 | TASK-32 | Comprehe | Proofreading | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 2,660 | 3,707 | 🔵 Pred |
| 33 | TASK-33 | Comprehe | Headline generation | Claude 3.7 Sonnet | high | ON | 19 | 4,096 | 750 | 4,865 | 🔵 Pred |
| 34 | TASK-34 | Comprehe | Fill-in template | Claude 3.7 Sonnet | medium | ON | 24 | 1,024 | 450 | 1,498 | 🔵 Pred |
| 35 | TASK-35 | Comprehe | Style transfer | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 550 | 1,596 | 🔵 Pred |
| 36 | TASK-36 | Comprehe | Incident postmortem | Claude 3.7 Sonnet | high | ON | 27 | 4,096 | 750 | 4,873 | 🔵 Pred |
| 37 | TASK-37 | Comprehe | Board memo | Perplexity Pro | medium | ON | 37 | 1,024 | 850 | 1,911 | 🔵 Pred |
| 38 | TASK-38 | Comprehe | Crisis communication | DeepSeek V4 (Flash / Pro | medium | ON | 37 | 1,024 | 350 | 1,411 | 🔵 Pred |
| 39 | TASK-39 | Comprehe | Legal clause | Claude 3.7 Sonnet | high | ON | 27 | 4,096 | 750 | 4,873 | 🔵 Pred |
| 40 | TASK-40 | Comprehe | RFP response | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 41 | TASK-41 | Comprehe | Business proposal | Claude 3.7 Sonnet | high | ON | 27 | 4,096 | 750 | 4,873 | 🔵 Pred |
| 42 | TASK-42 | Comprehe | Press release | Perplexity Pro | medium | ON | 24 | 1,024 | 850 | 1,898 | 🔵 Pred |
| 43 | TASK-43 | Comprehe | Policy document | ChatGPT (GPT-4o / GPT-5. | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 44 | TASK-44 | Comprehe | Meeting minutes | ChatGPT (GPT-4o / GPT-5. | medium | ON | 33 | 1,024 | 350 | 1,407 | 🔵 Pred |
| 45 | TASK-45 | Comprehe | Strategy document | Claude 3.7 Sonnet | high | ON | 37 | 4,096 | 750 | 4,883 | 🔵 Pred |
| 46 | TASK-46 | Comprehe | CSV reconciliation | ChatGPT (GPT-4o / GPT-5. | high | ON | 24 | 4,096 | 250 | 4,370 | 🔵 Pred |
| 47 | TASK-47 | Comprehe | Dashboard design | ChatGPT (GPT-4o / GPT-5. | high | ON | 26 | 4,096 | 250 | 4,372 | 🔵 Pred |
| 48 | TASK-48 | Comprehe | A/B test analysis | ChatGPT (GPT-4o / GPT-5. | high | ON | 50 | 4,096 | 250 | 4,396 | 🔵 Pred |
| 49 | TASK-49 | Comprehe | ETL pipeline | Claude Code / Cursor | high | ON | 31 | 4,096 | 350 | 4,477 | 🔵 Pred |
| 50 | TASK-50 | Comprehe | Invoice extraction | Claude 3.7 Sonnet | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 51 | TASK-51 | Comprehe | Time series forecast | ChatGPT (GPT-4o / GPT-5. | high | ON | 28 | 4,096 | 250 | 4,374 | 🔵 Pred |
| 52 | TASK-52 | Comprehe | Data cleaning | ChatGPT (GPT-4o / GPT-5. | high | ON | 30 | 4,096 | 250 | 4,376 | 🔵 Pred |
| 53 | TASK-53 | Comprehe | Log analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 30 | 1,024 | 350 | 1,404 | 🔵 Pred |
| 54 | TASK-54 | Comprehe | Survey analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 55 | TASK-55 | Comprehe | Financial data extraction | ChatGPT (GPT-4o / GPT-5. | high | ON | 35 | 4,096 | 250 | 4,381 | 🔵 Pred |
| 56 | TASK-56 | Comprehe | Competitor analysis | Perplexity Pro | medium | ON | 26 | 1,024 | 850 | 1,900 | 🔵 Pred |
| 57 | TASK-57 | Comprehe | Regulatory research | Perplexity Pro | medium | ON | 27 | 1,024 | 850 | 1,901 | 🔵 Pred |
| 58 | TASK-58 | Comprehe | Market sizing | DeepSeek V4 (Flash / Pro | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 59 | TASK-59 | Comprehe | Academic literature | Perplexity Pro | medium | ON | 28 | 1,024 | 850 | 1,902 | 🔵 Pred |
| 60 | TASK-60 | Comprehe | Patent search | Perplexity Pro | medium | ON | 22 | 1,024 | 850 | 1,896 | 🔵 Pred |
| 61 | TASK-61 | Comprehe | Technology comparison | Perplexity Pro | medium | ON | 26 | 1,024 | 850 | 1,900 | 🔵 Pred |
| 62 | TASK-62 | Comprehe | Industry benchmarks | Perplexity Pro | medium | ON | 27 | 1,024 | 850 | 1,901 | 🔵 Pred |
| 63 | TASK-63 | Comprehe | Hiring market research | Perplexity Pro | medium | ON | 29 | 1,024 | 850 | 1,903 | 🔵 Pred |
| 64 | TASK-64 | Comprehe | Product recall lookup | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 65 | TASK-65 | Comprehe | Standards lookup | Perplexity Pro | medium | ON | 19 | 1,024 | 850 | 1,893 | 🔵 Pred |
| 66 | TASK-66 | Comprehe | Legal contract summary | Claude 3.7 Sonnet | high | ON | 27 | 4,096 | 750 | 4,873 | 🔵 Pred |
| 67 | TASK-67 | Comprehe | Meeting notes summary | Claude 3.7 Sonnet | medium | ON | 27 | 1,024 | 450 | 1,501 | 🔵 Pred |
| 68 | TASK-68 | Comprehe | Research paper summary | Claude 3.7 Sonnet | medium | ON | 24 | 1,024 | 450 | 1,498 | 🔵 Pred |
| 69 | TASK-69 | Comprehe | Multi-doc synthesis | Claude 3.7 Sonnet | medium | ON | 26 | 1,024 | 450 | 1,500 | 🔵 Pred |
| 70 | TASK-70 | Comprehe | Email thread summary | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 71 | TASK-71 | Comprehe | Earnings call summary | Claude 3.7 Sonnet | medium | ON | 26 | 1,024 | 450 | 1,500 | 🔵 Pred |
| 72 | TASK-72 | Comprehe | Book chapter summary | Claude 3.7 Sonnet | medium | ON | 29 | 1,024 | 450 | 1,503 | 🔵 Pred |
| 73 | TASK-73 | Comprehe | Regulatory filing summary | Perplexity Pro | medium | ON | 34 | 1,024 | 850 | 1,908 | 🔵 Pred |
| 74 | TASK-74 | Comprehe | Customer feedback synthesis | Claude 3.7 Sonnet | medium | ON | 28 | 1,024 | 450 | 1,502 | 🔵 Pred |
| 75 | TASK-75 | Comprehe | Technical spec summary | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 76 | TASK-76 | Comprehe | Short story | Claude 3.7 Sonnet | medium | ON | 27 | 1,024 | 550 | 1,601 | 🔵 Pred |
| 77 | TASK-77 | Comprehe | Marketing copy | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 550 | 1,596 | 🔵 Pred |
| 78 | TASK-78 | Comprehe | Speech writing | Claude 3.7 Sonnet | medium | ON | 33 | 1,024 | 550 | 1,607 | 🔵 Pred |
| 79 | TASK-79 | Comprehe | Blog post | Claude 3.7 Sonnet | medium | ON | 25 | 1,024 | 1,995 | 3,044 | 🔵 Pred |
| 80 | TASK-80 | Comprehe | Ad copy variants | ChatGPT (GPT-4o / GPT-5. | medium | ON | 19 | 1,024 | 350 | 1,393 | 🔵 Pred |
| 81 | TASK-81 | Comprehe | Product descriptions | Claude 3.7 Sonnet | medium | ON | 18 | 1,024 | 550 | 1,592 | 🔵 Pred |
| 82 | TASK-82 | Comprehe | Newsletter | Claude 3.7 Sonnet | medium | ON | 27 | 1,024 | 550 | 1,601 | 🔵 Pred |
| 83 | TASK-83 | Comprehe | Screenplay dialogue | Claude 3.7 Sonnet | medium | ON | 29 | 1,024 | 550 | 1,603 | 🔵 Pred |
| 84 | TASK-84 | Comprehe | Poetry | Claude 3.7 Sonnet | medium | ON | 16 | 1,024 | 550 | 1,590 | 🔵 Pred |
| 85 | TASK-85 | Comprehe | Children's story | Claude 3.7 Sonnet | medium | ON | 28 | 1,024 | 550 | 1,602 | 🔵 Pred |
| 86 | TASK-86 | Comprehe | Technical manual translation | DeepSeek V4 (Flash / Pro | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 87 | TASK-87 | Comprehe | Marketing localization | Claude 3.7 Sonnet | low | OFF | 25 | 0 | 32 | 57 | 🔵 Pred |
| 88 | TASK-88 | Comprehe | Legal translation | Claude 3.7 Sonnet | low | OFF | 20 | 0 | 26 | 46 | 🔵 Pred |
| 89 | TASK-89 | Comprehe | Subtitle translation | Claude 3.7 Sonnet | low | OFF | 20 | 0 | 26 | 46 | 🔵 Pred |
| 90 | TASK-90 | Comprehe | Website localization | Claude 3.7 Sonnet | low | OFF | 22 | 0 | 28 | 50 | 🔵 Pred |
| 91 | TASK-91 | Comprehe | Medical translation | Claude 3.7 Sonnet | low | OFF | 20 | 0 | 26 | 46 | 🔵 Pred |
| 92 | TASK-92 | Comprehe | Multilingual SEO | Perplexity Pro | medium | ON | 25 | 1,024 | 850 | 1,899 | 🔵 Pred |
| 93 | TASK-93 | Comprehe | Cultural adaptation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 94 | TASK-94 | Comprehe | Real-time translation | Claude 3.7 Sonnet | low | OFF | 18 | 0 | 23 | 41 | 🔵 Pred |
| 95 | TASK-95 | Comprehe | Patent translation | Claude 3.7 Sonnet | low | OFF | 24 | 0 | 31 | 55 | 🔵 Pred |
| 96 | TASK-96 | Comprehe | Sentiment analysis | Gemini 3.6 Flash / Pro | low | OFF | 26 | 0 | 150 | 176 | 🔵 Pred |
| 97 | TASK-97 | Comprehe | Support ticket routing | Gemini 3.6 Flash / Pro | low | OFF | 24 | 0 | 150 | 174 | 🔵 Pred |
| 98 | TASK-98 | Comprehe | Fraud detection | Gemini 3.6 Flash / Pro | low | OFF | 27 | 0 | 150 | 177 | 🔵 Pred |
| 99 | TASK-99 | Comprehe | Content moderation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 100 | TASK-100 | Comprehe | Lead scoring | Gemini 3.6 Flash / Pro | low | OFF | 30 | 0 | 150 | 180 | 🔵 Pred |
| 101 | TASK-101 | Comprehe | Email categorization | Gemini 3.6 Flash / Pro | low | OFF | 28 | 0 | 150 | 178 | 🔵 Pred |
| 102 | TASK-102 | Comprehe | Document classification | Claude 3.7 Sonnet | medium | ON | 25 | 1,024 | 450 | 1,499 | 🔵 Pred |
| 103 | TASK-103 | Comprehe | Intent detection | ChatGPT (GPT-4o / GPT-5. | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 104 | TASK-104 | Comprehe | Priority tagging | ChatGPT (GPT-4o / GPT-5. | medium | ON | 39 | 1,024 | 350 | 1,413 | 🔵 Pred |
| 105 | TASK-105 | Comprehe | Duplicate detection | Gemini 3.6 Flash / Pro | low | OFF | 30 | 0 | 150 | 180 | 🔵 Pred |
| 106 | TASK-106 | Comprehe | Chart interpretation | Gemini 3.6 Flash / Pro | medium | ON | 30 | 1,024 | 450 | 1,504 | 🔵 Pred |
| 107 | TASK-107 | Comprehe | Screenshot debugging | Gemini 3.6 Flash / Pro | medium | ON | 32 | 1,024 | 450 | 1,506 | 🔵 Pred |
| 108 | TASK-108 | Comprehe | Architecture diagram review | Gemini 3.6 Flash / Pro | medium | ON | 24 | 1,024 | 450 | 1,498 | 🔵 Pred |
| 109 | TASK-109 | Comprehe | Image cataloging | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 110 | TASK-110 | Comprehe | Handwriting OCR | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 111 | TASK-111 | Comprehe | UI mockup review | ChatGPT (GPT-4o / GPT-5. | high | ON | 25 | 4,096 | 250 | 4,371 | 🔵 Pred |
| 112 | TASK-112 | Comprehe | Video summary | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 113 | TASK-113 | Comprehe | Receipt extraction | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 114 | TASK-114 | Comprehe | Before/after comparison | Gemini 3.6 Flash / Pro | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 115 | TASK-115 | Comprehe | Wireframe to code | DeepSeek V4 (Flash / Pro | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 116 | TASK-116 | Comprehe | Mathematical proof | Claude 3.7 Sonnet | high | ON | 24 | 4,096 | 650 | 4,770 | 🔵 Pred |
| 117 | TASK-117 | Comprehe | Algorithm correctness | Claude 3.7 Sonnet | high | ON | 24 | 4,096 | 650 | 4,770 | 🔵 Pred |
| 118 | TASK-118 | Comprehe | Logic puzzle | Claude 3.7 Sonnet | high | ON | 31 | 4,096 | 650 | 4,777 | 🔵 Pred |
| 119 | TASK-119 | Comprehe | Strategic tradeoff analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 37 | 1,024 | 350 | 1,411 | 🔵 Pred |
| 120 | TASK-120 | Comprehe | Causal inference | ChatGPT (GPT-4o / GPT-5. | medium | ON | 34 | 1,024 | 350 | 1,408 | 🔵 Pred |
| 121 | TASK-121 | Comprehe | Game theory problem | Perplexity Pro | medium | ON | 31 | 1,024 | 850 | 1,905 | 🔵 Pred |
| 122 | TASK-122 | Comprehe | Root cause analysis | Claude Code / Cursor | high | ON | 28 | 4,096 | 350 | 4,474 | 🔵 Pred |
| 123 | TASK-123 | Comprehe | Formal verification | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 124 | TASK-124 | Comprehe | Paradox analysis | ChatGPT (GPT-4o / GPT-5. | high | ON | 29 | 4,096 | 250 | 4,375 | 🔵 Pred |
| 125 | TASK-125 | Comprehe | Systems thinking | ChatGPT (GPT-4o / GPT-5. | medium | ON | 36 | 1,024 | 350 | 1,410 | 🔵 Pred |
| 126 | TASK-126 | Comprehe | Investor pitch deck | Gamma | medium | ON | 33 | 1,024 | 850 | 1,907 | 🔵 Pred |
| 127 | TASK-127 | Comprehe | Sales deck | Gamma | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 128 | TASK-128 | Comprehe | Board QBR deck | Gamma | medium | ON | 26 | 1,024 | 850 | 1,900 | 🔵 Pred |
| 129 | TASK-129 | Comprehe | Conference talk slides | Claude Code / Cursor | high | ON | 22 | 4,096 | 350 | 4,468 | 🔵 Pred |
| 130 | TASK-130 | Comprehe | Product launch deck | Gamma | medium | ON | 23 | 1,024 | 850 | 1,897 | 🔵 Pred |
| 131 | TASK-131 | Comprehe | Training deck | Gamma | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 132 | TASK-132 | Comprehe | All-hands deck | ChatGPT (GPT-4o / GPT-5. | medium | ON | 27 | 1,024 | 350 | 1,401 | 🔵 Pred |
| 133 | TASK-133 | Comprehe | Webinar deck | Gamma | medium | ON | 25 | 1,024 | 850 | 1,899 | 🔵 Pred |
| 134 | TASK-134 | Comprehe | Infographic slide | Gamma | medium | ON | 29 | 1,024 | 850 | 1,903 | 🔵 Pred |
| 135 | TASK-135 | Comprehe | Partner pitch deck | Gamma | medium | ON | 20 | 1,024 | 850 | 1,894 | 🔵 Pred |
| 136 | TASK-136 | Comprehe | One-word prompt | ChatGPT (GPT-4o / GPT-5. | medium | ON | 2 | 1,024 | 350 | 1,376 | 🔵 Pred |
| 137 | TASK-137 | Comprehe | Empty context | ChatGPT (GPT-4o / GPT-5. | medium | ON | 4 | 1,024 | 350 | 1,378 | 🔵 Pred |
| 138 | TASK-138 | Comprehe | Contradictory instructions | ChatGPT (GPT-4o / GPT-5. | medium | ON | 17 | 1,024 | 6,650 | 7,691 | 🔵 Pred |
| 139 | TASK-139 | Comprehe | Multi-domain mashup | DeepSeek V4 (Flash / Pro | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 140 | TASK-140 | Comprehe | Adversarial injection | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 141 | TASK-141 | Comprehe | Extremely vague | ChatGPT (GPT-4o / GPT-5. | medium | ON | 4 | 1,024 | 350 | 1,378 | 🔵 Pred |
| 142 | TASK-142 | Comprehe | Typo-heavy | ChatGPT (GPT-4o / GPT-5. | medium | ON | 17 | 1,024 | 350 | 1,391 | 🔵 Pred |
| 143 | TASK-143 | Comprehe | Non-English only | ChatGPT (GPT-4o / GPT-5. | medium | ON | 14 | 1,024 | 350 | 1,388 | 🔵 Pred |
| 144 | TASK-144 | Comprehe | Meta-routing question | Claude 3.7 Sonnet | high | ON | 19 | 4,096 | 750 | 4,865 | 🔵 Pred |
| 145 | TASK-145 | Comprehe | Impossible task | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 146 | TASK-146 | Comprehe | Research + write | Perplexity Pro | medium | ON | 25 | 1,024 | 2,660 | 3,709 | 🔵 Pred |
| 147 | TASK-147 | Comprehe | Analyze + present | Gamma | medium | ON | 23 | 1,024 | 850 | 1,897 | 🔵 Pred |
| 148 | TASK-148 | Comprehe | Extract + summarize | Claude 3.7 Sonnet | medium | ON | 33 | 1,024 | 450 | 1,507 | 🔵 Pred |
| 149 | TASK-149 | Comprehe | Code + test + deploy | Claude Code / Cursor | high | ON | 30 | 4,096 | 700 | 4,826 | 🔵 Pred |
| 150 | TASK-150 | Comprehe | Survey + report | Claude Code / Cursor | high | ON | 28 | 4,096 | 700 | 4,824 | 🔵 Pred |
| 151 | TASK-151 | Comprehe | Translate + localize + test | Claude 3.7 Sonnet | low | OFF | 27 | 0 | 35 | 62 | 🔵 Pred |
| 152 | TASK-152 | Comprehe | Audit + fix + document | Claude Code / Cursor | high | ON | 22 | 4,096 | 350 | 4,468 | 🔵 Pred |
| 153 | TASK-153 | Comprehe | Competitive intel pipeline | Perplexity Pro | medium | ON | 31 | 1,024 | 850 | 1,905 | 🔵 Pred |
| 154 | TASK-154 | Comprehe | Data pipeline end-to-end | Claude Code / Cursor | high | ON | 37 | 4,096 | 350 | 4,483 | 🔵 Pred |
| 155 | TASK-155 | Comprehe | Incident response workflow | Claude 3.7 Sonnet | high | ON | 29 | 4,096 | 750 | 4,875 | 🔵 Pred |
| 156 | TASK-156 | Stress T | Bug fix legacy code | Claude Code / Cursor | high | ON | 27 | 4,096 | 350 | 4,473 | 🔵 Pred |
| 157 | TASK-157 | Stress T | API integration | DeepSeek V4 (Flash / Pro | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 158 | TASK-158 | Stress T | DB schema design | DeepSeek V4 (Flash / Pro | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 159 | TASK-159 | Stress T | Frontend UI component | DeepSeek V4 (Flash / Pro | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 160 | TASK-160 | Stress T | DevOps/CI-CD script | Claude Code / Cursor | high | ON | 26 | 4,096 | 700 | 4,822 | 🔵 Pred |
| 161 | TASK-161 | Stress T | Mobile app dev | DeepSeek V4 (Flash / Pro | medium | ON | 19 | 1,024 | 350 | 1,393 | 🔵 Pred |
| 162 | TASK-162 | Stress T | Code review | Claude Code / Cursor | high | ON | 18 | 4,096 | 350 | 4,464 | 🔵 Pred |
| 163 | TASK-163 | Stress T | Algorithm design | Claude 3.7 Sonnet | high | ON | 23 | 4,096 | 650 | 4,769 | 🔵 Pred |
| 164 | TASK-164 | Stress T | Unit test generation | Claude Code / Cursor | high | ON | 14 | 4,096 | 700 | 4,810 | 🔵 Pred |
| 165 | TASK-165 | Stress T | Security vulnerability scan | DeepSeek V4 (Flash / Pro | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 166 | TASK-166 | Stress T | Excel formula fix | ChatGPT (GPT-4o / GPT-5. | high | ON | 25 | 4,096 | 250 | 4,371 | 🔵 Pred |
| 167 | TASK-167 | Stress T | SQL query writing | DeepSeek V4 (Flash / Pro | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 168 | TASK-168 | Stress T | Data cleaning | ChatGPT (GPT-4o / GPT-5. | high | ON | 20 | 4,096 | 250 | 4,366 | 🔵 Pred |
| 169 | TASK-169 | Stress T | Statistical analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 170 | TASK-170 | Stress T | Dashboard/BI report | ChatGPT (GPT-4o / GPT-5. | high | ON | 20 | 4,096 | 250 | 4,366 | 🔵 Pred |
| 171 | TASK-171 | Stress T | A/B test analysis | ChatGPT (GPT-4o / GPT-5. | high | ON | 45 | 4,096 | 250 | 4,391 | 🔵 Pred |
| 172 | TASK-172 | Stress T | Large CSV reconciliation | ChatGPT (GPT-4o / GPT-5. | high | ON | 23 | 4,096 | 250 | 4,369 | 🔵 Pred |
| 173 | TASK-173 | Stress T | Time-series forecasting | ChatGPT (GPT-4o / GPT-5. | high | ON | 24 | 4,096 | 250 | 4,370 | 🔵 Pred |
| 174 | TASK-174 | Stress T | Data visualization | Gemini 3.6 Flash / Pro | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 175 | TASK-175 | Stress T | ETL pipeline design | Claude Code / Cursor | high | ON | 23 | 4,096 | 350 | 4,469 | 🔵 Pred |
| 176 | TASK-176 | Stress T | Competitor pricing | Perplexity Pro | medium | ON | 20 | 1,024 | 850 | 1,894 | 🔵 Pred |
| 177 | TASK-177 | Stress T | Industry news | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 178 | TASK-178 | Stress T | Stock market update | Perplexity Pro | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 179 | TASK-179 | Stress T | Product comparison | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 180 | TASK-180 | Stress T | Regulatory/policy update | Perplexity Pro | medium | ON | 23 | 1,024 | 850 | 1,897 | 🔵 Pred |
| 181 | TASK-181 | Stress T | Travel destination research | Perplexity Pro | medium | ON | 20 | 1,024 | 850 | 1,894 | 🔵 Pred |
| 182 | TASK-182 | Stress T | Local business lookup | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 183 | TASK-183 | Stress T | Academic paper discovery | Perplexity Pro | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 184 | TASK-184 | Stress T | Real estate market research | Perplexity Pro | medium | ON | 29 | 1,024 | 850 | 1,903 | 🔵 Pred |
| 185 | TASK-185 | Stress T | Sports scores lookup | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 186 | TASK-186 | Stress T | Legal contract summary | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 187 | TASK-187 | Stress T | Meeting transcript summary | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 450 | 1,496 | 🔵 Pred |
| 188 | TASK-188 | Stress T | Research paper summary | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 189 | TASK-189 | Stress T | News article summary | Claude 3.7 Sonnet | medium | ON | 19 | 1,024 | 135 | 1,178 | 🔵 Pred |
| 190 | TASK-190 | Stress T | Book chapter summary | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 450 | 1,496 | 🔵 Pred |
| 191 | TASK-191 | Stress T | Email thread summary | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 192 | TASK-192 | Stress T | Customer feedback summary | Claude 3.7 Sonnet | high | ON | 19 | 4,096 | 450 | 4,565 | 🔵 Pred |
| 193 | TASK-193 | Stress T | Financial report summary | Claude 3.7 Sonnet | high | ON | 22 | 4,096 | 750 | 4,868 | 🔵 Pred |
| 194 | TASK-194 | Stress T | Podcast transcript summary | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 195 | TASK-195 | Stress T | Multi-document synthesis | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 196 | TASK-196 | Stress T | Short story | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 665 | 1,712 | 🔵 Pred |
| 197 | TASK-197 | Stress T | Poetry | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 198 | TASK-198 | Stress T | Marketing copy | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 550 | 1,595 | 🔵 Pred |
| 199 | TASK-199 | Stress T | Screenplay dialogue | Claude 3.7 Sonnet | medium | ON | 19 | 1,024 | 550 | 1,593 | 🔵 Pred |
| 200 | TASK-200 | Stress T | Blog post | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 1,330 | 2,376 | 🔵 Pred |
| 201 | TASK-201 | Stress T | Brand naming/slogans | ChatGPT (GPT-4o / GPT-5. | medium | ON | 16 | 1,024 | 350 | 1,390 | 🔵 Pred |
| 202 | TASK-202 | Stress T | Children's story | Claude 3.7 Sonnet | medium | ON | 31 | 1,024 | 399 | 1,454 | 🔵 Pred |
| 203 | TASK-203 | Stress T | Speech writing | Claude 3.7 Sonnet | medium | ON | 26 | 1,024 | 550 | 1,600 | 🔵 Pred |
| 204 | TASK-204 | Stress T | Parody writing | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 550 | 1,596 | 🔵 Pred |
| 205 | TASK-205 | Stress T | Product description | Claude 3.7 Sonnet | medium | ON | 18 | 1,024 | 550 | 1,592 | 🔵 Pred |
| 206 | TASK-206 | Stress T | Investor pitch deck | Gamma | medium | ON | 25 | 1,024 | 850 | 1,899 | 🔵 Pred |
| 207 | TASK-207 | Stress T | Sales presentation | Gamma | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 208 | TASK-208 | Stress T | Training/onboarding deck | Gamma | medium | ON | 19 | 1,024 | 850 | 1,893 | 🔵 Pred |
| 209 | TASK-209 | Stress T | Conference talk slides | ChatGPT (GPT-4o / GPT-5. | medium | ON | 17 | 1,024 | 350 | 1,391 | 🔵 Pred |
| 210 | TASK-210 | Stress T | Product launch deck | Gamma | medium | ON | 19 | 1,024 | 850 | 1,893 | 🔵 Pred |
| 211 | TASK-211 | Stress T | Board meeting deck | Gamma | medium | ON | 19 | 1,024 | 850 | 1,893 | 🔵 Pred |
| 212 | TASK-212 | Stress T | Single-slide infographic | Gamma | medium | ON | 25 | 1,024 | 850 | 1,899 | 🔵 Pred |
| 213 | TASK-213 | Stress T | Data-heavy chart deck | Gamma | medium | ON | 25 | 1,024 | 850 | 1,899 | 🔵 Pred |
| 214 | TASK-214 | Stress T | Executive summary deck | Gamma | medium | ON | 16 | 1,024 | 850 | 1,890 | 🔵 Pred |
| 215 | TASK-215 | Stress T | Webinar slide deck | Gamma | medium | ON | 21 | 1,024 | 850 | 1,895 | 🔵 Pred |
| 216 | TASK-216 | Stress T | Sentiment classification | Gemini 3.6 Flash / Pro | low | OFF | 22 | 0 | 150 | 172 | 🔵 Pred |
| 217 | TASK-217 | Stress T | Support ticket categorization | Gemini 3.6 Flash / Pro | low | OFF | 20 | 0 | 150 | 170 | 🔵 Pred |
| 218 | TASK-218 | Stress T | Spam/fraud detection | Gemini 3.6 Flash / Pro | low | OFF | 20 | 0 | 150 | 170 | 🔵 Pred |
| 219 | TASK-219 | Stress T | Content moderation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 220 | TASK-220 | Stress T | Lead scoring | Gemini 3.6 Flash / Pro | low | OFF | 27 | 0 | 150 | 177 | 🔵 Pred |
| 221 | TASK-221 | Stress T | Document type classification | Claude 3.7 Sonnet | medium | ON | 22 | 1,024 | 450 | 1,496 | 🔵 Pred |
| 222 | TASK-222 | Stress T | Language detection | ChatGPT (GPT-4o / GPT-5. | medium | ON | 14 | 1,024 | 350 | 1,388 | 🔵 Pred |
| 223 | TASK-223 | Stress T | Topic/genre classification | Gemini 3.6 Flash / Pro | low | OFF | 16 | 0 | 150 | 166 | 🔵 Pred |
| 224 | TASK-224 | Stress T | Priority/urgency tagging | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 225 | TASK-225 | Stress T | Duplicate detection | Gemini 3.6 Flash / Pro | low | OFF | 14 | 0 | 150 | 164 | 🔵 Pred |
| 226 | TASK-226 | Stress T | Document translation | Claude 3.7 Sonnet | low | OFF | 16 | 0 | 20 | 36 | 🔵 Pred |
| 227 | TASK-227 | Stress T | Website localization | Claude 3.7 Sonnet | low | OFF | 21 | 0 | 27 | 48 | 🔵 Pred |
| 228 | TASK-228 | Stress T | Marketing translation | Claude 3.7 Sonnet | low | OFF | 20 | 0 | 26 | 46 | 🔵 Pred |
| 229 | TASK-229 | Stress T | Legal doc translation | Claude 3.7 Sonnet | low | OFF | 16 | 0 | 20 | 36 | 🔵 Pred |
| 230 | TASK-230 | Stress T | Real-time chat translation | Claude 3.7 Sonnet | low | OFF | 16 | 0 | 20 | 36 | 🔵 Pred |
| 231 | TASK-231 | Stress T | Subtitle translation | Claude 3.7 Sonnet | low | OFF | 20 | 0 | 26 | 46 | 🔵 Pred |
| 232 | TASK-232 | Stress T | Technical manual translation | Claude 3.7 Sonnet | low | OFF | 16 | 0 | 20 | 36 | 🔵 Pred |
| 233 | TASK-233 | Stress T | Multilingual SEO | Perplexity Pro | medium | ON | 20 | 1,024 | 850 | 1,894 | 🔵 Pred |
| 234 | TASK-234 | Stress T | Voice transcript translation | Claude 3.7 Sonnet | low | OFF | 12 | 0 | 15 | 27 | 🔵 Pred |
| 235 | TASK-235 | Stress T | Idiomatic/cultural adaptation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 236 | TASK-236 | Stress T | Mathematical proof | Claude 3.7 Sonnet | high | ON | 24 | 4,096 | 650 | 4,770 | 🔵 Pred |
| 237 | TASK-237 | Stress T | Logic puzzle | Claude 3.7 Sonnet | high | ON | 40 | 4,096 | 650 | 4,786 | 🔵 Pred |
| 238 | TASK-238 | Stress T | Algorithm complexity | Claude 3.7 Sonnet | high | ON | 28 | 4,096 | 650 | 4,774 | 🔵 Pred |
| 239 | TASK-239 | Stress T | Statistical hypothesis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 33 | 1,024 | 350 | 1,407 | 🔵 Pred |
| 240 | TASK-240 | Stress T | Game theory | Claude 3.7 Sonnet | high | ON | 28 | 4,096 | 650 | 4,774 | 🔵 Pred |
| 241 | TASK-241 | Stress T | Multi-step word problem | ChatGPT (GPT-4o / GPT-5. | medium | ON | 41 | 1,024 | 350 | 1,415 | 🔵 Pred |
| 242 | TASK-242 | Stress T | Architecture tradeoff | ChatGPT (GPT-4o / GPT-5. | high | ON | 32 | 4,096 | 350 | 4,478 | 🔵 Pred |
| 243 | TASK-243 | Stress T | Root-cause analysis | Claude Code / Cursor | high | ON | 35 | 4,096 | 350 | 4,481 | 🔵 Pred |
| 244 | TASK-244 | Stress T | Scientific hypothesis | Claude 3.7 Sonnet | high | ON | 26 | 4,096 | 650 | 4,772 | 🔵 Pred |
| 245 | TASK-245 | Stress T | Strategic decision analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 246 | TASK-246 | Stress T | Full contract review | Gemini 3.6 Flash / Pro | high | ON | 27 | 4,096 | 950 | 5,073 | 🔵 Pred |
| 247 | TASK-247 | Stress T | Codebase-wide analysis | Claude Code / Cursor | high | ON | 23 | 4,096 | 350 | 4,469 | 🔵 Pred |
| 248 | TASK-248 | Stress T | Multi-year financial review | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 249 | TASK-249 | Stress T | Litigation document review | Gemini 3.6 Flash / Pro | high | ON | 27 | 4,096 | 105,000 | 109,123 | 🔵 Pred |
| 250 | TASK-250 | Stress T | Regulatory compliance review | Gemini 3.6 Flash / Pro | high | ON | 19 | 4,096 | 950 | 5,065 | 🔵 Pred |
| 251 | TASK-251 | Stress T | Manuscript analysis | Gemini 3.6 Flash / Pro | high | ON | 26 | 4,096 | 0 | 4,122 | 🔵 Pred |
| 252 | TASK-252 | Stress T | Research corpus meta-analysis | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 253 | TASK-253 | Stress T | Transcript series review | Gemini 3.6 Flash / Pro | high | ON | 23 | 4,096 | 950 | 5,069 | 🔵 Pred |
| 254 | TASK-254 | Stress T | Technical spec review | Gemini 3.6 Flash / Pro | high | ON | 24 | 4,096 | 950 | 5,070 | 🔵 Pred |
| 255 | TASK-255 | Stress T | M&A due-diligence docs | Gemini 3.6 Flash / Pro | high | ON | 30 | 4,096 | 140,000 | 144,126 | 🔵 Pred |
| 256 | TASK-256 | Stress T | Chart interpretation | Gemini 3.6 Flash / Pro | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 257 | TASK-257 | Stress T | Screenshot bug diagnosis | Gemini 3.6 Flash / Pro | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 258 | TASK-258 | Stress T | Image product cataloging | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 259 | TASK-259 | Stress T | Diagram/flowchart explanation | Gemini 3.6 Flash / Pro | medium | ON | 12 | 1,024 | 450 | 1,486 | 🔵 Pred |
| 260 | TASK-260 | Stress T | Handwriting/OCR extraction | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 261 | TASK-261 | Stress T | Video content summary | Claude 3.7 Sonnet | medium | ON | 16 | 1,024 | 450 | 1,490 | 🔵 Pred |
| 262 | TASK-262 | Stress T | UI/UX mockup review | Gemini 3.6 Flash / Pro | low | OFF | 18 | 0 | 150 | 168 | 🔵 Pred |
| 263 | TASK-263 | Stress T | Image description | Gemini 3.6 Flash / Pro | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 264 | TASK-264 | Stress T | Receipt/form data extraction | Gemini 3.6 Flash / Pro | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 265 | TASK-265 | Stress T | Comparative image analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 266 | TASK-266 | Stress T | Web + code task | DeepSeek V4 (Flash / Pro | medium | ON | 30 | 1,024 | 700 | 1,754 | 🔵 Pred |
| 267 | TASK-267 | Stress T | File organization | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 268 | TASK-268 | Stress T | Calendar + email coordination | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 269 | TASK-269 | Stress T | Multi-API orchestration | ChatGPT (GPT-4o / GPT-5. | high | ON | 25 | 4,096 | 250 | 4,371 | 🔵 Pred |
| 270 | TASK-270 | Stress T | Browser automation | ChatGPT (GPT-4o / GPT-5. | high | ON | 28 | 4,096 | 250 | 4,374 | 🔵 Pred |
| 271 | TASK-271 | Stress T | Research + report pipeline | Gamma | medium | ON | 31 | 1,024 | 850 | 1,905 | 🔵 Pred |
| 272 | TASK-272 | Stress T | Multi-file refactor + deploy | Claude Code / Cursor | high | ON | 28 | 4,096 | 700 | 4,824 | 🔵 Pred |
| 273 | TASK-273 | Stress T | Data pipeline + notification | ChatGPT (GPT-4o / GPT-5. | high | ON | 29 | 4,096 | 250 | 4,375 | 🔵 Pred |
| 274 | TASK-274 | Stress T | Cross-platform sync | Gemini 3.6 Flash / Pro | low | OFF | 23 | 0 | 150 | 173 | 🔵 Pred |
| 275 | TASK-275 | Stress T | Monitoring agent | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 276 | TASK-276 | Stress T | Contract clause drafting | Claude 3.7 Sonnet | high | ON | 24 | 4,096 | 750 | 4,870 | 🔵 Pred |
| 277 | TASK-277 | Stress T | NDA review | Gemini 3.6 Flash / Pro | low | OFF | 20 | 0 | 150 | 170 | 🔵 Pred |
| 278 | TASK-278 | Stress T | Compliance checklist | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 279 | TASK-279 | Stress T | IP/trademark research | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 280 | TASK-280 | Stress T | Employment law question | Claude 3.7 Sonnet | high | ON | 28 | 4,096 | 750 | 4,874 | 🔵 Pred |
| 281 | TASK-281 | Stress T | Case brief summarization | Claude 3.7 Sonnet | medium | ON | 21 | 1,024 | 450 | 1,495 | 🔵 Pred |
| 282 | TASK-282 | Stress T | Regulatory filing drafting | Claude 3.7 Sonnet | medium | ON | 19 | 1,024 | 450 | 1,493 | 🔵 Pred |
| 283 | TASK-283 | Stress T | ToS drafting | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 284 | TASK-284 | Stress T | Litigation strategy | Claude 3.7 Sonnet | high | ON | 20 | 4,096 | 650 | 4,766 | 🔵 Pred |
| 285 | TASK-285 | Stress T | Legal citation formatting | ChatGPT (GPT-4o / GPT-5. | medium | ON | 11 | 1,024 | 350 | 1,385 | 🔵 Pred |
| 286 | TASK-286 | Stress T | Symptom info lookup | ChatGPT (GPT-4o / GPT-5. | medium | ON | 28 | 1,024 | 350 | 1,402 | 🔵 Pred |
| 287 | TASK-287 | Stress T | Medical literature summary | Claude 3.7 Sonnet | medium | ON | 26 | 1,024 | 450 | 1,500 | 🔵 Pred |
| 288 | TASK-288 | Stress T | Clinical trial data review | Claude 3.7 Sonnet | medium | ON | 23 | 1,024 | 450 | 1,497 | 🔵 Pred |
| 289 | TASK-289 | Stress T | Patient education material | Claude 3.7 Sonnet | medium | ON | 25 | 1,024 | 550 | 1,599 | 🔵 Pred |
| 290 | TASK-290 | Stress T | Healthcare policy analysis | Perplexity Pro | medium | ON | 19 | 1,024 | 850 | 1,893 | 🔵 Pred |
| 291 | TASK-291 | Stress T | Medical billing question | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 292 | TASK-292 | Stress T | Public health data analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 293 | TASK-293 | Stress T | Nutrition/fitness plan | ChatGPT (GPT-4o / GPT-5. | medium | ON | 32 | 1,024 | 350 | 1,406 | 🔵 Pred |
| 294 | TASK-294 | Stress T | Medical device documentation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 295 | TASK-295 | Stress T | Insurance claims analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 19 | 1,024 | 350 | 1,393 | 🔵 Pred |
| 296 | TASK-296 | Stress T | Budget forecasting | ChatGPT (GPT-4o / GPT-5. | high | ON | 29 | 4,096 | 250 | 4,375 | 🔵 Pred |
| 297 | TASK-297 | Stress T | Tax question research | Perplexity Pro | medium | ON | 27 | 1,024 | 850 | 1,901 | 🔵 Pred |
| 298 | TASK-298 | Stress T | Investment portfolio analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 299 | TASK-299 | Stress T | Expense reconciliation | Gemini 3.6 Flash / Pro | low | OFF | 21 | 0 | 150 | 171 | 🔵 Pred |
| 300 | TASK-300 | Stress T | Financial statement prep | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 301 | TASK-301 | Stress T | Loan calculation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 34 | 1,024 | 350 | 1,408 | 🔵 Pred |
| 302 | TASK-302 | Stress T | Currency conversion analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 303 | TASK-303 | Stress T | Audit checklist | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 304 | TASK-304 | Stress T | Payroll question | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 305 | TASK-305 | Stress T | Valuation/DCF modeling | ChatGPT (GPT-4o / GPT-5. | medium | ON | 27 | 1,024 | 350 | 1,401 | 🔵 Pred |
| 306 | TASK-306 | Stress T | Ad campaign copy | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 550 | 1,594 | 🔵 Pred |
| 307 | TASK-307 | Stress T | SEO keyword research | Gemini 3.6 Flash / Pro | high | ON | 22 | 4,096 | 950 | 5,068 | 🔵 Pred |
| 308 | TASK-308 | Stress T | Social media content calendar | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 309 | TASK-309 | Stress T | Sales email sequences | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 310 | TASK-310 | Stress T | Customer persona development | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 311 | TASK-311 | Stress T | Competitive positioning | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 312 | TASK-312 | Stress T | Brand voice guidelines | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 313 | TASK-313 | Stress T | Email A/B test copy | ChatGPT (GPT-4o / GPT-5. | high | ON | 28 | 4,096 | 250 | 4,374 | 🔵 Pred |
| 314 | TASK-314 | Stress T | Influencer outreach | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 315 | TASK-315 | Stress T | Product launch messaging | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 316 | TASK-316 | Stress T | Job description writing | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 317 | TASK-317 | Stress T | Resume screening | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 318 | TASK-318 | Stress T | Interview question generation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 319 | TASK-319 | Stress T | Employee handbook drafting | ChatGPT (GPT-4o / GPT-5. | medium | ON | 18 | 1,024 | 350 | 1,392 | 🔵 Pred |
| 320 | TASK-320 | Stress T | Performance review writing | Claude 3.7 Sonnet | medium | ON | 29 | 1,024 | 450 | 1,503 | 🔵 Pred |
| 321 | TASK-321 | Stress T | Onboarding plan creation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 322 | TASK-322 | Stress T | Compensation benchmarking | Perplexity Pro | medium | ON | 26 | 1,024 | 850 | 1,900 | 🔵 Pred |
| 323 | TASK-323 | Stress T | DEI policy drafting | ChatGPT (GPT-4o / GPT-5. | medium | ON | 19 | 1,024 | 350 | 1,393 | 🔵 Pred |
| 324 | TASK-324 | Stress T | Exit interview analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 26 | 1,024 | 350 | 1,400 | 🔵 Pred |
| 325 | TASK-325 | Stress T | Org restructuring proposal | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 326 | TASK-326 | Stress T | Lesson plan creation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 327 | TASK-327 | Stress T | Quiz/exam generation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 328 | TASK-328 | Stress T | Concept explanation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 329 | TASK-329 | Stress T | Math/science homework help | ChatGPT (GPT-4o / GPT-5. | medium | ON | 16 | 1,024 | 350 | 1,390 | 🔵 Pred |
| 330 | TASK-330 | Stress T | Curriculum design | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 331 | TASK-331 | Stress T | Grading/feedback assistance | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 332 | TASK-332 | Stress T | Study guide creation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 333 | TASK-333 | Stress T | Language learning exercises | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 334 | TASK-334 | Stress T | Research methodology teaching | ChatGPT (GPT-4o / GPT-5. | medium | ON | 21 | 1,024 | 350 | 1,395 | 🔵 Pred |
| 335 | TASK-335 | Stress T | Thesis feedback | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 336 | TASK-336 | Stress T | Physics calculation | ChatGPT (GPT-4o / GPT-5. | medium | ON | 19 | 1,024 | 350 | 1,393 | 🔵 Pred |
| 337 | TASK-337 | Stress T | Chemical reaction analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 20 | 1,024 | 350 | 1,394 | 🔵 Pred |
| 338 | TASK-338 | Stress T | CAD/mechanical design | ChatGPT (GPT-4o / GPT-5. | medium | ON | 29 | 1,024 | 350 | 1,403 | 🔵 Pred |
| 339 | TASK-339 | Stress T | Environmental impact analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 340 | TASK-340 | Stress T | Materials science research | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 341 | TASK-341 | Stress T | Experimental design | ChatGPT (GPT-4o / GPT-5. | medium | ON | 25 | 1,024 | 350 | 1,399 | 🔵 Pred |
| 342 | TASK-342 | Stress T | Simulation data modeling | Claude 3.7 Sonnet | high | ON | 23 | 4,096 | 650 | 4,769 | 🔵 Pred |
| 343 | TASK-343 | Stress T | Robotics/control systems | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 344 | TASK-344 | Stress T | Renewable energy analysis | ChatGPT (GPT-4o / GPT-5. | medium | ON | 24 | 1,024 | 350 | 1,398 | 🔵 Pred |
| 345 | TASK-345 | Stress T | Structural engineering review | Gemini 3.6 Flash / Pro | low | OFF | 24 | 0 | 150 | 174 | 🔵 Pred |
| 346 | TASK-346 | Stress T | Code + slide deck | Gamma | medium | ON | 23 | 1,024 | 850 | 1,897 | 🔵 Pred |
| 347 | TASK-347 | Stress T | Summarize + translate | Claude 3.7 Sonnet | low | OFF | 14 | 0 | 18 | 32 | 🔵 Pred |
| 348 | TASK-348 | Stress T | Research + writing | Perplexity Pro | medium | ON | 23 | 1,024 | 1,995 | 3,042 | 🔵 Pred |
| 349 | TASK-349 | Stress T | Classify + summarize | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 350 | TASK-350 | Stress T | Data extraction + presentation | Gamma | medium | ON | 20 | 1,024 | 850 | 1,894 | 🔵 Pred |
| 351 | TASK-351 | Stress T | Creative + technical hybrid | DeepSeek V4 (Flash / Pro | medium | ON | 23 | 1,024 | 350 | 1,397 | 🔵 Pred |
| 352 | TASK-352 | Stress T | Multi-domain business plan | ChatGPT (GPT-4o / GPT-5. | high | ON | 24 | 4,096 | 250 | 4,370 | 🔵 Pred |
| 353 | TASK-353 | Stress T | Cross-functional project brief | ChatGPT (GPT-4o / GPT-5. | medium | ON | 27 | 1,024 | 350 | 1,401 | 🔵 Pred |
| 354 | TASK-354 | Stress T | Contradictory instructions | Claude 3.7 Sonnet | medium | ON | 16 | 1,024 | 66 | 1,106 | 🔵 Pred |
| 355 | TASK-355 | Stress T | No clear deliverable | ChatGPT (GPT-4o / GPT-5. | medium | ON | 11 | 1,024 | 350 | 1,385 | 🔵 Pred |
| 356 | TASK-356 | Stress T | One-word prompt | ChatGPT (GPT-4o / GPT-5. | medium | ON | 2 | 1,024 | 350 | 1,376 | 🔵 Pred |
| 357 | TASK-357 | Stress T | Extremely long rambling prompt | Claude 3.7 Sonnet | medium | ON | 128 | 1,024 | 350 | 1,502 | 🔵 Pred |
| 358 | TASK-358 | Stress T | Non-English prompt | ChatGPT (GPT-4o / GPT-5. | medium | ON | 16 | 1,024 | 350 | 1,390 | 🔵 Pred |
| 359 | TASK-359 | Stress T | Typo-heavy prompt | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 360 | TASK-360 | Stress T | Missing attachment reference | Gemini 3.6 Flash / Pro | high | ON | 16 | 4,096 | 950 | 5,062 | 🔵 Pred |
| 361 | TASK-361 | Stress T | Mixed languages prompt | Claude 3.7 Sonnet | medium | ON | 20 | 1,024 | 450 | 1,494 | 🔵 Pred |
| 362 | TASK-362 | Stress T | Real-time data request | Perplexity Pro | medium | ON | 18 | 1,024 | 850 | 1,892 | 🔵 Pred |
| 363 | TASK-363 | Stress T | Adversarial/trick prompt | ChatGPT (GPT-4o / GPT-5. | medium | ON | 22 | 1,024 | 350 | 1,396 | 🔵 Pred |
| 364 | TASK-364 | Stress T | Meta-prompt | Claude 3.7 Sonnet | high | ON | 22 | 4,096 | 750 | 4,868 | 🔵 Pred |
| 365 | TASK-365 | Stress T | Novel/unprecedented task | Claude Code / Cursor | high | ON | 27 | 4,096 | 350 | 4,473 | 🔵 Pred |

---
*Auto-generated by `evaluation/build_full_results.py`*
