import json

fake_data = [
    {
        "user_feedback": "downvote",
        "recommended_tool": "chatgpt",
        "actual_tool_used": "claude",
        "classification": {
            "task_type": "creative_writing",
            "reasoning_depth": "medium",
            "context_length_req": "short",
            "cost_sensitivity": "medium",
            "latency_sensitivity": "medium",
            "tool_use_needed": "none"
        }
    }
] * 6

with open('/Users/pratikyadav/Desktop/pratik_/Prompt_/evaluations/feedback.jsonl', 'a') as f:
    for entry in fake_data:
        f.write(json.dumps(entry) + '\n')
print("Added 6 fake downvotes.")
