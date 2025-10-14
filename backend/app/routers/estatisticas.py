from fastapi import APIRouter, HTTPException
from app.models.schemas import EstatisticasResponse, AnalisesRecentesResponse, AnaliseRecente, ModuloStats
from app.database.db import Database

router = APIRouter(prefix="/api/estatisticas", tags=["Estatísticas"])

db = Database()

@router.get("/periodo/{dias}", response_model=EstatisticasResponse)
async def get_estatisticas(dias: int = 7):
    """
    Retorna estatísticas dos últimos N dias
    """
    try:
        stats = db.get_estatisticas_periodo(dias)
        
        # Converte modulos_top para o modelo correto
        modulos_formatados = [
            ModuloStats(**modulo) for modulo in stats['modulos_top']
        ]
        
        return EstatisticasResponse(
            total_analises=stats['total_analises'],
            total_inconsistencias=stats['total_inconsistencias'],
            taxa_aprovacao=stats['taxa_aprovacao'],
            tempo_medio_ms=stats['tempo_medio_ms'],
            modulos_top=modulos_formatados,
            periodo_dias=dias
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {str(e)}")

@router.get("/recentes", response_model=AnalisesRecentesResponse)
async def get_analises_recentes(limit: int = 10):
    """
    Retorna as análises mais recentes
    """
    try:
        analises = db.get_analises_recentes(limit)
        
        analises_formatadas = [
            AnaliseRecente(**analise) for analise in analises
        ]
        
        return AnalisesRecentesResponse(
            analises=analises_formatadas,
            total=len(analises_formatadas)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar análises: {str(e)}")

@router.post("/limpar-cache")
async def limpar_cache():
    """
    Remove cache expirado
    """
    try:
        deletados = db.limpar_cache_expirado()
        return {
            "sucesso": True,
            "mensagem": f"{deletados} registros de cache removidos"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar cache: {str(e)}")

@router.delete("/limpar-analises")
async def limpar_analises():
    """
    Remove todas as análises do banco de dados
    """
    try:
        deletados = db.limpar_todas_analises()
        return {
            "sucesso": True,
            "mensagem": f"{deletados} análises removidas com sucesso",
            "total_deletado": deletados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar análises: {str(e)}")

