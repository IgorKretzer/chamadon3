from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import analise, estatisticas
from app.database.db import Database

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa banco de dados
db = Database(os.getenv("DATABASE_PATH", "ia_chamados.db"))

# Cria app FastAPI
app = FastAPI(
    title="IA Chamados Sponte",
    description="API para análise de tickets e geração de chamados com IA",
    version="1.0.0"
)

# Configuração CORS (permite acesso do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra routers
app.include_router(analise.router)
app.include_router(estatisticas.router)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "mensagem": "IA Chamados Sponte - API ativa",
        "versao": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

