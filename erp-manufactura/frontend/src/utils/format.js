/**
 * Formatea numeros eliminando decimales innecesarios.
 * Ej: 1000.00 → "1000", 1.50 → "1.5", 0.00 → "0"
 */
export function formatNumber(value) {
  if (value === null || value === undefined) return '-'
  const num = parseFloat(value)
  if (isNaN(num)) return '-'
  return num === Math.floor(num) ? num.toString() : parseFloat(num.toFixed(2)).toString()
}

/**
 * Formatea moneda eliminando decimales innecesarios.
 * Ej: 30.00 → "$30", 30.50 → "$30.5"
 */
export function formatCurrency(value) {
  if (value === null || value === undefined) return '-'
  const num = parseFloat(value)
  if (isNaN(num)) return '-'
  const formatted = num === Math.floor(num) ? num.toString() : parseFloat(num.toFixed(2)).toString()
  return `$${formatted}`
}
