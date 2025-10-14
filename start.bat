@echo off
REM Script de inicialização - IA Chamados Sponte (Windows)

echo 🚀 Iniciando IA Chamados Sponte...
echo.

REM Verifica se está na pasta correta
if not exist "backend" (
    echo ❌ Execute este script na pasta raiz do projeto!
    exit /b 1
)

REM Iniciar Backend
echo 📦 Iniciando Backend...
cd backend

REM Verifica ambiente virtual
if not exist "venv" (
    echo ⚠️  Ambiente virtual não encontrado. Criando...
    python -m venv venv
)

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Instala dependências
if not exist "venv\installed" (
    echo 📥 Instalando dependências do backend...
    pip install -r requirements.txt
    echo. > venv\installed
)

REM Verifica .env
if not exist ".env" (
    echo ⚠️  Arquivo .env não encontrado. Criando...
    copy .env.example .env
    echo ✏️  Configure o arquivo backend\.env com suas credenciais!
)

REM Inicia backend
echo ✅ Iniciando servidor backend na porta 8000...
start "Backend - IA Chamados" cmd /k python -m app.main

cd ..

REM Aguarda backend
timeout /t 3 /nobreak >nul

REM Iniciar Frontend
echo 📦 Iniciando Frontend...
cd frontend

REM Instala dependências
if not exist "node_modules" (
    echo 📥 Instalando dependências do frontend...
    call npm install
)

REM Verifica .env
if not exist ".env" (
    echo VITE_API_URL=http://localhost:8000 > .env
)

echo ✅ Iniciando servidor frontend na porta 3000...
start "Frontend - IA Chamados" cmd /k npm run dev

cd ..

echo.
echo ✅ Sistema iniciado com sucesso!
echo.
echo 📍 URLs:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    Docs:     http://localhost:8000/docs
echo.
echo Pressione qualquer tecla para sair...
pause >nul

