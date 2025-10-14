import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// ==================== ANÁLISE ====================

export const analisarTicket = async (ticketNumero, usuarioNome = null) => {
  try {
    const response = await api.post('/api/analise/ticket', {
      ticket_numero: ticketNumero,
      usuario_nome: usuarioNome
    })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const marcarCopiado = async (analiseId) => {
  try {
    const response = await api.post('/api/analise/marcar-copiado', {
      analise_id: analiseId
    })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const enviarFeedback = async (analiseId, foiUtil, nota = null, comentario = null) => {
  try {
    const response = await api.post('/api/analise/feedback', {
      analise_id: analiseId,
      foi_util: foiUtil,
      nota: nota,
      comentario: comentario
    })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

// ==================== ESTATÍSTICAS ====================

export const getEstatisticas = async (dias = 7) => {
  try {
    const response = await api.get(`/api/estatisticas/periodo/${dias}`)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const getAnalisesRecentes = async (limit = 10) => {
  try {
    const response = await api.get(`/api/estatisticas/recentes?limit=${limit}`)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const limparCache = async () => {
  try {
    const response = await api.post('/api/estatisticas/limpar-cache')
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export default api

