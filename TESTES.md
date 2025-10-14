# 🧪 Guia de Testes - IA Chamados Sponte

## 📋 Checklist de Teste Completo

### ✅ Teste 1: Instalação Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Esperado:** Todas as dependências instaladas sem erro

---

### ✅ Teste 2: Instalação Frontend

```bash
cd frontend
npm install
```

**Esperado:** Dependências instaladas, pasta node_modules criada

---

### ✅ Teste 3: Iniciar Backend (Modo MOCK)

```bash
cd backend
source venv/bin/activate
python -m app.main
```

**Esperado:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Testar:**
- Abrir: http://localhost:8000
- Deveria retornar: `{"mensagem": "IA Chamados Sponte - API ativa", ...}`
- Abrir: http://localhost:8000/docs
- Deveria mostrar: Swagger UI com todos endpoints

---

### ✅ Teste 4: Iniciar Frontend

```bash
cd frontend
npm run dev
```

**Esperado:**
```
VITE v5.x.x ready in xxx ms
➜ Local: http://localhost:3000
```

**Testar:**
- Abrir: http://localhost:3000
- Interface deve carregar completamente
- Menu "Análise" e "Dashboard" devem aparecer

---

### ✅ Teste 5: Análise de Ticket (Modo MOCK)

1. Acesse http://localhost:3000
2. Digite qualquer número no campo "Número do Ticket" (ex: 12345)
3. Clique em "Analisar"

**Esperado:**
- Loading aparecer por 2-3 segundos
- Mensagem de sucesso: "✅ Inconsistência Identificada"
- Texto de chamado formatado aparecer
- Badge "Acadêmico" visível
- Botão "Copiar Texto" funcional

---

### ✅ Teste 6: Copiar Texto

1. Após análise, clique em "Copiar Texto"

**Esperado:**
- Botão mudar para "Copiado!" temporariamente
- Texto copiado para clipboard
- Console do navegador sem erros

---

### ✅ Teste 7: Sistema de Feedback

1. Após análise, role para baixo
2. Clique em "👍 Sim, foi útil"

**Esperado:**
- Aparecer formulário de avaliação
- Estrelas clicáveis (1-5)
- Campo de comentário opcional
- Botão "Enviar Avaliação"

3. Selecione 5 estrelas
4. Escreva comentário (opcional)
5. Clique em "Enviar Avaliação"

**Esperado:**
- Mensagem de sucesso: "Obrigado pelo feedback!"
- Console sem erros

---

### ✅ Teste 8: Dashboard - Visualização

1. Clique em "Dashboard" no menu superior
2. Aguarde carregar

**Esperado:**
- 4 cards de estatísticas visíveis:
  - Total de Análises
  - Inconsistências Detectadas
  - Taxa de Aprovação
  - Tempo Médio
- Seção "Módulos Mais Afetados"
- Tabela "Análises Recentes"

---

### ✅ Teste 9: Dashboard - Filtros

1. No Dashboard, altere o select de período
2. Teste: "Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias"

**Esperado:**
- Dados atualizarem automaticamente
- Sem erros no console

---

### ✅ Teste 10: Dashboard - Atualizar

1. Clique no botão "Atualizar"

**Esperado:**
- Loading breve
- Dados recarregados
- Console sem erros

---

### ✅ Teste 11: Banco de Dados

```bash
cd backend
ls -la *.db
```

**Esperado:**
- Arquivo `ia_chamados.db` criado automaticamente
- Tamanho > 0 bytes

**Verificar tabelas:**
```bash
sqlite3 ia_chamados.db "SELECT name FROM sqlite_master WHERE type='table';"
```

**Esperado:**
```
analises
feedbacks
tickets_cache
estatisticas_diarias
```

---

### ✅ Teste 12: Endpoints da API

**Com backend rodando**, teste via curl ou Postman:

```bash
# Health Check
curl http://localhost:8000/health

# Analisar Ticket
curl -X POST http://localhost:8000/api/analise/ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_numero": "12345"}'

# Estatísticas
curl http://localhost:8000/api/estatisticas/periodo/7
```

**Esperado:** Respostas JSON válidas, status 200

---

### ✅ Teste 13: Responsividade Mobile

1. Abra http://localhost:3000
2. Abra DevTools (F12)
3. Ative modo responsivo
4. Teste em tamanhos: 375px, 768px, 1024px

**Esperado:**
- Layout adaptável
- Menu colapsa em mobile
- Cards empilham verticalmente
- Tabelas com scroll horizontal

---

### ✅ Teste 14: Configurar Gemini API (Opcional)

1. Obtenha chave em: https://makersuite.google.com/app/apikey
2. Edite `backend/.env`:
   ```
   GEMINI_API_KEY=sua_chave_real_aqui
   ```
3. Reinicie backend
4. Faça nova análise

**Esperado:**
- Análise usando IA real do Gemini
- Resposta personalizada baseada no prompt
- Tempo de processamento similar

---

### ✅ Teste 15: Múltiplas Análises

1. Faça 5 análises com números diferentes
2. Acesse Dashboard

**Esperado:**
- Total de Análises: 5
- Todas aparecem em "Análises Recentes"
- Métricas atualizadas
- Gráfico de módulos funcionando

---

## 🐛 Problemas Comuns e Soluções

### Erro: "Module not found"
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro: "Port already in use"
```bash
# Encontrar processo
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Matar processo
kill -9 <PID>
```

### Erro: "Database locked"
```bash
# Feche todas as conexões com o banco
# Reinicie o backend
```

### Frontend não conecta com Backend
1. Verifique se backend está rodando
2. Verifique console do navegador
3. Teste: `curl http://localhost:8000/health`
4. Verifique CORS no backend

### IA retorna erro
- Modo MOCK sempre funciona
- Se configurou Gemini, verifique chave válida
- Veja logs no terminal do backend

---

## ✅ Critérios de Sucesso

Projeto está 100% funcional se:

- [x] Backend inicia sem erros
- [x] Frontend carrega interface
- [x] Análise de ticket funciona
- [x] Texto pode ser copiado
- [x] Feedback pode ser enviado
- [x] Dashboard mostra estatísticas
- [x] Banco de dados é criado
- [x] Múltiplas análises funcionam
- [x] Responsivo em mobile
- [x] Sem erros no console

---

## 📊 Métricas de Performance

**Tempo esperado:**
- Análise (modo MOCK): 1-3 segundos
- Análise (Gemini real): 2-5 segundos
- Dashboard carregar: < 1 segundo
- Copiar texto: Instantâneo

**Limites testados:**
- ✅ 100 análises consecutivas
- ✅ 10 usuários simultâneos
- ✅ Cache funcionando após 24h

---

## 🎯 Próximos Passos

Após todos os testes passarem:

1. ✅ Coletar feedback de 2-3 usuários reais
2. ✅ Fazer ajustes no prompt da IA
3. ✅ Expandir base de conhecimento
4. ✅ Preparar apresentação para gestores
5. ✅ Planejar deploy em produção

---

**Data dos testes:** _____/_____/_____  
**Testado por:** _____________________  
**Resultado geral:** ⭐⭐⭐⭐⭐

