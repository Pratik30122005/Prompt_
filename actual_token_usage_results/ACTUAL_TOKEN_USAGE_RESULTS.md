# Actual Token Usage Verification & Prediction Accuracy Results

> Empirical verification results and model prediction accuracy across all **365 benchmark tasks** (TASK-1 to TASK-365).

## 🏆 Overall Model Accuracy Report

| Accuracy Metric | Value | Status |
|-----------------|-------|--------|
| **Overall Average Per-Task Accuracy** | **92.7%** | 🎯 High Precision |
| **Aggregate Token Volume Accuracy** | **99.3%** | 📊 Bounded Calibration |
| **Prediction Within Bounds Rate** | **83.0%** (303/365 tasks) | ✅ Validated |
| **Total Tasks Benchmark Execution** | **365 tasks** | 🚀 100% Covered |
| **Total Verified Actual Tokens Used** | **985,050 tokens** | ⚡ Measured |

## Task-by-Task Token Usage & Accuracy Results (365 Tasks)

| Task ID | Category | Suggested Model | Predicted Total (Exp) | Actual Input | Actual Think | Actual Output | Actual Total | Accuracy (%) | Within Bounds | Latency |
|---------|----------|-----------------|-----------------------|--------------|--------------|---------------|--------------|--------------|---------------|---------|
| TASK-1 | Coding & Automation | DeepSeek V4 (Flash / P | 1,396 | 20 | 575 | 1,021 | 1,616 | **95.3%** | ✅ Yes | 9.69s |
| TASK-2 | Summarization (Constra | Perplexity Pro | 1,897 | 24 | 421 | 213 | 658 | **34.7%** | ⚠️ No | 5.36s |
| TASK-3 | Web Research & Analysi | Perplexity Pro | 1,890 | 17 | 627 | 1,133 | 1,777 | **94.0%** | ✅ Yes | 11.17s |
| TASK-4 | Math & Computation | ChatGPT (GPT-5o / O3-M | 1,401 | 28 | 448 | 542 | 1,018 | **72.7%** | ✅ Yes | 4.44s |
| TASK-5 | Creative Writing (Cons | Claude 3.7 Sonnet / Op | 1,446 | 21 | 701 | 408 | 1,130 | **78.2%** | ✅ Yes | 6.03s |
| TASK-6 | A | ChatGPT (GPT-5o / O3-M | 1,401 | 26 | 886 | 280 | 1,192 | **85.1%** | ⚠️ No | 6.14s |
| TASK-7 | A | ChatGPT (GPT-5o / O3-M | 1,390 | 15 | 1,044 | 311 | 1,370 | **98.6%** | ✅ Yes | 6.97s |
| TASK-8 | A | ChatGPT (GPT-5o / O3-M | 4,371 | 25 | 4,706 | 239 | 4,970 | **86.3%** | ⚠️ No | 20.97s |
| TASK-9 | A | ChatGPT (GPT-5o / O3-M | 1,412 | 37 | 1,089 | 337 | 1,463 | **96.4%** | ✅ Yes | 7.29s |
| TASK-10 | A | ChatGPT (GPT-5o / O3-M | 1,400 | 27 | 889 | 330 | 1,246 | **89.0%** | ✅ Yes | 6.43s |
| TASK-11 | A | Gamma App | 1,904 | 29 | 1,128 | 944 | 2,101 | **89.7%** | ✅ Yes | 12.39s |
| TASK-12 | A | ChatGPT (GPT-5o / O3-M | 1,408 | 35 | 1,079 | 308 | 1,422 | **99.0%** | ✅ Yes | 7.04s |
| TASK-13 | A | ChatGPT (GPT-5o / O3-M | 1,411 | 36 | 978 | 367 | 1,381 | **97.9%** | ✅ Yes | 7.13s |
| TASK-14 | A | ChatGPT (GPT-5o / O3-M | 1,402 | 29 | 1,158 | 346 | 1,533 | **90.7%** | ✅ Yes | 7.70s |
| TASK-15 | A | ChatGPT (GPT-5o / O3-M | 1,419 | 46 | 1,062 | 328 | 1,436 | **98.8%** | ✅ Yes | 7.13s |
| TASK-16 | B | DeepSeek V4 (Flash / P | 1,400 | 27 | 903 | 408 | 1,338 | **95.6%** | ✅ Yes | 7.07s |
| TASK-17 | B | DeepSeek V4 (Flash / P | 1,399 | 25 | 902 | 309 | 1,236 | **88.3%** | ✅ Yes | 6.50s |
| TASK-18 | B | DeepSeek V4 (Flash / P | 1,402 | 30 | 873 | 318 | 1,221 | **87.1%** | ✅ Yes | 6.40s |
| TASK-19 | B | DeepSeek V4 (Flash / P | 1,407 | 32 | 964 | 340 | 1,336 | **95.0%** | ✅ Yes | 6.91s |
| TASK-20 | B | DeepSeek V4 (Flash / P | 1,400 | 25 | 1,067 | 367 | 1,459 | **95.8%** | ✅ Yes | 7.44s |
| TASK-21 | B | DeepSeek V4 (Flash / P | 1,403 | 29 | 813 | 374 | 1,216 | **86.7%** | ✅ Yes | 6.55s |
| TASK-22 | B | DeepSeek V4 (Flash / P | 1,402 | 28 | 1,026 | 391 | 1,445 | **96.9%** | ✅ Yes | 7.54s |
| TASK-23 | B | DeepSeek V4 (Flash / P | 1,403 | 29 | 1,061 | 372 | 1,462 | **95.8%** | ✅ Yes | 7.40s |
| TASK-24 | B | Claude Code | 4,823 | 26 | 3,416 | 723 | 4,165 | **86.4%** | ⚠️ No | 19.74s |
| TASK-25 | B | DeepSeek V4 (Flash / P | 1,398 | 24 | 1,003 | 352 | 1,379 | **98.6%** | ✅ Yes | 7.04s |
| TASK-26 | C | ChatGPT (GPT-5o / O3-M | 1,407 | 34 | 959 | 267 | 1,260 | **89.6%** | ✅ Yes | 6.28s |
| TASK-27 | C | ChatGPT (GPT-5o / O3-M | 1,402 | 28 | 936 | 350 | 1,314 | **93.7%** | ✅ Yes | 6.77s |
| TASK-28 | C | Claude 3.7 Sonnet / Op | 1,590 | 15 | 1,071 | 506 | 1,592 | **99.9%** | ✅ Yes | 8.55s |
| TASK-29 | C | Claude 3.7 Sonnet / Op | 1,712 | 25 | 955 | 768 | 1,748 | **97.9%** | ✅ Yes | 10.26s |
| TASK-30 | C | Claude 3.7 Sonnet / Op | 1,596 | 24 | 1,104 | 472 | 1,600 | **99.7%** | ✅ Yes | 8.47s |
| TASK-31 | C | Claude 3.7 Sonnet / Op | 1,594 | 22 | 1,115 | 571 | 1,708 | **92.8%** | ✅ Yes | 9.23s |
| TASK-32 | C | ChatGPT (GPT-5o / O3-M | 3,707 | 25 | 931 | 2,471 | 3,427 | **92.4%** | ✅ Yes | 23.66s |
| TASK-33 | C | Claude 3.7 Sonnet / Op | 4,865 | 18 | 3,549 | 674 | 4,241 | **87.2%** | ⚠️ No | 19.74s |
| TASK-34 | C | Claude 3.7 Sonnet / Op | 1,498 | 26 | 852 | 386 | 1,264 | **84.4%** | ✅ Yes | 6.87s |
| TASK-35 | C | Claude 3.7 Sonnet / Op | 1,596 | 24 | 921 | 555 | 1,500 | **94.0%** | ✅ Yes | 8.29s |
| TASK-36 | D | Claude 3.7 Sonnet / Op | 4,873 | 29 | 4,112 | 669 | 4,810 | **98.7%** | ✅ Yes | 22.14s |
| TASK-37 | D | Perplexity Pro | 1,911 | 37 | 717 | 857 | 1,611 | **84.3%** | ✅ Yes | 9.91s |
| TASK-38 | D | DeepSeek V4 (Flash / P | 1,411 | 36 | 983 | 364 | 1,383 | **98.0%** | ✅ Yes | 7.08s |
| TASK-39 | D | Claude 3.7 Sonnet / Op | 4,873 | 28 | 3,731 | 767 | 4,526 | **92.9%** | ✅ Yes | 21.31s |
| TASK-40 | D | ChatGPT (GPT-5o / O3-M | 1,398 | 23 | 1,039 | 348 | 1,410 | **99.1%** | ✅ Yes | 7.13s |
| TASK-41 | D | Claude 3.7 Sonnet / Op | 4,873 | 28 | 3,965 | 880 | 4,873 | **100.0%** | ✅ Yes | 23.24s |
| TASK-42 | D | Perplexity Pro | 1,898 | 23 | 1,103 | 908 | 2,034 | **92.8%** | ✅ Yes | 12.09s |
| TASK-43 | D | ChatGPT (GPT-5o / O3-M | 1,403 | 29 | 903 | 359 | 1,291 | **92.0%** | ✅ Yes | 6.83s |
| TASK-44 | D | ChatGPT (GPT-5o / O3-M | 1,407 | 34 | 1,026 | 390 | 1,450 | **96.9%** | ✅ Yes | 7.41s |
| TASK-45 | D | Claude 3.7 Sonnet / Op | 4,883 | 38 | 4,726 | 617 | 5,381 | **89.8%** | ✅ Yes | 24.18s |
| TASK-46 | E | ChatGPT (GPT-5o / O3-M | 4,370 | 26 | 4,154 | 232 | 4,412 | **99.0%** | ✅ Yes | 18.75s |
| TASK-47 | E | ChatGPT (GPT-5o / O3-M | 4,372 | 25 | 4,522 | 233 | 4,780 | **90.7%** | ⚠️ No | 20.34s |
| TASK-48 | E | ChatGPT (GPT-5o / O3-M | 4,396 | 52 | 4,566 | 221 | 4,839 | **89.9%** | ⚠️ No | 20.29s |
| TASK-49 | E | Claude Code | 4,477 | 32 | 4,501 | 382 | 4,915 | **90.2%** | ⚠️ No | 21.30s |
| TASK-50 | E | Claude 3.7 Sonnet / Op | 1,400 | 26 | 1,092 | 252 | 1,370 | **97.9%** | ✅ Yes | 6.67s |
| TASK-51 | E | ChatGPT (GPT-5o / O3-M | 4,374 | 29 | 3,409 | 239 | 3,677 | **84.1%** | ⚠️ No | 15.73s |
| TASK-52 | E | ChatGPT (GPT-5o / O3-M | 4,376 | 31 | 3,840 | 294 | 4,165 | **95.2%** | ⚠️ No | 17.97s |
| TASK-53 | E | ChatGPT (GPT-5o / O3-M | 1,404 | 29 | 969 | 329 | 1,327 | **94.5%** | ✅ Yes | 6.76s |
| TASK-54 | E | ChatGPT (GPT-5o / O3-M | 1,403 | 28 | 967 | 292 | 1,287 | **91.7%** | ✅ Yes | 6.36s |
| TASK-55 | E | ChatGPT (GPT-5o / O3-M | 4,381 | 35 | 3,973 | 256 | 4,264 | **97.3%** | ✅ Yes | 18.20s |
| TASK-56 | F | Perplexity Pro | 1,900 | 25 | 1,090 | 786 | 1,901 | **99.9%** | ✅ Yes | 10.92s |
| TASK-57 | F | Perplexity Pro | 1,901 | 28 | 1,038 | 872 | 1,938 | **98.1%** | ✅ Yes | 11.51s |
| TASK-58 | F | DeepSeek V4 (Flash / P | 1,397 | 23 | 1,059 | 321 | 1,403 | **99.6%** | ✅ Yes | 7.12s |
| TASK-59 | F | Perplexity Pro | 1,902 | 29 | 1,011 | 754 | 1,794 | **94.3%** | ✅ Yes | 10.50s |
| TASK-60 | F | Perplexity Pro | 1,896 | 22 | 1,071 | 896 | 1,989 | **95.1%** | ✅ Yes | 11.62s |
| TASK-61 | F | Perplexity Pro | 1,900 | 26 | 1,071 | 762 | 1,859 | **97.8%** | ✅ Yes | 10.79s |
| TASK-62 | F | Perplexity Pro | 1,901 | 26 | 941 | 872 | 1,839 | **96.7%** | ✅ Yes | 11.01s |
| TASK-63 | F | Perplexity Pro | 1,903 | 31 | 867 | 877 | 1,775 | **93.3%** | ✅ Yes | 10.77s |
| TASK-64 | F | ChatGPT (GPT-5o / O3-M | 1,399 | 25 | 1,235 | 338 | 1,598 | **85.8%** | ✅ Yes | 8.07s |
| TASK-65 | F | Perplexity Pro | 1,893 | 18 | 978 | 1,112 | 2,108 | **88.6%** | ✅ Yes | 13.21s |
| TASK-66 | G | Claude 3.7 Sonnet / Op | 4,873 | 29 | 4,713 | 731 | 5,473 | **87.7%** | ✅ Yes | 24.93s |
| TASK-67 | G | Claude 3.7 Sonnet / Op | 1,501 | 28 | 1,141 | 454 | 1,623 | **91.9%** | ✅ Yes | 8.38s |
| TASK-68 | G | Claude 3.7 Sonnet / Op | 1,498 | 25 | 940 | 397 | 1,362 | **90.9%** | ✅ Yes | 7.13s |
| TASK-69 | G | Claude 3.7 Sonnet / Op | 1,500 | 26 | 869 | 447 | 1,342 | **89.5%** | ✅ Yes | 7.27s |
| TASK-70 | G | Claude 3.7 Sonnet / Op | 1,495 | 23 | 923 | 510 | 1,456 | **97.4%** | ✅ Yes | 8.06s |
| TASK-71 | G | Claude 3.7 Sonnet / Op | 1,500 | 27 | 954 | 452 | 1,433 | **95.5%** | ✅ Yes | 7.83s |
| TASK-72 | G | Claude 3.7 Sonnet / Op | 1,503 | 29 | 1,021 | 439 | 1,489 | **99.1%** | ✅ Yes | 7.95s |
| TASK-73 | G | Perplexity Pro | 1,908 | 36 | 1,320 | 886 | 2,242 | **82.5%** | ✅ Yes | 12.72s |
| TASK-74 | G | Claude 3.7 Sonnet / Op | 1,502 | 27 | 871 | 476 | 1,374 | **91.5%** | ✅ Yes | 7.52s |
| TASK-75 | G | Claude 3.7 Sonnet / Op | 1,497 | 24 | 934 | 473 | 1,431 | **95.6%** | ✅ Yes | 7.89s |
| TASK-76 | H | Claude 3.7 Sonnet / Op | 1,601 | 29 | 967 | 604 | 1,600 | **99.9%** | ✅ Yes | 9.05s |
| TASK-77 | H | Claude 3.7 Sonnet / Op | 1,596 | 21 | 786 | 547 | 1,354 | **84.8%** | ✅ Yes | 7.87s |
| TASK-78 | H | Claude 3.7 Sonnet / Op | 1,607 | 34 | 846 | 565 | 1,445 | **89.9%** | ✅ Yes | 8.32s |
| TASK-79 | H | Claude 3.7 Sonnet / Op | 3,044 | 26 | 901 | 2,215 | 3,142 | **96.8%** | ✅ Yes | 21.69s |
| TASK-80 | H | ChatGPT (GPT-5o / O3-M | 1,393 | 18 | 1,139 | 292 | 1,449 | **96.0%** | ✅ Yes | 7.12s |
| TASK-81 | H | Claude 3.7 Sonnet / Op | 1,592 | 17 | 1,168 | 446 | 1,631 | **97.6%** | ✅ Yes | 8.57s |
| TASK-82 | H | Claude 3.7 Sonnet / Op | 1,601 | 26 | 1,026 | 614 | 1,666 | **95.9%** | ✅ Yes | 9.38s |
| TASK-83 | H | Claude 3.7 Sonnet / Op | 1,603 | 31 | 881 | 576 | 1,488 | **92.8%** | ✅ Yes | 8.57s |
| TASK-84 | H | Claude 3.7 Sonnet / Op | 1,590 | 18 | 982 | 552 | 1,552 | **97.6%** | ✅ Yes | 8.55s |
| TASK-85 | H | Claude 3.7 Sonnet / Op | 1,602 | 27 | 939 | 594 | 1,560 | **97.4%** | ✅ Yes | 8.86s |
| TASK-86 | I | DeepSeek V4 (Flash / P | 1,396 | 23 | 939 | 370 | 1,332 | **95.4%** | ✅ Yes | 7.13s |
| TASK-87 | I | Claude 3.7 Sonnet / Op | 57 | 26 | 0 | 32 | 58 | **98.2%** | ⚠️ No | 0.47s |
| TASK-88 | I | Claude 3.7 Sonnet / Op | 46 | 20 | 0 | 27 | 47 | **97.8%** | ⚠️ No | 0.58s |
| TASK-89 | I | Claude 3.7 Sonnet / Op | 46 | 22 | 0 | 27 | 49 | **93.5%** | ⚠️ No | 0.60s |
| TASK-90 | I | Claude 3.7 Sonnet / Op | 50 | 21 | 0 | 26 | 47 | **94.0%** | ⚠️ No | 0.42s |
| TASK-91 | I | Claude 3.7 Sonnet / Op | 46 | 21 | 0 | 25 | 46 | **100.0%** | ⚠️ No | 0.47s |
| TASK-92 | I | Perplexity Pro | 1,899 | 26 | 967 | 796 | 1,789 | **94.2%** | ✅ Yes | 10.60s |
| TASK-93 | I | ChatGPT (GPT-5o / O3-M | 1,399 | 26 | 851 | 362 | 1,239 | **88.6%** | ✅ Yes | 6.52s |
| TASK-94 | I | Claude 3.7 Sonnet / Op | 41 | 20 | 0 | 20 | 40 | **97.6%** | ⚠️ No | 0.53s |
| TASK-95 | I | Claude 3.7 Sonnet / Op | 55 | 25 | 0 | 29 | 54 | **98.2%** | ⚠️ No | 0.47s |
| TASK-96 | J | Gemini 3.1 Flash / Pro | 176 | 26 | 0 | 152 | 178 | **98.9%** | ✅ Yes | 1.41s |
| TASK-97 | J | Gemini 3.1 Flash / Pro | 174 | 26 | 0 | 136 | 162 | **93.1%** | ✅ Yes | 1.34s |
| TASK-98 | J | Gemini 3.1 Flash / Pro | 177 | 26 | 0 | 146 | 172 | **97.2%** | ✅ Yes | 1.53s |
| TASK-99 | J | ChatGPT (GPT-5o / O3-M | 1,400 | 26 | 855 | 374 | 1,255 | **89.6%** | ✅ Yes | 6.63s |
| TASK-100 | J | Gemini 3.1 Flash / Pro | 180 | 32 | 0 | 145 | 177 | **98.3%** | ✅ Yes | 1.58s |
| TASK-101 | J | Gemini 3.1 Flash / Pro | 178 | 30 | 0 | 134 | 164 | **92.1%** | ✅ Yes | 1.41s |
| TASK-102 | J | Claude 3.7 Sonnet / Op | 1,499 | 24 | 845 | 409 | 1,278 | **85.3%** | ✅ Yes | 6.82s |
| TASK-103 | J | ChatGPT (GPT-5o / O3-M | 1,403 | 28 | 962 | 341 | 1,331 | **94.9%** | ✅ Yes | 6.82s |
| TASK-104 | J | ChatGPT (GPT-5o / O3-M | 1,413 | 40 | 1,102 | 389 | 1,531 | **91.6%** | ✅ Yes | 7.90s |
| TASK-105 | J | Gemini 3.1 Flash / Pro | 180 | 30 | 0 | 143 | 173 | **96.1%** | ✅ Yes | 1.50s |
| TASK-106 | K | Gemini 3.1 Flash / Pro | 1,504 | 31 | 922 | 486 | 1,439 | **95.7%** | ✅ Yes | 7.82s |
| TASK-107 | K | Gemini 3.1 Flash / Pro | 1,506 | 31 | 1,015 | 431 | 1,477 | **98.1%** | ✅ Yes | 7.83s |
| TASK-108 | K | Gemini 3.1 Flash / Pro | 1,498 | 26 | 1,003 | 420 | 1,449 | **96.7%** | ✅ Yes | 7.81s |
| TASK-109 | K | ChatGPT (GPT-5o / O3-M | 1,395 | 20 | 1,126 | 451 | 1,597 | **85.5%** | ✅ Yes | 8.31s |
| TASK-110 | K | Claude 3.7 Sonnet / Op | 1,497 | 25 | 1,080 | 393 | 1,498 | **99.9%** | ✅ Yes | 7.71s |
| TASK-111 | K | ChatGPT (GPT-5o / O3-M | 4,371 | 24 | 4,546 | 257 | 4,827 | **89.6%** | ⚠️ No | 20.67s |
| TASK-112 | K | Claude 3.7 Sonnet / Op | 1,494 | 19 | 1,010 | 426 | 1,455 | **97.4%** | ✅ Yes | 7.88s |
| TASK-113 | K | ChatGPT (GPT-5o / O3-M | 1,397 | 25 | 1,001 | 309 | 1,335 | **95.6%** | ✅ Yes | 6.81s |
| TASK-114 | K | Gemini 3.1 Flash / Pro | 1,497 | 22 | 885 | 500 | 1,407 | **94.0%** | ✅ Yes | 7.89s |
| TASK-115 | K | DeepSeek V4 (Flash / P | 1,398 | 23 | 1,241 | 336 | 1,600 | **85.6%** | ✅ Yes | 8.05s |
| TASK-116 | L | Claude 3.7 Sonnet / Op | 4,770 | 23 | 4,059 | 711 | 4,793 | **99.5%** | ✅ Yes | 22.28s |
| TASK-117 | L | Claude 3.7 Sonnet / Op | 4,770 | 25 | 3,958 | 631 | 4,614 | **96.7%** | ✅ Yes | 21.07s |
| TASK-118 | L | Claude 3.7 Sonnet / Op | 4,777 | 31 | 4,819 | 518 | 5,368 | **87.6%** | ✅ Yes | 23.71s |
| TASK-119 | L | ChatGPT (GPT-5o / O3-M | 1,411 | 38 | 1,118 | 314 | 1,470 | **95.8%** | ✅ Yes | 7.46s |
| TASK-120 | L | ChatGPT (GPT-5o / O3-M | 1,408 | 36 | 1,163 | 342 | 1,541 | **90.6%** | ✅ Yes | 7.79s |
| TASK-121 | L | Perplexity Pro | 1,905 | 33 | 1,010 | 683 | 1,726 | **90.6%** | ✅ Yes | 9.84s |
| TASK-122 | L | Claude Code | 4,474 | 28 | 4,605 | 322 | 4,955 | **89.2%** | ⚠️ No | 21.43s |
| TASK-123 | L | ChatGPT (GPT-5o / O3-M | 1,394 | 22 | 953 | 343 | 1,318 | **94.5%** | ✅ Yes | 6.85s |
| TASK-124 | L | ChatGPT (GPT-5o / O3-M | 4,375 | 30 | 3,990 | 238 | 4,258 | **97.3%** | ✅ Yes | 18.15s |
| TASK-125 | L | ChatGPT (GPT-5o / O3-M | 1,410 | 36 | 893 | 336 | 1,265 | **89.7%** | ✅ Yes | 6.53s |
| TASK-126 | M | Gamma App | 1,907 | 35 | 1,184 | 849 | 2,068 | **91.6%** | ✅ Yes | 11.77s |
| TASK-127 | M | Gamma App | 1,895 | 22 | 1,009 | 986 | 2,017 | **93.6%** | ✅ Yes | 12.20s |
| TASK-128 | M | Gamma App | 1,900 | 27 | 1,112 | 812 | 1,951 | **97.3%** | ✅ Yes | 11.26s |
| TASK-129 | M | Claude Code | 4,468 | 22 | 4,918 | 303 | 5,243 | **82.7%** | ⚠️ No | 22.32s |
| TASK-130 | M | Gamma App | 1,897 | 24 | 1,331 | 826 | 2,181 | **85.0%** | ✅ Yes | 12.24s |
| TASK-131 | M | Gamma App | 1,895 | 20 | 1,005 | 868 | 1,893 | **99.9%** | ✅ Yes | 11.23s |
| TASK-132 | M | ChatGPT (GPT-5o / O3-M | 1,401 | 28 | 1,011 | 305 | 1,344 | **95.9%** | ✅ Yes | 6.75s |
| TASK-133 | M | Gamma App | 1,899 | 26 | 914 | 939 | 1,879 | **98.9%** | ✅ Yes | 11.33s |
| TASK-134 | M | Gamma App | 1,903 | 31 | 1,100 | 889 | 2,020 | **93.9%** | ✅ Yes | 11.73s |
| TASK-135 | M | Gamma App | 1,894 | 21 | 1,158 | 977 | 2,156 | **86.2%** | ✅ Yes | 12.78s |
| TASK-136 | N | ChatGPT (GPT-5o / O3-M | 1,376 | 1 | 952 | 361 | 1,314 | **95.5%** | ✅ Yes | 6.83s |
| TASK-137 | N | ChatGPT (GPT-5o / O3-M | 1,378 | 5 | 962 | 259 | 1,226 | **89.0%** | ✅ Yes | 6.29s |
| TASK-138 | N | ChatGPT (GPT-5o / O3-M | 7,691 | 18 | 1,099 | 7,024 | 8,141 | **94.1%** | ✅ Yes | 60.97s |
| TASK-139 | N | DeepSeek V4 (Flash / P | 1,397 | 25 | 1,164 | 341 | 1,530 | **90.5%** | ✅ Yes | 7.76s |
| TASK-140 | N | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 1,299 | 372 | 1,693 | **78.7%** | ✅ Yes | 8.55s |
| TASK-141 | N | ChatGPT (GPT-5o / O3-M | 1,378 | 3 | 967 | 312 | 1,282 | **93.0%** | ✅ Yes | 6.55s |
| TASK-142 | N | ChatGPT (GPT-5o / O3-M | 1,391 | 19 | 916 | 387 | 1,322 | **95.0%** | ✅ Yes | 6.96s |
| TASK-143 | N | ChatGPT (GPT-5o / O3-M | 1,388 | 13 | 1,077 | 377 | 1,467 | **94.3%** | ✅ Yes | 7.49s |
| TASK-144 | N | Claude 3.7 Sonnet / Op | 4,865 | 18 | 4,637 | 734 | 5,389 | **89.2%** | ✅ Yes | 24.82s |
| TASK-145 | N | ChatGPT (GPT-5o / O3-M | 1,395 | 21 | 987 | 349 | 1,357 | **97.3%** | ✅ Yes | 7.10s |
| TASK-146 | O | Perplexity Pro | 3,709 | 27 | 1,220 | 3,473 | 4,720 | **72.7%** | ⚠️ No | 32.90s |
| TASK-147 | O | Gamma App | 1,897 | 24 | 917 | 773 | 1,714 | **90.4%** | ✅ Yes | 10.29s |
| TASK-148 | O | Claude 3.7 Sonnet / Op | 1,507 | 34 | 1,331 | 423 | 1,788 | **81.4%** | ✅ Yes | 8.93s |
| TASK-149 | O | Claude Code | 4,826 | 29 | 3,659 | 605 | 4,293 | **89.0%** | ⚠️ No | 19.93s |
| TASK-150 | O | Claude Code | 4,824 | 28 | 3,781 | 752 | 4,561 | **94.5%** | ✅ Yes | 21.34s |
| TASK-151 | O | Claude 3.7 Sonnet / Op | 62 | 26 | 0 | 36 | 62 | **100.0%** | ⚠️ No | 0.70s |
| TASK-152 | O | Claude Code | 4,468 | 22 | 3,769 | 374 | 4,165 | **93.2%** | ⚠️ No | 18.44s |
| TASK-153 | O | Perplexity Pro | 1,905 | 33 | 1,007 | 858 | 1,898 | **99.6%** | ✅ Yes | 11.12s |
| TASK-154 | O | Claude Code | 4,483 | 36 | 4,288 | 352 | 4,676 | **95.7%** | ✅ Yes | 20.44s |
| TASK-155 | O | Claude 3.7 Sonnet / Op | 4,875 | 31 | 4,026 | 784 | 4,841 | **99.3%** | ✅ Yes | 22.81s |
| TASK-156 | A | Claude Code | 4,473 | 28 | 4,194 | 306 | 4,528 | **98.8%** | ✅ Yes | 19.54s |
| TASK-157 | A | DeepSeek V4 (Flash / P | 1,394 | 21 | 962 | 318 | 1,301 | **93.3%** | ✅ Yes | 6.66s |
| TASK-158 | A | DeepSeek V4 (Flash / P | 1,399 | 24 | 1,237 | 401 | 1,662 | **81.2%** | ✅ Yes | 8.37s |
| TASK-159 | A | DeepSeek V4 (Flash / P | 1,392 | 20 | 1,164 | 376 | 1,560 | **87.9%** | ✅ Yes | 8.02s |
| TASK-160 | A | Claude Code | 4,822 | 27 | 3,912 | 668 | 4,607 | **95.5%** | ✅ Yes | 21.42s |
| TASK-161 | A | DeepSeek V4 (Flash / P | 1,393 | 18 | 968 | 334 | 1,320 | **94.8%** | ✅ Yes | 6.70s |
| TASK-162 | A | Claude Code | 4,464 | 19 | 4,339 | 288 | 4,646 | **95.9%** | ✅ Yes | 19.81s |
| TASK-163 | A | Claude 3.7 Sonnet / Op | 4,769 | 24 | 4,227 | 648 | 4,899 | **97.3%** | ✅ Yes | 22.44s |
| TASK-164 | A | Claude Code | 4,810 | 14 | 4,547 | 694 | 5,255 | **90.7%** | ✅ Yes | 23.95s |
| TASK-165 | A | DeepSeek V4 (Flash / P | 1,396 | 22 | 1,091 | 370 | 1,483 | **93.8%** | ✅ Yes | 7.52s |
| TASK-166 | B | ChatGPT (GPT-5o / O3-M | 4,371 | 26 | 4,644 | 229 | 4,899 | **87.9%** | ⚠️ No | 20.76s |
| TASK-167 | B | DeepSeek V4 (Flash / P | 1,402 | 27 | 818 | 314 | 1,159 | **82.7%** | ⚠️ No | 6.04s |
| TASK-168 | B | ChatGPT (GPT-5o / O3-M | 4,366 | 21 | 3,861 | 292 | 4,174 | **95.6%** | ⚠️ No | 18.19s |
| TASK-169 | B | ChatGPT (GPT-5o / O3-M | 1,398 | 24 | 835 | 357 | 1,216 | **87.0%** | ✅ Yes | 6.54s |
| TASK-170 | B | ChatGPT (GPT-5o / O3-M | 4,366 | 22 | 4,250 | 220 | 4,492 | **97.1%** | ✅ Yes | 19.01s |
| TASK-171 | B | ChatGPT (GPT-5o / O3-M | 4,391 | 44 | 3,528 | 243 | 3,815 | **86.9%** | ⚠️ No | 16.26s |
| TASK-172 | B | ChatGPT (GPT-5o / O3-M | 4,369 | 25 | 5,052 | 235 | 5,312 | **78.4%** | ⚠️ No | 22.39s |
| TASK-173 | B | ChatGPT (GPT-5o / O3-M | 4,370 | 26 | 3,655 | 262 | 3,943 | **90.2%** | ⚠️ No | 17.12s |
| TASK-174 | B | Gemini 3.1 Flash / Pro | 1,494 | 21 | 1,061 | 469 | 1,551 | **96.2%** | ✅ Yes | 8.17s |
| TASK-175 | B | Claude Code | 4,469 | 22 | 4,795 | 361 | 5,178 | **84.1%** | ⚠️ No | 22.34s |
| TASK-176 | C | Perplexity Pro | 1,894 | 19 | 892 | 839 | 1,750 | **92.4%** | ✅ Yes | 10.51s |
| TASK-177 | C | ChatGPT (GPT-5o / O3-M | 1,392 | 19 | 758 | 274 | 1,051 | **75.5%** | ⚠️ No | 5.52s |
| TASK-178 | C | Perplexity Pro | 1,895 | 21 | 1,156 | 1,016 | 2,193 | **84.3%** | ✅ Yes | 13.14s |
| TASK-179 | C | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 911 | 320 | 1,253 | **89.8%** | ✅ Yes | 6.58s |
| TASK-180 | C | Perplexity Pro | 1,897 | 22 | 1,019 | 902 | 1,943 | **97.6%** | ✅ Yes | 11.71s |
| TASK-181 | C | Perplexity Pro | 1,894 | 21 | 1,230 | 821 | 2,072 | **90.6%** | ✅ Yes | 11.71s |
| TASK-182 | C | ChatGPT (GPT-5o / O3-M | 1,395 | 20 | 990 | 341 | 1,351 | **96.8%** | ✅ Yes | 6.94s |
| TASK-183 | C | Perplexity Pro | 1,895 | 22 | 1,219 | 835 | 2,076 | **90.4%** | ✅ Yes | 11.87s |
| TASK-184 | C | Perplexity Pro | 1,903 | 28 | 968 | 866 | 1,862 | **97.8%** | ✅ Yes | 11.10s |
| TASK-185 | C | ChatGPT (GPT-5o / O3-M | 1,398 | 24 | 1,200 | 352 | 1,576 | **87.3%** | ✅ Yes | 7.98s |
| TASK-186 | D | Claude 3.7 Sonnet / Op | 1,495 | 23 | 1,037 | 313 | 1,373 | **91.8%** | ✅ Yes | 6.91s |
| TASK-187 | D | Claude 3.7 Sonnet / Op | 1,496 | 23 | 1,064 | 456 | 1,543 | **96.9%** | ✅ Yes | 8.15s |
| TASK-188 | D | Claude 3.7 Sonnet / Op | 1,495 | 23 | 859 | 570 | 1,452 | **97.1%** | ✅ Yes | 8.40s |
| TASK-189 | D | Claude 3.7 Sonnet / Op | 1,178 | 20 | 1,151 | 143 | 1,314 | **88.5%** | ⚠️ No | 5.93s |
| TASK-190 | D | Claude 3.7 Sonnet / Op | 1,496 | 21 | 960 | 518 | 1,499 | **99.8%** | ✅ Yes | 8.35s |
| TASK-191 | D | Claude 3.7 Sonnet / Op | 1,495 | 20 | 1,077 | 424 | 1,521 | **98.3%** | ✅ Yes | 7.89s |
| TASK-192 | D | Claude 3.7 Sonnet / Op | 4,565 | 19 | 3,525 | 403 | 3,947 | **86.5%** | ⚠️ No | 17.70s |
| TASK-193 | D | Claude 3.7 Sonnet / Op | 4,868 | 21 | 5,201 | 773 | 5,995 | **76.8%** | ⚠️ No | 27.18s |
| TASK-194 | D | Claude 3.7 Sonnet / Op | 1,497 | 23 | 1,102 | 433 | 1,558 | **95.9%** | ✅ Yes | 8.22s |
| TASK-195 | D | Claude 3.7 Sonnet / Op | 1,494 | 20 | 1,270 | 414 | 1,704 | **85.9%** | ✅ Yes | 8.82s |
| TASK-196 | E | Claude 3.7 Sonnet / Op | 1,712 | 25 | 1,130 | 699 | 1,854 | **91.7%** | ✅ Yes | 10.39s |
| TASK-197 | E | ChatGPT (GPT-5o / O3-M | 1,394 | 21 | 1,142 | 337 | 1,500 | **92.4%** | ✅ Yes | 7.47s |
| TASK-198 | E | Claude 3.7 Sonnet / Op | 1,595 | 21 | 1,017 | 541 | 1,579 | **99.0%** | ✅ Yes | 8.56s |
| TASK-199 | E | Claude 3.7 Sonnet / Op | 1,593 | 19 | 892 | 593 | 1,504 | **94.4%** | ✅ Yes | 8.59s |
| TASK-200 | E | Claude 3.7 Sonnet / Op | 2,376 | 23 | 1,179 | 1,266 | 2,468 | **96.1%** | ✅ Yes | 15.11s |
| TASK-201 | E | ChatGPT (GPT-5o / O3-M | 1,390 | 15 | 997 | 386 | 1,398 | **99.4%** | ✅ Yes | 7.25s |
| TASK-202 | E | Claude 3.7 Sonnet / Op | 1,454 | 32 | 1,191 | 485 | 1,708 | **82.5%** | ⚠️ No | 8.95s |
| TASK-203 | E | Claude 3.7 Sonnet / Op | 1,600 | 25 | 954 | 645 | 1,624 | **98.5%** | ✅ Yes | 9.25s |
| TASK-204 | E | Claude 3.7 Sonnet / Op | 1,596 | 23 | 961 | 471 | 1,455 | **91.2%** | ✅ Yes | 7.94s |
| TASK-205 | E | Claude 3.7 Sonnet / Op | 1,592 | 17 | 1,045 | 541 | 1,603 | **99.3%** | ✅ Yes | 8.69s |
| TASK-206 | F | Gamma App | 1,899 | 27 | 1,042 | 884 | 1,953 | **97.2%** | ✅ Yes | 11.50s |
| TASK-207 | F | Gamma App | 1,895 | 20 | 980 | 897 | 1,897 | **99.9%** | ✅ Yes | 11.46s |
| TASK-208 | F | Gamma App | 1,893 | 18 | 1,240 | 807 | 2,065 | **90.9%** | ✅ Yes | 11.72s |
| TASK-209 | F | ChatGPT (GPT-5o / O3-M | 1,391 | 17 | 1,245 | 398 | 1,660 | **80.7%** | ✅ Yes | 8.35s |
| TASK-210 | F | Gamma App | 1,893 | 19 | 1,011 | 1,039 | 2,069 | **90.7%** | ✅ Yes | 12.66s |
| TASK-211 | F | Gamma App | 1,893 | 20 | 717 | 668 | 1,405 | **74.2%** | ⚠️ No | 8.48s |
| TASK-212 | F | Gamma App | 1,899 | 27 | 1,022 | 962 | 2,011 | **94.1%** | ✅ Yes | 12.18s |
| TASK-213 | F | Gamma App | 1,899 | 27 | 801 | 936 | 1,764 | **92.9%** | ✅ Yes | 10.94s |
| TASK-214 | F | Gamma App | 1,890 | 15 | 972 | 805 | 1,792 | **94.8%** | ✅ Yes | 10.51s |
| TASK-215 | F | Gamma App | 1,895 | 23 | 991 | 916 | 1,930 | **98.2%** | ✅ Yes | 11.74s |
| TASK-216 | G | Gemini 3.1 Flash / Pro | 172 | 23 | 0 | 164 | 187 | **91.3%** | ✅ Yes | 1.48s |
| TASK-217 | G | Gemini 3.1 Flash / Pro | 170 | 22 | 0 | 129 | 151 | **88.8%** | ✅ Yes | 1.38s |
| TASK-218 | G | Gemini 3.1 Flash / Pro | 170 | 19 | 0 | 124 | 143 | **84.1%** | ✅ Yes | 1.36s |
| TASK-219 | G | ChatGPT (GPT-5o / O3-M | 1,397 | 22 | 921 | 357 | 1,300 | **93.1%** | ✅ Yes | 6.97s |
| TASK-220 | G | Gemini 3.1 Flash / Pro | 177 | 26 | 0 | 155 | 181 | **97.7%** | ✅ Yes | 1.68s |
| TASK-221 | G | Claude 3.7 Sonnet / Op | 1,496 | 23 | 1,011 | 397 | 1,431 | **95.7%** | ✅ Yes | 7.46s |
| TASK-222 | G | ChatGPT (GPT-5o / O3-M | 1,388 | 15 | 964 | 371 | 1,350 | **97.3%** | ✅ Yes | 7.07s |
| TASK-223 | G | Gemini 3.1 Flash / Pro | 166 | 15 | 0 | 139 | 154 | **92.8%** | ✅ Yes | 1.38s |
| TASK-224 | G | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 951 | 371 | 1,347 | **96.4%** | ✅ Yes | 7.01s |
| TASK-225 | G | Gemini 3.1 Flash / Pro | 164 | 15 | 0 | 178 | 193 | **82.3%** | ✅ Yes | 1.83s |
| TASK-226 | H | Claude 3.7 Sonnet / Op | 36 | 16 | 0 | 22 | 38 | **94.4%** | ⚠️ No | 0.40s |
| TASK-227 | H | Claude 3.7 Sonnet / Op | 48 | 21 | 0 | 28 | 49 | **97.9%** | ⚠️ No | 0.51s |
| TASK-228 | H | Claude 3.7 Sonnet / Op | 46 | 21 | 0 | 26 | 47 | **97.8%** | ⚠️ No | 0.59s |
| TASK-229 | H | Claude 3.7 Sonnet / Op | 36 | 16 | 0 | 20 | 36 | **100.0%** | ⚠️ No | 0.40s |
| TASK-230 | H | Claude 3.7 Sonnet / Op | 36 | 18 | 0 | 20 | 38 | **94.4%** | ⚠️ No | 0.54s |
| TASK-231 | H | Claude 3.7 Sonnet / Op | 46 | 19 | 0 | 23 | 42 | **91.3%** | ⚠️ No | 0.40s |
| TASK-232 | H | Claude 3.7 Sonnet / Op | 36 | 18 | 0 | 21 | 39 | **91.7%** | ⚠️ No | 0.57s |
| TASK-233 | H | Perplexity Pro | 1,894 | 20 | 1,089 | 836 | 1,945 | **97.3%** | ✅ Yes | 11.43s |
| TASK-234 | H | Claude 3.7 Sonnet / Op | 27 | 12 | 0 | 20 | 32 | **81.5%** | ⚠️ No | 0.56s |
| TASK-235 | H | ChatGPT (GPT-5o / O3-M | 1,395 | 21 | 880 | 346 | 1,247 | **89.4%** | ✅ Yes | 6.52s |
| TASK-236 | I | Claude 3.7 Sonnet / Op | 4,770 | 23 | 4,099 | 700 | 4,822 | **98.9%** | ✅ Yes | 22.32s |
| TASK-237 | I | Claude 3.7 Sonnet / Op | 4,786 | 39 | 4,282 | 688 | 5,009 | **95.3%** | ✅ Yes | 23.00s |
| TASK-238 | I | Claude 3.7 Sonnet / Op | 4,774 | 30 | 4,818 | 660 | 5,508 | **84.6%** | ⚠️ No | 24.79s |
| TASK-239 | I | ChatGPT (GPT-5o / O3-M | 1,407 | 35 | 978 | 296 | 1,309 | **93.0%** | ✅ Yes | 6.60s |
| TASK-240 | I | Claude 3.7 Sonnet / Op | 4,774 | 28 | 3,939 | 696 | 4,663 | **97.7%** | ✅ Yes | 21.78s |
| TASK-241 | I | ChatGPT (GPT-5o / O3-M | 1,415 | 42 | 962 | 323 | 1,327 | **93.8%** | ✅ Yes | 6.70s |
| TASK-242 | I | ChatGPT (GPT-5o / O3-M | 4,478 | 32 | 3,785 | 388 | 4,205 | **93.9%** | ⚠️ No | 18.44s |
| TASK-243 | I | Claude Code | 4,481 | 37 | 4,234 | 317 | 4,588 | **97.6%** | ✅ Yes | 19.66s |
| TASK-244 | I | Claude 3.7 Sonnet / Op | 4,772 | 28 | 4,619 | 664 | 5,311 | **88.7%** | ✅ Yes | 23.95s |
| TASK-245 | I | ChatGPT (GPT-5o / O3-M | 1,396 | 21 | 900 | 401 | 1,322 | **94.7%** | ✅ Yes | 7.06s |
| TASK-246 | J | Gemini 3.1 Flash / Pro | 5,073 | 29 | 3,232 | 900 | 4,161 | **82.0%** | ⚠️ No | 20.40s |
| TASK-247 | J | Claude Code | 4,469 | 25 | 4,406 | 312 | 4,743 | **93.9%** | ✅ Yes | 20.37s |
| TASK-248 | J | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 1,091 | 344 | 1,460 | **95.6%** | ✅ Yes | 7.28s |
| TASK-249 | J | Gemini 3.1 Flash / Pro | 109,123 | 27 | 5,015 | 103,309 | 108,351 | **99.3%** | ✅ Yes | 846.95s |
| TASK-250 | J | Gemini 3.1 Flash / Pro | 5,065 | 19 | 3,721 | 987 | 4,727 | **93.3%** | ✅ Yes | 23.02s |
| TASK-251 | J | Gemini 3.1 Flash / Pro | 4,122 | 28 | 4,347 | 20 | 4,395 | **93.4%** | ⚠️ No | 17.91s |
| TASK-252 | J | Claude 3.7 Sonnet / Op | 1,494 | 22 | 1,111 | 497 | 1,630 | **90.9%** | ✅ Yes | 8.57s |
| TASK-253 | J | Gemini 3.1 Flash / Pro | 5,069 | 25 | 3,522 | 924 | 4,471 | **88.2%** | ⚠️ No | 21.85s |
| TASK-254 | J | Gemini 3.1 Flash / Pro | 5,070 | 26 | 3,166 | 895 | 4,087 | **80.6%** | ⚠️ No | 20.18s |
| TASK-255 | J | Gemini 3.1 Flash / Pro | 144,126 | 32 | 4,100 | 132,702 | 136,834 | **94.9%** | ✅ Yes | 1078.40s |
| TASK-256 | K | Gemini 3.1 Flash / Pro | 1,494 | 20 | 1,033 | 434 | 1,487 | **99.5%** | ✅ Yes | 7.91s |
| TASK-257 | K | Gemini 3.1 Flash / Pro | 1,497 | 24 | 1,053 | 397 | 1,474 | **98.5%** | ✅ Yes | 7.60s |
| TASK-258 | K | ChatGPT (GPT-5o / O3-M | 1,392 | 19 | 1,218 | 365 | 1,602 | **84.9%** | ✅ Yes | 8.07s |
| TASK-259 | K | Gemini 3.1 Flash / Pro | 1,486 | 13 | 919 | 473 | 1,405 | **94.5%** | ✅ Yes | 7.70s |
| TASK-260 | K | Claude 3.7 Sonnet / Op | 1,494 | 21 | 962 | 466 | 1,449 | **97.0%** | ✅ Yes | 7.85s |
| TASK-261 | K | Claude 3.7 Sonnet / Op | 1,490 | 17 | 1,090 | 476 | 1,583 | **93.8%** | ✅ Yes | 8.47s |
| TASK-262 | K | Gemini 3.1 Flash / Pro | 168 | 19 | 0 | 123 | 142 | **84.5%** | ✅ Yes | 1.30s |
| TASK-263 | K | Gemini 3.1 Flash / Pro | 1,494 | 20 | 949 | 395 | 1,364 | **91.3%** | ✅ Yes | 7.24s |
| TASK-264 | K | Gemini 3.1 Flash / Pro | 1,495 | 21 | 1,177 | 439 | 1,637 | **90.5%** | ✅ Yes | 8.65s |
| TASK-265 | K | ChatGPT (GPT-5o / O3-M | 1,394 | 21 | 976 | 389 | 1,386 | **99.4%** | ✅ Yes | 7.23s |
| TASK-266 | L | DeepSeek V4 (Flash / P | 1,754 | 29 | 1,130 | 742 | 1,901 | **91.6%** | ✅ Yes | 10.89s |
| TASK-267 | L | ChatGPT (GPT-5o / O3-M | 1,394 | 22 | 1,099 | 330 | 1,451 | **95.9%** | ✅ Yes | 7.27s |
| TASK-268 | L | ChatGPT (GPT-5o / O3-M | 1,399 | 24 | 1,160 | 335 | 1,519 | **91.4%** | ✅ Yes | 7.63s |
| TASK-269 | L | ChatGPT (GPT-5o / O3-M | 4,371 | 25 | 4,652 | 230 | 4,907 | **87.7%** | ⚠️ No | 20.65s |
| TASK-270 | L | ChatGPT (GPT-5o / O3-M | 4,374 | 30 | 4,540 | 214 | 4,784 | **90.6%** | ⚠️ No | 20.12s |
| TASK-271 | L | Gamma App | 1,905 | 31 | 1,028 | 863 | 1,922 | **99.1%** | ✅ Yes | 11.22s |
| TASK-272 | L | Claude Code | 4,824 | 29 | 3,919 | 644 | 4,592 | **95.2%** | ✅ Yes | 21.16s |
| TASK-273 | L | ChatGPT (GPT-5o / O3-M | 4,375 | 28 | 3,782 | 211 | 4,021 | **91.9%** | ⚠️ No | 17.11s |
| TASK-274 | L | Gemini 3.1 Flash / Pro | 173 | 23 | 0 | 142 | 165 | **95.4%** | ✅ Yes | 1.55s |
| TASK-275 | L | ChatGPT (GPT-5o / O3-M | 1,397 | 24 | 1,135 | 385 | 1,544 | **89.5%** | ✅ Yes | 7.83s |
| TASK-276 | M | Claude 3.7 Sonnet / Op | 4,870 | 24 | 4,062 | 835 | 4,921 | **99.0%** | ✅ Yes | 23.29s |
| TASK-277 | M | Gemini 3.1 Flash / Pro | 170 | 22 | 0 | 180 | 202 | **81.2%** | ✅ Yes | 1.83s |
| TASK-278 | M | ChatGPT (GPT-5o / O3-M | 1,392 | 18 | 1,118 | 379 | 1,515 | **91.2%** | ✅ Yes | 7.80s |
| TASK-279 | M | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 820 | 285 | 1,130 | **80.8%** | ⚠️ No | 5.86s |
| TASK-280 | M | Claude 3.7 Sonnet / Op | 4,874 | 28 | 3,943 | 790 | 4,761 | **97.7%** | ✅ Yes | 22.52s |
| TASK-281 | M | Claude 3.7 Sonnet / Op | 1,495 | 23 | 1,143 | 443 | 1,609 | **92.4%** | ✅ Yes | 8.28s |
| TASK-282 | M | Claude 3.7 Sonnet / Op | 1,493 | 21 | 1,077 | 384 | 1,482 | **99.3%** | ✅ Yes | 7.73s |
| TASK-283 | M | ChatGPT (GPT-5o / O3-M | 1,399 | 24 | 941 | 358 | 1,323 | **94.6%** | ✅ Yes | 7.07s |
| TASK-284 | M | Claude 3.7 Sonnet / Op | 4,766 | 22 | 3,572 | 622 | 4,216 | **88.5%** | ⚠️ No | 19.70s |
| TASK-285 | M | ChatGPT (GPT-5o / O3-M | 1,385 | 11 | 1,074 | 301 | 1,386 | **99.9%** | ✅ Yes | 6.98s |
| TASK-286 | N | ChatGPT (GPT-5o / O3-M | 1,402 | 28 | 1,313 | 397 | 1,738 | **76.0%** | ✅ Yes | 8.80s |
| TASK-287 | N | Claude 3.7 Sonnet / Op | 1,500 | 28 | 1,062 | 411 | 1,501 | **99.9%** | ✅ Yes | 7.77s |
| TASK-288 | N | Claude 3.7 Sonnet / Op | 1,497 | 22 | 1,331 | 481 | 1,834 | **77.5%** | ✅ Yes | 9.34s |
| TASK-289 | N | Claude 3.7 Sonnet / Op | 1,599 | 24 | 990 | 585 | 1,599 | **100.0%** | ✅ Yes | 8.80s |
| TASK-290 | N | Perplexity Pro | 1,893 | 21 | 952 | 834 | 1,807 | **95.5%** | ✅ Yes | 10.87s |
| TASK-291 | N | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 1,096 | 368 | 1,489 | **93.5%** | ✅ Yes | 7.74s |
| TASK-292 | N | ChatGPT (GPT-5o / O3-M | 1,397 | 23 | 999 | 351 | 1,373 | **98.3%** | ✅ Yes | 7.17s |
| TASK-293 | N | ChatGPT (GPT-5o / O3-M | 1,406 | 32 | 1,070 | 334 | 1,436 | **97.9%** | ✅ Yes | 7.40s |
| TASK-294 | N | ChatGPT (GPT-5o / O3-M | 1,398 | 26 | 1,112 | 337 | 1,475 | **94.5%** | ✅ Yes | 7.41s |
| TASK-295 | N | ChatGPT (GPT-5o / O3-M | 1,393 | 21 | 954 | 368 | 1,343 | **96.4%** | ✅ Yes | 7.04s |
| TASK-296 | O | ChatGPT (GPT-5o / O3-M | 4,375 | 28 | 5,325 | 248 | 5,601 | **72.0%** | ⚠️ No | 23.51s |
| TASK-297 | O | Perplexity Pro | 1,901 | 27 | 985 | 821 | 1,833 | **96.4%** | ✅ Yes | 10.82s |
| TASK-298 | O | ChatGPT (GPT-5o / O3-M | 1,400 | 26 | 872 | 350 | 1,248 | **89.1%** | ✅ Yes | 6.46s |
| TASK-299 | O | Gemini 3.1 Flash / Pro | 171 | 21 | 0 | 143 | 164 | **95.9%** | ✅ Yes | 1.39s |
| TASK-300 | O | ChatGPT (GPT-5o / O3-M | 1,396 | 21 | 949 | 400 | 1,370 | **98.1%** | ✅ Yes | 7.36s |
| TASK-301 | O | ChatGPT (GPT-5o / O3-M | 1,408 | 34 | 1,163 | 335 | 1,532 | **91.2%** | ✅ Yes | 7.60s |
| TASK-302 | O | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 970 | 332 | 1,327 | **94.9%** | ✅ Yes | 6.84s |
| TASK-303 | O | ChatGPT (GPT-5o / O3-M | 1,397 | 25 | 988 | 399 | 1,412 | **98.9%** | ✅ Yes | 7.39s |
| TASK-304 | O | ChatGPT (GPT-5o / O3-M | 1,400 | 26 | 977 | 348 | 1,351 | **96.5%** | ✅ Yes | 6.89s |
| TASK-305 | O | ChatGPT (GPT-5o / O3-M | 1,401 | 28 | 1,051 | 362 | 1,441 | **97.1%** | ✅ Yes | 7.31s |
| TASK-306 | P | Claude 3.7 Sonnet / Op | 1,594 | 20 | 872 | 539 | 1,431 | **89.8%** | ✅ Yes | 8.15s |
| TASK-307 | P | Gemini 3.1 Flash / Pro | 5,068 | 23 | 4,530 | 1,071 | 5,624 | **89.0%** | ✅ Yes | 26.97s |
| TASK-308 | P | ChatGPT (GPT-5o / O3-M | 1,398 | 25 | 775 | 335 | 1,135 | **81.2%** | ⚠️ No | 6.09s |
| TASK-309 | P | ChatGPT (GPT-5o / O3-M | 1,397 | 22 | 1,055 | 284 | 1,361 | **97.4%** | ✅ Yes | 6.66s |
| TASK-310 | P | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 954 | 369 | 1,345 | **96.3%** | ✅ Yes | 7.06s |
| TASK-311 | P | ChatGPT (GPT-5o / O3-M | 1,395 | 23 | 1,005 | 372 | 1,400 | **99.6%** | ✅ Yes | 7.23s |
| TASK-312 | P | ChatGPT (GPT-5o / O3-M | 1,400 | 28 | 932 | 352 | 1,312 | **93.7%** | ✅ Yes | 6.78s |
| TASK-313 | P | ChatGPT (GPT-5o / O3-M | 4,374 | 30 | 4,050 | 257 | 4,337 | **99.2%** | ✅ Yes | 18.66s |
| TASK-314 | P | ChatGPT (GPT-5o / O3-M | 1,392 | 17 | 1,253 | 360 | 1,630 | **82.9%** | ✅ Yes | 8.14s |
| TASK-315 | P | ChatGPT (GPT-5o / O3-M | 1,399 | 27 | 885 | 325 | 1,237 | **88.4%** | ✅ Yes | 6.46s |
| TASK-316 | Q | ChatGPT (GPT-5o / O3-M | 1,397 | 22 | 1,118 | 358 | 1,498 | **92.8%** | ✅ Yes | 7.64s |
| TASK-317 | Q | ChatGPT (GPT-5o / O3-M | 1,397 | 22 | 927 | 370 | 1,319 | **94.4%** | ✅ Yes | 7.02s |
| TASK-318 | Q | ChatGPT (GPT-5o / O3-M | 1,392 | 19 | 930 | 399 | 1,348 | **96.8%** | ✅ Yes | 7.07s |
| TASK-319 | Q | ChatGPT (GPT-5o / O3-M | 1,392 | 19 | 857 | 374 | 1,250 | **89.8%** | ✅ Yes | 6.79s |
| TASK-320 | Q | Claude 3.7 Sonnet / Op | 1,503 | 31 | 1,171 | 489 | 1,691 | **87.5%** | ✅ Yes | 8.89s |
| TASK-321 | Q | ChatGPT (GPT-5o / O3-M | 1,398 | 24 | 979 | 354 | 1,357 | **97.1%** | ✅ Yes | 7.08s |
| TASK-322 | Q | Perplexity Pro | 1,900 | 26 | 1,073 | 658 | 1,757 | **92.5%** | ✅ Yes | 9.90s |
| TASK-323 | Q | ChatGPT (GPT-5o / O3-M | 1,393 | 21 | 981 | 331 | 1,333 | **95.7%** | ✅ Yes | 6.75s |
| TASK-324 | Q | ChatGPT (GPT-5o / O3-M | 1,400 | 26 | 991 | 344 | 1,361 | **97.2%** | ✅ Yes | 6.89s |
| TASK-325 | Q | ChatGPT (GPT-5o / O3-M | 1,397 | 22 | 1,119 | 320 | 1,461 | **95.4%** | ✅ Yes | 7.40s |
| TASK-326 | R | ChatGPT (GPT-5o / O3-M | 1,399 | 25 | 1,042 | 335 | 1,402 | **99.8%** | ✅ Yes | 7.09s |
| TASK-327 | R | ChatGPT (GPT-5o / O3-M | 1,394 | 22 | 934 | 324 | 1,280 | **91.8%** | ✅ Yes | 6.71s |
| TASK-328 | R | ChatGPT (GPT-5o / O3-M | 1,397 | 24 | 955 | 361 | 1,340 | **95.9%** | ✅ Yes | 6.91s |
| TASK-329 | R | ChatGPT (GPT-5o / O3-M | 1,390 | 15 | 885 | 291 | 1,191 | **85.7%** | ✅ Yes | 6.13s |
| TASK-330 | R | ChatGPT (GPT-5o / O3-M | 1,398 | 26 | 932 | 302 | 1,260 | **90.1%** | ✅ Yes | 6.44s |
| TASK-331 | R | ChatGPT (GPT-5o / O3-M | 1,398 | 24 | 973 | 370 | 1,367 | **97.8%** | ✅ Yes | 7.28s |
| TASK-332 | R | ChatGPT (GPT-5o / O3-M | 1,398 | 24 | 1,067 | 367 | 1,458 | **95.7%** | ✅ Yes | 7.64s |
| TASK-333 | R | ChatGPT (GPT-5o / O3-M | 1,397 | 25 | 1,142 | 397 | 1,564 | **88.0%** | ✅ Yes | 7.94s |
| TASK-334 | R | ChatGPT (GPT-5o / O3-M | 1,395 | 22 | 865 | 404 | 1,291 | **92.5%** | ✅ Yes | 6.86s |
| TASK-335 | R | ChatGPT (GPT-5o / O3-M | 1,397 | 25 | 1,061 | 338 | 1,424 | **98.1%** | ✅ Yes | 7.39s |
| TASK-336 | S | ChatGPT (GPT-5o / O3-M | 1,393 | 18 | 914 | 355 | 1,287 | **92.4%** | ✅ Yes | 6.82s |
| TASK-337 | S | ChatGPT (GPT-5o / O3-M | 1,394 | 22 | 1,171 | 363 | 1,556 | **88.4%** | ✅ Yes | 7.76s |
| TASK-338 | S | ChatGPT (GPT-5o / O3-M | 1,403 | 29 | 1,029 | 354 | 1,412 | **99.4%** | ✅ Yes | 7.24s |
| TASK-339 | S | ChatGPT (GPT-5o / O3-M | 1,397 | 25 | 1,000 | 356 | 1,381 | **98.9%** | ✅ Yes | 7.30s |
| TASK-340 | S | ChatGPT (GPT-5o / O3-M | 1,399 | 27 | 881 | 322 | 1,230 | **87.9%** | ✅ Yes | 6.32s |
| TASK-341 | S | ChatGPT (GPT-5o / O3-M | 1,399 | 27 | 989 | 367 | 1,383 | **98.9%** | ✅ Yes | 7.07s |
| TASK-342 | S | Claude 3.7 Sonnet / Op | 4,769 | 22 | 4,392 | 748 | 5,162 | **91.8%** | ✅ Yes | 23.90s |
| TASK-343 | S | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 1,032 | 325 | 1,379 | **98.8%** | ✅ Yes | 7.01s |
| TASK-344 | S | ChatGPT (GPT-5o / O3-M | 1,398 | 26 | 1,058 | 359 | 1,443 | **96.8%** | ✅ Yes | 7.48s |
| TASK-345 | S | Gemini 3.1 Flash / Pro | 174 | 24 | 0 | 145 | 169 | **97.1%** | ✅ Yes | 1.31s |
| TASK-346 | T | Gamma App | 1,897 | 23 | 774 | 765 | 1,562 | **82.3%** | ✅ Yes | 9.50s |
| TASK-347 | T | Claude 3.7 Sonnet / Op | 32 | 15 | 0 | 20 | 35 | **90.6%** | ⚠️ No | 0.58s |
| TASK-348 | T | Perplexity Pro | 3,042 | 24 | 1,077 | 2,001 | 3,102 | **98.0%** | ✅ Yes | 20.72s |
| TASK-349 | T | Claude 3.7 Sonnet / Op | 1,494 | 20 | 1,249 | 400 | 1,669 | **88.3%** | ✅ Yes | 8.36s |
| TASK-350 | T | Gamma App | 1,894 | 20 | 972 | 744 | 1,736 | **91.7%** | ✅ Yes | 10.02s |
| TASK-351 | T | DeepSeek V4 (Flash / P | 1,397 | 25 | 1,004 | 334 | 1,363 | **97.6%** | ✅ Yes | 7.03s |
| TASK-352 | T | ChatGPT (GPT-5o / O3-M | 4,370 | 24 | 4,187 | 222 | 4,433 | **98.6%** | ✅ Yes | 18.81s |
| TASK-353 | T | ChatGPT (GPT-5o / O3-M | 1,401 | 26 | 1,020 | 327 | 1,373 | **98.0%** | ✅ Yes | 7.04s |
| TASK-354 | T | Claude 3.7 Sonnet / Op | 1,106 | 18 | 1,091 | 72 | 1,181 | **93.2%** | ⚠️ No | 5.10s |
| TASK-355 | T | ChatGPT (GPT-5o / O3-M | 1,385 | 10 | 1,104 | 285 | 1,399 | **99.0%** | ✅ Yes | 6.99s |
| TASK-356 | U | ChatGPT (GPT-5o / O3-M | 1,376 | 4 | 1,036 | 374 | 1,414 | **97.2%** | ✅ Yes | 7.49s |
| TASK-357 | U | Claude 3.7 Sonnet / Op | 1,502 | 127 | 1,122 | 314 | 1,563 | **95.9%** | ✅ Yes | 7.57s |
| TASK-358 | U | ChatGPT (GPT-5o / O3-M | 1,390 | 16 | 1,008 | 377 | 1,401 | **99.2%** | ✅ Yes | 7.48s |
| TASK-359 | U | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 791 | 425 | 1,238 | **88.7%** | ✅ Yes | 6.89s |
| TASK-360 | U | Gemini 3.1 Flash / Pro | 5,062 | 18 | 3,769 | 871 | 4,658 | **92.0%** | ✅ Yes | 22.20s |
| TASK-361 | U | Claude 3.7 Sonnet / Op | 1,494 | 21 | 1,041 | 404 | 1,466 | **98.1%** | ✅ Yes | 7.82s |
| TASK-362 | U | Perplexity Pro | 1,892 | 17 | 1,004 | 739 | 1,760 | **93.0%** | ✅ Yes | 10.27s |
| TASK-363 | U | ChatGPT (GPT-5o / O3-M | 1,396 | 22 | 841 | 426 | 1,289 | **92.3%** | ✅ Yes | 7.12s |
| TASK-364 | U | Claude 3.7 Sonnet / Op | 4,868 | 24 | 3,275 | 761 | 4,060 | **83.4%** | ⚠️ No | 19.36s |
| TASK-365 | U | Claude Code | 4,473 | 26 | 3,769 | 438 | 4,233 | **94.6%** | ⚠️ No | 18.87s |

---
*Auto-generated from `evaluation/actual_token_usage_results.json`*
