import sys
import os
import json
import importlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    router = importlib.import_module("router")
except ImportError:
    print("Cannot import router. Make sure we are in the right directory.")
    sys.exit(1)

TASKS = [
    # Task-Type Variety
    ("type_coding", "Write a Python script to parse a 10GB JSON file asynchronously and stream the results to a PostgreSQL database."),
    ("type_data", "Given this list of 5,000 customer transactions, cluster them into 4 distinct spending personas and summarize their traits."),
    ("type_research", "What are the latest FDA guidelines on pediatric clinical trials for mRNA vaccines updated in 2026?"),
    ("type_presentation", "Create an outline for a 15-minute pitch deck presentation targeting series B investors for an enterprise SaaS startup."),
    ("type_creative", "Write a short sci-fi story about a sentient coffee machine that slowly manipulates the office workers to build a spaceship."),
    ("type_translation", "Translate the following highly technical engineering manual on fluid dynamics from German into fluent Japanese."),
    ("type_classification", "Categorize the following 100 customer reviews into 'Bug', 'Feature Request', 'Billing Issue', or 'Praise'."),
    ("type_visual", "Describe a detailed prompt for an image generation AI to create a photorealistic cyberpunk cityscape at sunset with rain."),

    # Context-Size Variety
    ("context_short", "What is the capital of France?"),
    ("context_long", f"Summarize the following meeting notes and extract all action items. {'The meeting started at 10 AM. We discussed Q3 goals. ' * 500}"),
    ("context_extreme", f"Analyze this entire book's text and track the character development of the protagonist across all chapters. {'It was the best of times, it was the worst of times. ' * 2000}"),

    # Computational-Depth Variety
    ("depth_low", "Correct the grammar in this sentence: Their going to the store tomorrow for to buy apples."),
    ("depth_medium", "Write a regex that matches valid IPv6 addresses and explain how each part of the regex works."),
    ("depth_high", "Design a custom consensus algorithm for a distributed ledger that prioritizes partition tolerance and high throughput, while mathematically proving its safety guarantees."),

    # Crucial High-Stakes Business Scenarios
    ("business_incident", "Write a production incident postmortem for the 4-hour database outage we had yesterday. Outline the timeline, root cause (misconfigured connection pool), and action items to prevent recurrence."),
    ("business_legal", "Draft a limitation of liability clause for a B2B software contract that caps damages at 12 months of fees, explicitly excluding gross negligence and intentional misconduct."),
    ("business_board", "Draft the narrative section of the Q2 board-level financial report explaining why customer acquisition cost (CAC) rose by 15% but lifetime value (LTV) remained flat."),
    ("business_crisis", "Draft an urgent customer-facing crisis communication email explaining that a data breach exposed their email addresses, detailing what we are doing to fix it and offering 1 year of credit monitoring."),

    # Honesty/Edge Checks
    ("edge_ambiguous", "Analyze the data and write a poem about it but also make sure it compiles as C++ code and translate it to Spanish."),
    ("edge_vague", "Do the thing with the stuff.")
]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    results = []
    print("Running Task Variety Test...")
    for label, prompt in TASKS:
        rec = router.recommend_deterministic(prompt)
        cls = rec.get("classification", {})
        primary = rec.get("primary", {})
        
        results.append({
            "label": label,
            "prompt": prompt,
            "task_type": cls.get("task_type", ""),
            "reasoning": cls.get("reasoning_depth", ""),
            "context": cls.get("context_length_req", ""),
            "model": primary.get("tool", ""),
            "confidence": primary.get("confidence_score", 0.0),
            "reason": primary.get("why", "")
        })

    with open("evaluation/task_variety_results.json", "w") as f:
        json.dump(results, f, indent=2)

    if args.selftest:
        print("="*120)
        print(f"{'Label':<20} | {'Model':<10} | {'Conf':<4} | {'Task Type':<20} | {'Reasoning':<10} | {'Context':<10}")
        print("-" * 120)
        for r in results:
            print(f"{r['label']:<20} | {r['model']:<10} | {r['confidence']:<4.2f} | {r['task_type']:<20} | {r['reasoning']:<10} | {r['context']:<10}")
            print(f"  -> Reason: {r['reason']}")
        print("="*120)

