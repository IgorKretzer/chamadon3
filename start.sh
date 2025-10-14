#!/bin/bash

# Script de inicialização - IA Chamados Sponte

echo "🚀 Iniciando IA Chamados Sponte..."
echo ""

# Verifica se está na pasta correta
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Execute este script na pasta raiz do projeto!"
    exit 1
fi

# Iniciar Backend
echo "📦 Iniciando Backend..."
cd backend

# Verifica ambiente virtual
if [ ! -d "venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativa ambiente virtual
source venv/bin/activate

# Instala dependências se necessário
if [ ! -f "venv/installed" ]; then
    echo "📥 Instalando dependências do backend..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Verifica .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando a partir do exemplo..."
    cp .env.example .env
    echo "✏️  Configure o arquivo backend/.env com suas credenciais!"
fi

# Inicia backend em background
echo "✅ Iniciando servidor backend na porta 8000..."
python -m app.main &
BACKEND_PID=$!

cd ..

# Aguarda backend iniciar
echo "⏳ Aguardando backend inicializar..."
sleep 3

# Iniciar Frontend
echo "📦 Iniciando Frontend..."
cd frontend

# Instala dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências do frontend..."
    npm install
fi

# Verifica .env
if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || echo "VITE_API_URL=http://localhost:8000" > .env
fi

echo "✅ Iniciando servidor frontend na porta 3000..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Sistema iniciado com sucesso!"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Docs:     http://localhost:8000/docs"
echo ""
echo "Para parar: Ctrl+C"
echo ""

# Aguarda Ctrl+C
trap "echo ''; echo '🛑 Parando servidores...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

