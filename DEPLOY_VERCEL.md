# 🚀 Deploy no Vercel - Guia Passo a Passo

## 🎉 Deploy Realizado com Sucesso!

**Status**: ✅ Online  
**URL**: https://ia-chamados-sponte-c97u9qfge-igorkretzers-projects.vercel.app  
**Painel**: https://vercel.com/igorkretzers-projects/ia-chamados-sponte  
**Data**: 13 de Outubro de 2025

---

## ✅ Preparação Concluída!

- ✅ Seção "empty state" removida
- ✅ Build do frontend criado (pasta `frontend/dist`)
- ✅ Vercel CLI instalado
- ✅ Arquivos de configuração criados
- ✅ Deploy em produção realizado

---

## 📦 Deploy via CLI (Recomendado)

### Passo 1: Fazer Login no Vercel

```bash
cd /home/eduardo/Desktop/IaChamadoN3
vercel login
```

**O que vai acontecer:**
- Vercel vai pedir seu email
- Você receberá um email de confirmação
- Clique no link do email para autenticar

### Passo 2: Deploy do Projeto

```bash
cd /home/eduardo/Desktop/IaChamadoN3
vercel --prod
```

**Vercel vai perguntar:**

1. **"Set up and deploy?"** → `Y` (Yes)
2. **"Which scope?"** → Selecione `igorkretzers-projects`
3. **"Link to existing project?"** → `N` (No, criar novo)
4. **"What's your project's name?"** → `ia-chamados-sponte` (ou outro nome)
5. **"In which directory is your code located?"** → `./frontend`

**Vercel vai fazer o deploy automaticamente!** 🚀

---

## 🌐 Deploy via Interface Web (Alternativa)

### Opção 1: Conectar Repositório GitHub

1. Faça push do código para GitHub:
```bash
cd /home/eduardo/Desktop/IaChamadoN3
git init
git add .
git commit -m "Initial commit - IA Chamados Sponte"
git remote add origin https://github.com/seu-usuario/ia-chamados-sponte.git
git push -u origin main
```

2. Acesse: https://vercel.com/igorkretzers-projects
3. Clique em **"New Project"**
4. Selecione o repositório
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Clique em **"Deploy"**

### Opção 2: Upload Manual

1. Acesse: https://vercel.com/igorkretzers-projects
2. Clique em **"New Project"**
3. Clique em **"Continue with Other"**
4. Faça upload da pasta `frontend/dist`

---

## ⚙️ Configurações Importantes no Vercel

### Variáveis de Ambiente

Depois do deploy, configure a variável de ambiente:

1. Acesse seu projeto no Vercel
2. Vá em **Settings** > **Environment Variables**
3. Adicione:
   - **Name**: `VITE_API_URL`
   - **Value**: `http://localhost:8000` (ou URL do backend em produção)

### Rewrite Rules

O arquivo `vercel.json` já está configurado para redirecionar chamadas `/api/*` para o backend.

**Quando tiver o backend em produção**, edite `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://seu-backend-aqui.render.com/api/:path*"
    }
  ]
}
```

---

## 🎯 Deploy Rápido (Resumido)

```bash
# 1. Login
vercel login

# 2. Deploy
cd /home/eduardo/Desktop/IaChamadoN3
vercel --prod

# 3. Seguir instruções interativas
```

**Pronto!** Seu site estará online em segundos! 🚀

---

## 📋 Estrutura de Deploy

```
Vercel
└── Frontend (React + Vite)
    ├── Build: frontend/dist
    ├── URL: https://ia-chamados-sponte.vercel.app
    └── API Proxy: /api/* → Backend externo

Backend (Separado)
└── Deploy no Render.com, Railway, ou outro
    └── URL: https://seu-backend.com
```

---

## 🔧 Deploy do Backend (Opcional)

Se quiser fazer deploy do backend também:

### Render.com (Gratuito)

1. Acesse: https://render.com
2. Crie conta
3. **New Web Service**
4. Conecte GitHub
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m app.main`
   - **Environment**: Python 3.10+
6. Adicione variáveis de ambiente:
   - `GEMINI_API_KEY`
   - `MOVIDESK_API_TOKEN`

### Railway.app (Gratuito)

1. Acesse: https://railway.app
2. Crie conta
3. **New Project** > **Deploy from GitHub**
4. Selecione o repositório
5. Configure path: `backend`
6. Railway detecta Python automaticamente

---

## 📊 Após o Deploy

### URLs do Projeto

- **Frontend**: https://ia-chamados-sponte-c97u9qfge-igorkretzers-projects.vercel.app
- **Painel**: https://vercel.com/igorkretzers-projects/ia-chamados-sponte
- **Backend**: (configurar quando fizer deploy)

### Testar

1. Acesse a URL do frontend
2. Digite número de ticket
3. Clique em "Analisar"
4. Veja funcionando! ✨

---

## 🐛 Troubleshooting

### Erro: "Build failed"

```bash
# Rebuild local e teste
cd frontend
npm run build

# Se funcionar, faça deploy novamente
```

### Erro: "API não conecta"

- Verifique variável `VITE_API_URL` no Vercel
- Backend precisa estar online
- CORS configurado no backend

### Erro: "Module not found"

```bash
# Reinstalar dependências
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 🎉 Comandos Úteis

```bash
# Ver status do projeto
vercel ls

# Ver logs em tempo real
vercel logs

# Ver domínios
vercel domains ls

# Remover deployment
vercel rm ia-chamados-sponte
```

---

## 📝 Checklist de Deploy

- [x] Build local testado
- [x] Vercel CLI instalado
- [x] Login no Vercel feito
- [x] Deploy executado
- [ ] Variáveis de ambiente configuradas
- [x] Site funcionando
- [ ] Backend conectado (se aplicável)

---

## 🚀 EXECUTE AGORA

```bash
vercel login
vercel --prod
```

**É só isso!** 🎉

---

**Links Úteis:**
- Vercel Docs: https://vercel.com/docs
- Seu Dashboard: https://vercel.com/igorkretzers-projects

