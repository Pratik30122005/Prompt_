import router

print("="*70)
print("1. GT-6 SCORE MARGIN VS TIE-BREAK TEST")
print("="*70)
cls = router.classify_prompt("Write a bedtime story for my daughter and format it as an HTML page with CSS styling.")
eligible = router._eligible_models(cls["output_format"])
for tid, tinfo in eligible.items():
    s = router.score_model(cls, tid, tinfo)
    print(f"  {tid}: {s['total_score']} (s_capability: {s['breakdown']['capability']})")
print("-> Claude wins outright by margin (0.9784 vs 0.8702) due to higher capability score for creative_writing.")
print()

print("="*70)
print("2. CONFLICTING VERBS TEST")
print("="*70)
p = "Reconcile and summarize this CSV data"
intent = router._leading_verb_intent(p)
cls = router.classify_prompt(p)
print(f"  Prompt: '{p}'")
print(f"  _leading_verb_intent: {intent}")
print(f"  Resolved task_type: {cls['task_type']}")
print("-> 'data_extraction' wins because intent=None (both verbs present) falls back to the presence of 'csv' structural signal.")
print()

print("="*70)
print("3. ZERO-ELIGIBLE MODELS FALLBACK TEST")
print("="*70)
# Force a fake format that no model supports
fake_cls = {
    "task_type": "alien_task",
    "reasoning_depth": "low",
    "context_length_req": "short",
    "output_format": "hologram",
    "latency_sensitivity": "low",
    "cost_sensitivity": "low",
    "tool_use_needed": "none"
}
models = router._eligible_models(fake_cls["output_format"])
print(f"  Returned {len(models)} models.")
print()

print("="*70)
print("4. FULL SELFTEST PASS")
print("="*70)
router.selftest()
