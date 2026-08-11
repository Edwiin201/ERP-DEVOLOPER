/**
 * Cliente HTTP para la API del backend.
 * Usa fetch nativo con manejo de errores centralizado.
 */

const API_BASE = 'http://localhost:8000'

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, config)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error desconocido' }))
      throw new Error(error.detail || `Error ${response.status}`)
    }

    // 204 No Content no tiene body
    if (response.status === 204) {
      return null
    }

    return await response.json()
  } catch (error) {
    console.error('API Error:', error.message)
    throw error
  }
}

export const api = {
  get(path, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `${path}?${queryString}` : path
    return request(url)
  },

  post(path, data) {
    return request(path, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  put(path, data) {
    return request(path, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  delete(path) {
    return request(path, {
      method: 'DELETE',
    })
  },
}
