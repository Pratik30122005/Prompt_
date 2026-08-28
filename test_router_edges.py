import router

print("GT-6 score breakdown:")
cls = router.classify_prompt("Write a bedtime story for my daughter and format it as an HTML page with CSS styling.")
eligible = router._eligible_models(cls["output_format"])
for tid, tinfo in eligible.items():
    s = router.score_model(cls, tid, tinfo)
    print(f"  {tid}: {s['total_score']}")

print("\nConflicting verbs test:")
p = "Reconcile and summarize this CSV data"
intent = router._leading_verb_intent(p)
cls = router.classify_prompt(p)
print(f"  intent={intent}, resolves to={cls['task_type']}")
