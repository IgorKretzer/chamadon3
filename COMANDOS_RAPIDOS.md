# ⚡ Comandos Rápidos - IA Chamados Sponte

## 🚀 Iniciar Projeto

### Forma Mais Rápida
```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### Manualmente

**Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

python -m app.main
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## 📦 Instalação Inicial

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

## 🔧 Configuração

**Criar .env do backend:**
```bash
cd backend
cp .env.example .env
# Editar .env com suas credenciais
```

**Chave Gemini (gratuita):**
- Acesse: https://makersuite.google.com/app/apikey
- Cole no .env: `GEMINI_API_KEY=sua_chave`

---

## 🧪 Testar

**Health check backend:**
```bash
curl http://localhost:8000/health
```

**Analisar ticket via API:**
```bash
curl -X POST http://localhost:8000/api/analise/ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_numero": "12345"}'
```

**Estatísticas:**
```bash
curl http://localhost:8000/api/estatisticas/periodo/7
```

---

## 🗄️ Banco de Dados

**Ver tabelas:**
```bash
cd backend
sqlite3 ia_chamados.db ".tables"
```

**Ver análises:**
```bash
sqlite3 ia_chamados.db "SELECT * FROM analises LIMIT 5;"
```

**Limpar banco:**
```bash
rm ia_chamados.db
# Será recriado automaticamente ao reiniciar
```

---

## 🐛 Debug

**Logs do backend:**
```bash
# O terminal onde rodou python -m app.main
# mostra todos os logs em tempo real
```

**Logs do frontend:**
```bash
# Abra DevTools no navegador (F12)
# Vá para aba Console
```

**Reinstalar dependências:**
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🔄 Atualizar Projeto

**Atualizar dependências:**
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

**Limpar cache:**
```bash
# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Node cache
npm cache clean --force
```

---

## 📊 Estatísticas do Banco

**Total de análises:**
```bash
sqlite3 ia_chamados.db "SELECT COUNT(*) FROM analises;"
```

**Taxa de aprovação:**
```bash
sqlite3 ia_chamados.db "
  SELECT 
    ROUND(
      (SELECT COUNT(*) FROM feedbacks WHERE foi_util = 1) * 100.0 / 
      (SELECT COUNT(*) FROM feedbacks)
    , 2) as taxa_aprovacao;
"
```

**Módulos mais afetados:**
```bash
sqlite3 ia_chamados.db "
  SELECT modulo_identificado, COUNT(*) as total 
  FROM analises 
  GROUP BY modulo_identificado 
  ORDER BY total DESC 
  LIMIT 5;
"
```

---

## 🔍 Verificar Status

**Processos rodando:**
```bash
# Backend
lsof -i :8000

# Frontend
lsof -i :3000
```

**Matar processos:**
```bash
kill -9 $(lsof -t -i:8000)  # Backend
kill -9 $(lsof -t -i:3000)  # Frontend
```

---

## 📁 Estrutura Rápida

```
backend/        → Python + FastAPI
  app/
    main.py     → 🚪 Entry point
    routers/    → 🛣️ Endpoints
    services/   → 🔧 Lógica de negócio
    database/   → 🗄️ Banco de dados
    models/     → 📋 Schemas

frontend/       → React + Vite
  src/
    App.jsx     → 🏠 App principal
    pages/      → 📄 Páginas
    components/ → 🧩 Componentes
    services/   → 🔌 API client
    styles/     → 🎨 CSS
```

---

## 🌐 URLs Importantes

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 💾 Backup

**Fazer backup do banco:**
```bash
cp backend/ia_chamados.db backup_$(date +%Y%m%d).db
```

**Fazer backup completo:**
```bash
cd ..
tar -czf IaChamadoN3_backup_$(date +%Y%m%d).tar.gz IaChamadoN3/
```

---

## 🚀 Deploy (Futuro)

**Backend (Render.com):**
```bash
# Criar conta no Render.com
# Conectar repositório GitHub
# Configurar variáveis de ambiente
# Deploy automático!
```

**Frontend (Vercel):**
```bash
cd frontend
npm run build
# Deploy via Vercel CLI ou GitHub
```

---

## 📝 Documentação

- `README.md` - Documentação completa
- `SETUP.md` - Instalação rápida
- `TESTES.md` - Checklist de testes
- `RESUMO_PROJETO.md` - Visão geral
- `CHANGELOG.md` - Histórico
- Este arquivo - Comandos rápidos

---

## 🎯 Atalhos de Desenvolvimento

**Reiniciar backend rapidamente:**
```bash
# Ctrl+C para parar
# Seta para cima para comando anterior
# Enter
```

**Ver logs filtrados:**
```bash
# Backend (apenas erros)
python -m app.main 2>&1 | grep -i error

# Frontend (apenas warnings)
npm run dev 2>&1 | grep -i warn
```

**Formatar código:**
```bash
# Python
black backend/app/

# JavaScript
cd frontend
npx prettier --write src/
```

---

## 🔑 Variáveis de Ambiente

**Backend (.env):**
```env
MOVIDESK_API_TOKEN=seu_token
MOVIDESK_API_URL=https://api.movidesk.com/public/v1
GEMINI_API_KEY=sua_chave
DATABASE_PATH=ia_chamados.db
PORT=8000
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

---

## 🎨 Customização Rápida

**Mudar porta do backend:**
```python
# backend/app/main.py (última linha)
uvicorn.run(app, host="0.0.0.0", port=8080)  # Era 8000
```

**Mudar porta do frontend:**
```javascript
// frontend/vite.config.js
server: {
  port: 3001  // Era 3000
}
```

**Mudar cores:**
```css
/* frontend/src/styles/index.css */
:root {
  --color-primary: #10a37f;  /* Sua cor aqui */
}
```

---

**⚡ Comandos sempre à mão!**

