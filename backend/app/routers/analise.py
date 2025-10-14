from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AnalisarTicketRequest, 
    AnalisarTicketResponse,
    FeedbackRequest,
    FeedbackResponse,
    MarcarCopiado,
    ResultadoIA
)
from app.services.movidesk_service import MovideskService
from app.services.ia_service import IAService
from app.database.db import Database
import time

router = APIRouter(prefix="/api/analise", tags=["Análise"])

# Inicializa serviços
movidesk_service = MovideskService()
ia_service = IAService()
db = Database()

@router.post("/ticket", response_model=AnalisarTicketResponse)
async def analisar_ticket(request: AnalisarTicketRequest):
    """
    Analisa um ticket do Movidesk e gera sugestão de chamado
    """
    try:
        inicio = time.time()
        
        # 1. Verifica cache
        dados_cache = db.get_cache_ticket(request.ticket_numero)
        
        if dados_cache:
            print(f"✅ Usando cache para ticket {request.ticket_numero}")
            dados_ticket = dados_cache
        else:
            # 2. Busca ticket no Movidesk
            print(f"🔍 Buscando ticket {request.ticket_numero} no Movidesk...")
            dados_ticket = await movidesk_service.get_ticket(request.ticket_numero)
            
            # Salva no cache
            db.salvar_cache_ticket(request.ticket_numero, dados_ticket)
        
        # 3. Analisa com IA
        print(f"🤖 Analisando ticket com IA...")
        resultado_ia = await ia_service.analisar_ticket(dados_ticket)
        
        # 4. Calcula tempo
        fim = time.time()
        tempo_ms = int((fim - inicio) * 1000)
        
        # 5. Registra no banco
        analise_id = db.registrar_analise(
            ticket_numero=request.ticket_numero,
            dados_movidesk=dados_ticket,
            resultado_ia=resultado_ia,
            tempo_ms=tempo_ms,
            usuario=request.usuario_nome
        )
        
        print(f"✅ Análise concluída em {tempo_ms}ms (ID: {analise_id})")
        
        return AnalisarTicketResponse(
            sucesso=True,
            analise_id=analise_id,
            ticket_numero=request.ticket_numero,
            resultado=ResultadoIA(**resultado_ia),
            tempo_processamento_ms=tempo_ms,
            mensagem="Análise realizada com sucesso"
        )
        
    except Exception as e:
        print(f"❌ Erro ao analisar ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao analisar ticket: {str(e)}")

@router.post("/feedback", response_model=FeedbackResponse)
async def registrar_feedback(request: FeedbackRequest):
    """
    Registra feedback do suporte sobre a análise
    """
    try:
        feedback_id = db.registrar_feedback(
            analise_id=request.analise_id,
            foi_util=request.foi_util,
            nota=request.nota,
            comentario=request.comentario,
            texto_final=request.texto_final_usado
        )
        
        emoji = "👍" if request.foi_util else "👎"
        print(f"{emoji} Feedback registrado (ID: {feedback_id})")
        
        return FeedbackResponse(
            sucesso=True,
            feedback_id=feedback_id,
            mensagem="Feedback registrado com sucesso"
        )
        
    except Exception as e:
        print(f"❌ Erro ao registrar feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar feedback: {str(e)}")

@router.post("/marcar-copiado")
async def marcar_copiado(request: MarcarCopiado):
    """
    Marca que o suporte copiou o texto do chamado
    """
    try:
        db.marcar_como_copiado(request.analise_id)
        return {"sucesso": True, "mensagem": "Marcado como copiado"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

