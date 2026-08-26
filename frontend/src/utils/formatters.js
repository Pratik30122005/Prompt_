/**
 * Format a USD cost value for display.
 */
export function formatCost(cost) {
  if (cost === null || cost === undefined) return '?'
  if (cost === 0) return '$0.00'
  if (cost < 0.000001) return '<$0.000001'
  if (cost < 0.01) return `$${cost.toFixed(6)}`
  return `$${cost.toFixed(4)}`
}

/**
 * Format seconds for display.
 */
export function formatSeconds(secs) {
  if (secs === null || secs === undefined) return '-'
  return `${secs.toFixed(1)}s`
}

/**
 * Format a score (1-5) for display.
 */
export function formatScore(score) {
  if (score === null || score === undefined || score === 0) return '-'
  return score.toFixed(1)
}

/**
 * Compute the mean of an object's values.
 */
export function meanScore(scoreObj) {
  if (!scoreObj || typeof scoreObj !== 'object') return null
  const values = Object.values(scoreObj).filter(v => typeof v === 'number' && v > 0)
  if (values.length === 0) return null
  return values.reduce((a, b) => a + b, 0) / values.length
}

/**
 * Format a variance value (0-1) as a percentage-like label.
 */
export function formatVariance(variance) {
  if (variance === null || variance === undefined) return '-'
  return variance.toFixed(2)
}

/**
 * Format token counts for display.
 */
export function formatTokens(tokens) {
  if (!tokens) return '-'
  const total = (tokens.in || 0) + (tokens.out || 0) + (tokens.think || 0)
  if (total >= 1000) return `${(total / 1000).toFixed(1)}k`
  return total.toString()
}

/**
 * Format a thinking budget for display.
 */
export function formatThinking(thinking) {
  if (thinking === null || thinking === undefined) return 'Default'
  if (thinking === -1) return 'Dynamic'
  if (thinking === 0) return 'Off'
  return thinking.toLocaleString()
}

/**
 * Format a timestamp string for display.
 */
export function formatTimestamp(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const diffMs = now - d
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return d.toLocaleDateString()
}

/**
 * Truncate a string to a max length.
 */
export function truncate(str, maxLen = 80) {
  if (!str) return ''
  if (str.length <= maxLen) return str
  return str.slice(0, maxLen) + '…'
}

/**
 * Get a color-coded class for a score value (1-5).
 */
export function scoreColorClass(score) {
  if (score >= 4.5) return 'text-emerald-600 dark:text-emerald-400'
  if (score >= 3.5) return 'text-blue-600 dark:text-blue-400'
  if (score >= 2.5) return 'text-yellow-600 dark:text-yellow-400'
  if (score >= 1.5) return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}

/**
 * Get a background color class for a score value (1-5).
 */
export function scoreBgClass(score) {
  if (score >= 4.5) return 'bg-emerald-100 dark:bg-emerald-900/30'
  if (score >= 3.5) return 'bg-blue-100 dark:bg-blue-900/30'
  if (score >= 2.5) return 'bg-yellow-100 dark:bg-yellow-900/30'
  if (score >= 1.5) return 'bg-orange-100 dark:bg-orange-900/30'
  return 'bg-red-100 dark:bg-red-900/30'
}
