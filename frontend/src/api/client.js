const API_BASE = '/api'

function getApiKey() {
  return localStorage.getItem('gemini_api_key') || ''
}

export function hasApiKey() {
  return !!getApiKey()
}

/**
 * Run an evaluation and stream progress via SSE.
 * @param {object} config - Evaluation config
 * @param {function} onEvent - Called with each SSE event object
 * @returns {Promise<void>}
 */
export async function evaluatePrompt(config, onEvent) {
  const response = await fetch(`${API_BASE}/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': getApiKey(),
    },
    body: JSON.stringify(config),
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Evaluation failed: ${response.status} ${text}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n\n')
    buffer = lines.pop() || ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6))
          onEvent(data)
        } catch {
          // skip malformed events
        }
      }
    }
  }
}

/**
 * List all saved evaluations (metadata only).
 */
export async function listEvaluations() {
  const res = await fetch(`${API_BASE}/evaluations`)
  if (!res.ok) throw new Error('Failed to fetch evaluations')
  return res.json()
}

/**
 * Get full evaluation result by ID.
 */
export async function getEvaluation(id) {
  const res = await fetch(`${API_BASE}/evaluations/${id}`)
  if (!res.ok) throw new Error('Evaluation not found')
  return res.json()
}

/**
 * Delete a saved evaluation.
 */
export async function deleteEvaluation(id) {
  const res = await fetch(`${API_BASE}/evaluations/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete evaluation')
  return res.json()
}

/**
 * Get available models and pricing.
 */
export async function getModels() {
  const res = await fetch(`${API_BASE}/models`)
  if (!res.ok) throw new Error('Failed to fetch models')
  return res.json()
}

/**
 * Route one task to a tool + intelligence level.
 */
export async function recommendTool(prompt, model) {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': getApiKey(),
    },
    body: JSON.stringify(model ? { prompt, model } : { prompt }),
  })
  if (!res.ok) {
    const { detail } = await res.json().catch(() => ({}))
    throw new Error(detail || `Recommendation failed: ${res.status}`)
  }
  return res.json()
}

/**
 * Get the router's tool catalog.
 */
export async function getTools() {
  const res = await fetch(`${API_BASE}/tools`)
  if (!res.ok) throw new Error('Failed to fetch tools')
  return res.json()
}
