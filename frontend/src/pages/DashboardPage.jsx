import React, { useState, useEffect } from 'react'
import { 
  getEstatisticas, 
  getAnalisesRecentes,
  limparCache 
} from '../services/api'
import { 
  TrendingUp, 
  CheckCircle, 
  ThumbsUp, 
  Clock,
  RefreshCw,
  Trash2,
  AlertCircle
} from 'lucide-react'

function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [analises, setAnalises] = useState([])
  const [periodo, setPeriodo] = useState(7)
  const [loading, setLoading] = useState(true)
  const [erro, setErro] = useState(null)
  const [analiseExpandida, setAnaliseExpandida] = useState(null)

  const carregarDados = async () => {
    setLoading(true)
    setErro(null)
    
    try {
      const [statsData, analisesData] = await Promise.all([
        getEstatisticas(periodo),
        getAnalisesRecentes(10)
      ])
      
      setStats(statsData)
      setAnalises(analisesData.analises)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
      setErro('Erro ao carregar estatísticas')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    carregarDados()
  }, [periodo])

  const handleLimparCache = async () => {
    if (confirm('Deseja realmente limpar o cache expirado?')) {
      try {
        const result = await limparCache()
        alert(result.mensagem)
        carregarDados()
      } catch (error) {
        alert('Erro ao limpar cache')
      }
    }
  }

  const formatarData = (dataStr) => {
    const data = new Date(dataStr)
    return data.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Carregando estatísticas...</p>
      </div>
    )
  }

  if (erro) {
    return (
      <div className="error-message">
        <AlertCircle size={20} />
        <p>{erro}</p>
      </div>
    )
  }

  return (
    <div className="dashboard-page">
      <div className="container">
        {/* Header */}
        <div className="dashboard-header">
          <div>
            <h2>📊 Dashboard de Estatísticas</h2>
            <p className="subtitle">Métricas e análises dos últimos {periodo} dias</p>
          </div>
          <div className="dashboard-actions">
            <select 
              value={periodo} 
              onChange={(e) => setPeriodo(Number(e.target.value))}
              className="period-select"
            >
              <option value={7}>Últimos 7 dias</option>
              <option value={15}>Últimos 15 dias</option>
              <option value={30}>Últimos 30 dias</option>
            </select>
            <button onClick={carregarDados} className="btn-secondary">
              <RefreshCw size={18} />
              Atualizar
            </button>
            <button onClick={handleLimparCache} className="btn-secondary">
              <Trash2 size={18} />
              Limpar Cache
            </button>
          </div>
        </div>

        {/* Cards de Estatísticas */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon blue">
              <TrendingUp size={24} />
            </div>
            <div className="stat-content">
              <p className="stat-label">Total de Análises</p>
              <h3 className="stat-value">{stats.total_analises}</h3>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon red">
              <CheckCircle size={24} />
            </div>
            <div className="stat-content">
              <p className="stat-label">Inconsistências Detectadas</p>
              <h3 className="stat-value">{stats.total_inconsistencias}</h3>
              <p className="stat-detail">
                {stats.total_analises > 0 
                  ? `${Math.round((stats.total_inconsistencias / stats.total_analises) * 100)}%`
                  : '0%'
                } do total
              </p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon green">
              <ThumbsUp size={24} />
            </div>
            <div className="stat-content">
              <p className="stat-label">Taxa de Aprovação</p>
              <h3 className="stat-value">{stats.taxa_aprovacao}%</h3>
              <p className="stat-detail">Feedbacks positivos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon purple">
              <Clock size={24} />
            </div>
            <div className="stat-content">
              <p className="stat-label">Tempo Médio</p>
              <h3 className="stat-value">
                {(stats.tempo_medio_ms / 1000).toFixed(2)}s
              </h3>
              <p className="stat-detail">Por análise</p>
            </div>
          </div>
        </div>

        {/* Módulos Mais Afetados */}
        {stats.modulos_top && stats.modulos_top.length > 0 && (
          <div className="section">
            <h3 className="section-title">🎯 Módulos Mais Afetados</h3>
            <div className="modulos-list">
              {stats.modulos_top.map((modulo, index) => {
                const porcentagem = stats.total_analises > 0
                  ? (modulo.total / stats.total_analises) * 100
                  : 0
                
                return (
                  <div key={index} className="modulo-item">
                    <div className="modulo-info">
                      <span className="modulo-rank">#{index + 1}</span>
                      <span className="modulo-nome">{modulo.modulo_identificado}</span>
                      <span className="modulo-count">{modulo.total} ocorrências</span>
                    </div>
                    <div className="modulo-bar-container">
                      <div 
                        className="modulo-bar" 
                        style={{ width: `${porcentagem}%` }}
                      ></div>
                    </div>
                    <span className="modulo-percent">{porcentagem.toFixed(1)}%</span>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Análises Recentes */}
        {analises.length > 0 && (
          <div className="section">
            <h3 className="section-title">📋 Análises Recentes</h3>
            <div className="analises-recentes-lista">
              {analises.map((analise) => (
                <div key={analise.id} className="analise-item">
                  <div 
                    className="analise-header"
                    onClick={() => setAnaliseExpandida(analiseExpandida === analise.id ? null : analise.id)}
                  >
                    <div className="analise-info">
                      <span className="ticket-badge">#{analise.ticket_numero}</span>
                      <span className="analise-usuario">{analise.usuario_nome || 'Anônimo'}</span>
                      <span className={`type-badge ${analise.tipo_identificado}`}>
                        {analise.tipo_identificado || 'N/A'}
                      </span>
                      {analise.modulo_identificado && (
                        <span className="analise-modulo">📦 {analise.modulo_identificado}</span>
                      )}
                    </div>
                    <div className="analise-meta">
                      <span className="date-cell">{formatarData(analise.data_analise)}</span>
                      {analise.foi_copiado ? (
                        <span className="status-badge copiado">Copiado</span>
                      ) : (
                        <span className="status-badge pendente">Pendente</span>
                      )}
                      <button className="btn-expand">
                        {analiseExpandida === analise.id ? '▲' : '▼'}
                      </button>
                    </div>
                  </div>
                  
                  {analiseExpandida === analise.id && analise.chamado_gerado && (
                    <div className="analise-conteudo">
                      <div className="analise-sugestao">
                        <div className="sugestao-header">
                          <h4>💡 Sugestão de Chamado</h4>
                          <button 
                            className="btn-copy-small"
                            onClick={() => {
                              navigator.clipboard.writeText(analise.chamado_gerado)
                              alert('Sugestão copiada!')
                            }}
                          >
                            📋 Copiar
                          </button>
                        </div>
                        <div className="sugestao-texto">
                          <pre>{analise.chamado_gerado}</pre>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {stats.total_analises === 0 && (
          <div className="empty-state">
            <div className="empty-icon">📊</div>
            <h3>Nenhuma análise ainda</h3>
            <p>Comece analisando tickets para ver as estatísticas aqui</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default DashboardPage

