# 🤖 IA Chamados Sponte

Sistema inteligente para análise de tickets do Movidesk e geração automática de sugestões de chamados para o sistema Sponte.

## 📋 Sobre o Projeto

Esta aplicação utiliza Inteligência Artificial (Google Gemini) para:
- ✅ Ler conversas de atendimento do Movidesk
- ✅ Identificar inconsistências e bugs no sistema Sponte
- ✅ Gerar sugestões de chamados bem estruturados
- ✅ Coletar feedback para melhorar continuamente
- ✅ Gerar estatísticas e métricas de uso

## 🏗️ Arquitetura

### Backend (Python + FastAPI)
- **Framework**: FastAPI
- **IA**: Google Gemini API (gratuito)
- **Banco de Dados**: SQLite
- **API Externa**: Movidesk API

### Frontend (React + Vite)
- **Framework**: React 18
- **Build Tool**: Vite
- **Estilo**: CSS puro (inspirado no ChatGPT)
- **Roteamento**: React Router

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- npm ou yarn

### 1️⃣ Configurar Backend

```bash
# Entrar na pasta do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

**Configurar .env:**
```env
MOVIDESK_API_TOKEN=seu_token_movidesk_aqui
MOVIDESK_API_URL=https://api.movidesk.com/public/v1
GEMINI_API_KEY=sua_chave_gemini_aqui
DATABASE_PATH=ia_chamados.db
ENVIRONMENT=development
```

**Como obter Gemini API Key (GRATUITO):**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com conta Google
3. Clique em "Create API Key"
4. Copie a chave e cole no .env

```bash
# Iniciar servidor backend
python -m app.main

# Ou com uvicorn:
uvicorn app.main:app --reload --port 8000
```

Backend estará rodando em: http://localhost:8000

### 2️⃣ Configurar Frontend

```bash
# Em outro terminal, entrar na pasta frontend
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

Frontend estará rodando em: http://localhost:3000

## 📖 Como Usar

### 1. Analisar Ticket

1. Acesse http://localhost:3000
2. Digite o número de um ticket do Movidesk
3. (Opcional) Informe seu nome
4. Clique em "Analisar"
5. Aguarde a IA processar (2-5 segundos)
6. Copie a sugestão de chamado gerado
7. Dê feedback (👍/👎) para ajudar a melhorar

### 2. Ver Dashboard

1. Clique em "Dashboard" no menu
2. Veja estatísticas de uso:
   - Total de análises
   - Inconsistências detectadas
   - Taxa de aprovação
   - Tempo médio de processamento
   - Módulos mais afetados
3. Análises recentes

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **analises**: Log completo de todas as análises
- **feedbacks**: Avaliações dos usuários
- **tickets_cache**: Cache de tickets (24h)
- **estatisticas_diarias**: Métricas agregadas

## 🎯 Funcionalidades

### ✅ Implementadas

- [x] Integração com API Movidesk
- [x] Análise de tickets com IA (Gemini)
- [x] Geração de sugestões de chamados
- [x] Sistema de feedback
- [x] Cache inteligente (24h)
- [x] Dashboard de estatísticas
- [x] Interface moderna e responsiva
- [x] Modo MOCK (sem APIs configuradas)

### 🔮 Futuras Melhorias

- [ ] Autenticação de usuários
- [ ] Histórico de análises por usuário
- [ ] Exportar relatórios em PDF
- [ ] Integração direta com sistema de chamados
- [ ] Fine-tuning com exemplos reais
- [ ] Vector Database (RAG) para base conhecimento
- [ ] Deploy em produção

## 🧪 Modo de Demonstração

O sistema funciona em **modo MOCK** se você não configurar as APIs:

- **Sem Gemini API**: Retorna sugestões pré-programadas
- **Sem Movidesk API**: Usa dados mockados de ticket

Isso permite testar o sistema sem precisar de credenciais!

## 📊 Endpoints da API

### Análise
- `POST /api/analise/ticket` - Analisa um ticket
- `POST /api/analise/feedback` - Registra feedback
- `POST /api/analise/marcar-copiado` - Marca texto como copiado

### Estatísticas
- `GET /api/estatisticas/periodo/{dias}` - Estatísticas do período
- `GET /api/estatisticas/recentes` - Análises recentes
- `POST /api/estatisticas/limpar-cache` - Limpa cache expirado

### Documentação
- `GET /docs` - Swagger UI (documentação interativa)
- `GET /health` - Health check

## 🔧 Tecnologias Utilizadas

### Backend
- FastAPI
- Google Generative AI (Gemini)
- SQLite3
- httpx
- Pydantic
- python-dotenv

### Frontend
- React 18
- Vite
- React Router
- Axios
- Lucide React (ícones)
- React Markdown

## 📁 Estrutura do Projeto

```
IaChamadoN3/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   ├── db.py              # Classe Database
│   │   │   └── schema.sql         # Schema SQL
│   │   ├── models/
│   │   │   └── schemas.py         # Modelos Pydantic
│   │   ├── routers/
│   │   │   ├── analise.py         # Endpoints de análise
│   │   │   └── estatisticas.py   # Endpoints de stats
│   │   ├── services/
│   │   │   ├── ia_service.py      # Integração Gemini
│   │   │   └── movidesk_service.py # Integração Movidesk
│   │   └── main.py                # App principal
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TicketInput.jsx
│   │   │   └── ResultDisplay.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   └── DashboardPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── index.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verifique se o ambiente virtual está ativo
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Frontend com erro de CORS
- Certifique-se que o backend está rodando na porta 8000
- O vite.config.js está configurado com proxy

### Banco não cria
- Verifique permissões da pasta
- O banco é criado automaticamente na primeira execução

### IA não funciona
- Verifique GEMINI_API_KEY no .env
- Teste em modo MOCK primeiro (sem configurar API)

## 💡 Dicas

1. **Para desenvolvimento rápido**: Use modo MOCK (sem APIs)
2. **Para demonstração**: Configure apenas Gemini API
3. **Para produção**: Configure tudo + adicione autenticação

## 📝 Licença

Este projeto foi desenvolvido como MVP demonstrativo para N3 Suporte.

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📞 Contato

Desenvolvido para **Sponte - N3 Suporte**

---

**⚡ Versão**: 1.0.0  
**📅 Última atualização**: Outubro 2025

