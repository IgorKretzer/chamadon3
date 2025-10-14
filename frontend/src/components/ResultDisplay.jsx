import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { 
  Copy, 
  Check, 
  ThumbsUp, 
  ThumbsDown, 
  Star,
  AlertCircle,
  CheckCircle2,
  MessageSquare
} from 'lucide-react'
import { marcarCopiado, enviarFeedback } from '../services/api'

function ResultDisplay({ resultado, analiseId }) {
  const [copiado, setCopiado] = useState(false)
  const [feedbackEnviado, setFeedbackEnviado] = useState(false)
  const [mostrarFeedback, setMostrarFeedback] = useState(false)
  const [nota, setNota] = useState(0)
  const [comentario, setComentario] = useState('')

  const handleCopiar = async () => {
    try {
      await navigator.clipboard.writeText(resultado.chamado_texto)
      setCopiado(true)
      
      // Marca no backend
      await marcarCopiado(analiseId)
      
      setTimeout(() => setCopiado(false), 2000)
    } catch (error) {
      console.error('Erro ao copiar:', error)
    }
  }

  const handleFeedback = async (foiUtil) => {
    setMostrarFeedback(true)
    
    if (!foiUtil) {
      // Se não foi útil, já envia
      await enviarFeedback(analiseId, false)
      setFeedbackEnviado(true)
    }
  }

  const handleEnviarFeedbackCompleto = async () => {
    try {
      await enviarFeedback(analiseId, true, nota > 0 ? nota : null, comentario || null)
      setFeedbackEnviado(true)
      setMostrarFeedback(false)
    } catch (error) {
      console.error('Erro ao enviar feedback:', error)
    }
  }

  const isInconsistencia = resultado.tipo === 'inconsistencia'

  return (
    <div className="result-container">
      {/* Header com status */}
      <div className={`result-header ${isInconsistencia ? 'success' : 'warning'}`}>
        {isInconsistencia ? (
          <>
            <CheckCircle2 size={24} />
            <div>
              <h3>✅ Inconsistência Identificada</h3>
              <p>Chamado sugerido gerado com sucesso</p>
            </div>
          </>
        ) : (
          <>
            <AlertCircle size={24} />
            <div>
              <h3>ℹ️ Análise Concluída</h3>
              <p>Este ticket pode não ser uma inconsistência</p>
            </div>
          </>
        )}
      </div>

      {/* Metadata */}
      {resultado.modulo && (
        <div className="result-metadata">
          <div className="metadata-item">
            <span className="metadata-label">Módulo:</span>
            <span className="metadata-value badge">{resultado.modulo}</span>
          </div>
          {resultado.metadata?.tela && (
            <div className="metadata-item">
              <span className="metadata-label">Tela:</span>
              <span className="metadata-value">{resultado.metadata.tela}</span>
            </div>
          )}
        </div>
      )}

      {/* Texto do Chamado */}
      <div className="result-content">
        <div className="content-header">
          <h4>📋 Sugestão de Chamado</h4>
          <button
            onClick={handleCopiar}
            className="btn-secondary btn-small"
          >
            {copiado ? (
              <>
                <Check size={16} />
                Copiado!
              </>
            ) : (
              <>
                <Copy size={16} />
                Copiar Texto
              </>
            )}
          </button>
        </div>
        
        <div className="chamado-texto">
          <pre>{resultado.chamado_texto}</pre>
        </div>
      </div>

      {/* Feedback */}
      {!feedbackEnviado && !mostrarFeedback && (
        <div className="feedback-section">
          <p className="feedback-title">Esta sugestão foi útil?</p>
          <div className="feedback-buttons">
            <button
              onClick={() => handleFeedback(true)}
              className="btn-feedback btn-feedback-positive"
            >
              <ThumbsUp size={20} />
              Sim, foi útil
            </button>
            <button
              onClick={() => handleFeedback(false)}
              className="btn-feedback btn-feedback-negative"
            >
              <ThumbsDown size={20} />
              Não foi útil
            </button>
          </div>
        </div>
      )}

      {/* Form de feedback detalhado */}
      {mostrarFeedback && !feedbackEnviado && (
        <div className="feedback-form">
          <h4>Avalie a sugestão (opcional)</h4>
          
          <div className="star-rating">
            {[1, 2, 3, 4, 5].map((estrela) => (
              <button
                key={estrela}
                onClick={() => setNota(estrela)}
                className={`star-btn ${nota >= estrela ? 'active' : ''}`}
              >
                <Star size={24} fill={nota >= estrela ? 'currentColor' : 'none'} />
              </button>
            ))}
          </div>

          <textarea
            value={comentario}
            onChange={(e) => setComentario(e.target.value)}
            placeholder="Comentários ou sugestões de melhoria (opcional)"
            className="feedback-textarea"
            rows={3}
          />

          <button
            onClick={handleEnviarFeedbackCompleto}
            className="btn-primary"
          >
            <MessageSquare size={18} />
            Enviar Avaliação
          </button>
        </div>
      )}

      {/* Feedback enviado */}
      {feedbackEnviado && (
        <div className="feedback-success">
          <Check size={20} />
          Obrigado pelo feedback! Isso nos ajuda a melhorar a IA.
        </div>
      )}
    </div>
  )
}

export default ResultDisplay

