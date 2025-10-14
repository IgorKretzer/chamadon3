import React, { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'

function TicketInput({ onSubmit, loading }) {
  const [ticketNumero, setTicketNumero] = useState('')
  const [usuarioNome, setUsuarioNome] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (ticketNumero.trim()) {
      onSubmit(ticketNumero.trim(), usuarioNome.trim() || null)
    }
  }

  return (
    <div className="ticket-input-container">
      <div className="ticket-input-header">
        <h2>Analisar Ticket do Movidesk</h2>
        <p className="subtitle">
          Informe o número do ticket para gerar uma sugestão de chamado
        </p>
      </div>

      <form onSubmit={handleSubmit} className="ticket-form">
        <div className="form-group">
          <label htmlFor="usuario">Seu Nome (opcional)</label>
          <input
            type="text"
            id="usuario"
            value={usuarioNome}
            onChange={(e) => setUsuarioNome(e.target.value)}
            placeholder="Digite seu nome..."
            className="form-input"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="ticket">Número do Ticket *</label>
          <div className="input-with-button">
            <input
              type="text"
              id="ticket"
              value={ticketNumero}
              onChange={(e) => setTicketNumero(e.target.value)}
              placeholder="Ex: 156789"
              className="form-input"
              disabled={loading}
              required
            />
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !ticketNumero.trim()}
            >
              {loading ? (
                <>
                  <Loader2 className="spin" size={20} />
                  Analisando...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Analisar
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

export default TicketInput

