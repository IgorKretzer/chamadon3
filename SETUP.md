# 🚀 Guia de Setup Rápido - IA Chamados Sponte

## ⚡ Setup Express (5 minutos)

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Criar .env (pode deixar vazio para modo MOCK)
touch .env

# Iniciar
python -m app.main
```

✅ Backend rodando em http://localhost:8000

### 2. Frontend

```bash
# Em outro terminal
cd frontend
npm install
npm run dev
```

✅ Frontend rodando em http://localhost:3000

## 🎯 Teste Rápido

1. Abra http://localhost:3000
2. Digite qualquer número (ex: 12345)
3. Clique em "Analisar"
4. Veja a sugestão gerada (modo MOCK)

## 🔑 Configurar APIs (Opcional)

### Google Gemini (Gratuito)

1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma API Key
3. Cole no backend/.env:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### Movidesk

Cole no backend/.env:

```env
MOVIDESK_API_TOKEN=seu_token
MOVIDESK_API_URL=https://api.movidesk.com/public/v1
```

## ✅ Checklist de Sucesso

- [ ] Backend iniciou sem erros
- [ ] Frontend carregou a interface
- [ ] Conseguiu analisar um ticket
- [ ] Dashboard mostra estatísticas
- [ ] Conseguiu copiar texto gerado

## 🐛 Problemas Comuns

**Erro: "Module not found"**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Erro: "Port already in use"**
```bash
# Mude a porta
# Backend: python -m app.main (edite main.py linha do uvicorn)
# Frontend: vite.config.js (mude server.port)
```

**Banco não cria**
- É normal! Ele cria automaticamente na primeira análise

## 📊 Próximos Passos

1. ✅ Testar com dados reais do Movidesk
2. ✅ Configurar Gemini API
3. ✅ Coletar feedback de usuários reais
4. ✅ Apresentar para gestores com dashboard

---

**Dúvidas?** Consulte o README.md completo

