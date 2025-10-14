import React, { useState } from 'react'
import TicketInput from '../components/TicketInput'
import ResultDisplay from '../components/ResultDisplay'
import { analisarTicket } from '../services/api'
import { AlertCircle } from 'lucide-react'

function HomePage() {
  const [loading, setLoading] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [analiseId, setAnaliseId] = useState(null)
  const [erro, setErro] = useState(null)
  const [tempoProcessamento, setTempoProcessamento] = useState(null)

  const handleAnalisar = async (ticketNumero, usuarioNome) => {
    setLoading(true)
    setErro(null)
    setResultado(null)

    try {
      const response = await analisarTicket(ticketNumero, usuarioNome)
      
      if (response.sucesso) {
        setResultado(response.resultado)
        setAnaliseId(response.analise_id)
        setTempoProcessamento(response.tempo_processamento_ms)
      } else {
        setErro(response.mensagem || 'Erro ao analisar ticket')
      }
    } catch (error) {
      console.error('Erro:', error)
      setErro(error.detail || 'Erro ao conectar com o servidor. Verifique se o backend está rodando.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home-page">
      <div className="container">
        {/* Input Section */}
        <TicketInput onSubmit={handleAnalisar} loading={loading} />

        {/* Error Message */}
        {erro && (
          <div className="error-message">
            <AlertCircle size={20} />
            <p>{erro}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Analisando ticket com IA...</p>
            <p className="loading-subtitle">
              Buscando dados do Movidesk e processando com inteligência artificial
            </p>
          </div>
        )}

        {/* Result Display */}
        {resultado && !loading && (
          <div className="result-section">
            {tempoProcessamento && (
              <div className="tempo-info">
                ⚡ Processado em {(tempoProcessamento / 1000).toFixed(2)}s
              </div>
            )}
            <ResultDisplay resultado={resultado} analiseId={analiseId} />
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage

