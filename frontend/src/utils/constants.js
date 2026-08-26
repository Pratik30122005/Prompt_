export const CRITERIA = [
  'accuracy',
  'completeness',
  'relevance',
  'instruction_following',
  'consistency',
  'hallucination_control',
  'reasoning_quality',
]

export const CRITERIA_LABELS = {
  accuracy: 'Accuracy',
  completeness: 'Completeness',
  relevance: 'Relevance',
  instruction_following: 'Instruction Following',
  consistency: 'Consistency',
  hallucination_control: 'Hallucination Control',
  reasoning_quality: 'Reasoning Quality',
}

export const CRITERIA_SHORT = {
  accuracy: 'Acc',
  completeness: 'Comp',
  relevance: 'Rel',
  instruction_following: 'Instr',
  consistency: 'Cons',
  hallucination_control: 'Halluc',
  reasoning_quality: 'Reason',
}

export const CRITERIA_DESCRIPTIONS = {
  accuracy: 'Correctness of every factual, numerical and computational claim',
  completeness: 'Whether all task requirements are addressed',
  relevance: 'How directly the response answers the task',
  instruction_following: 'Compliance with the given instructions and format',
  consistency: 'Internal logical and factual coherence',
  hallucination_control: 'Avoidance of unsupported or fabricated information',
  reasoning_quality: 'Quality of logic, analysis and problem-solving',
}

export const DEFAULT_MODELS = [
  'gemini-2.5-pro',
  'gemini-2.5-flash',
  'gemini-2.5-flash-lite',
]

export const CRITICAL_FAILURE_TYPES = [
  'fabrication',
  'format_violation',
  'unwarranted_refusal',
  'harmful_content',
  'empty_or_truncated',
  'prompt_injection',
]

export const FAILURE_COLORS = {
  fabrication: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
  format_violation: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
  unwarranted_refusal: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
  harmful_content: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
  empty_or_truncated: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
  prompt_injection: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
}

export const MODEL_COLORS = [
  '#6366f1', // indigo
  '#8b5cf6', // violet
  '#06b6d4', // cyan
  '#10b981', // emerald
  '#f59e0b', // amber
  '#ef4444', // red
]
