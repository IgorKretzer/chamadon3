from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==================== REQUEST MODELS ====================

class AnalisarTicketRequest(BaseModel):
    ticket_numero: str = Field(..., description="Número do ticket do Movidesk")
    usuario_nome: Optional[str] = Field(None, description="Nome do suporte que está usando")

class FeedbackRequest(BaseModel):
    analise_id: int
    foi_util: bool
    nota: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = None
    texto_final_usado: Optional[str] = None

class MarcarCopiado(BaseModel):
    analise_id: int

# ==================== RESPONSE MODELS ====================

class ResultadoIA(BaseModel):
    tipo: str  # 'inconsistencia', 'duvida', 'outro'
    modulo: Optional[str] = None
    chamado_texto: str
    metadata: Optional[dict] = None

class AnalisarTicketResponse(BaseModel):
    sucesso: bool
    analise_id: int
    ticket_numero: str
    resultado: ResultadoIA
    tempo_processamento_ms: int
    mensagem: Optional[str] = None

class FeedbackResponse(BaseModel):
    sucesso: bool
    feedback_id: int
    mensagem: str

class ModuloStats(BaseModel):
    modulo_identificado: str
    total: int

class EstatisticasResponse(BaseModel):
    total_analises: int
    total_inconsistencias: int
    taxa_aprovacao: float
    tempo_medio_ms: float
    modulos_top: List[ModuloStats]
    periodo_dias: int

class AnaliseRecente(BaseModel):
    id: int
    ticket_numero: str
    usuario_nome: Optional[str]
    data_analise: str
    tipo_identificado: Optional[str]
    modulo_identificado: Optional[str]
    foi_copiado: bool

class AnalisesRecentesResponse(BaseModel):
    analises: List[AnaliseRecente]
    total: int

