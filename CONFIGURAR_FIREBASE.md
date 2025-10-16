# 🔥 Configuração do Firebase

Este guia explica como configurar o Firebase para o sistema IA Chamados Sponte.

## 📋 Pré-requisitos

1. **Conta Google** (gratuita)
2. **Projeto Firebase** criado
3. **Service Account** configurado

---

## 🚀 Passo 1: Criar Projeto no Firebase

1. **Acesse:** https://console.firebase.google.com/
2. **Clique:** "Adicionar projeto"
3. **Nome:** `ia-chamados-sponte` (ou o que preferir)
4. **Analytics:** Pode desabilitar por enquanto
5. **Clique:** "Criar projeto"

---

## 🔑 Passo 2: Configurar Service Account

### 2.1 Acessar Configurações do Projeto
1. No console Firebase, clique na **engrenagem** ⚙️
2. **Selecione:** "Configurações do projeto"
3. **Aba:** "Contas de serviço"

### 2.2 Gerar Chave Privada
1. **Selecione:** "Python" na seção "SDK do Admin"
2. **Clique:** "Gerar nova chave privada"
3. **Baixe** o arquivo JSON (ex: `firebase-adminsdk-xxxxx.json`)

### 2.3 Configurar Firestore
1. **No menu lateral:** "Firestore Database"
2. **Clique:** "Criar banco de dados"
3. **Modo:** "Começar no modo de teste" (por enquanto)
4. **Localização:** Escolha a mais próxima do Brasil
5. **Clique:** "Próximo" → "Ativar"

---

## ⚙️ Passo 3: Configurar no Sistema

### 3.1 Opção A: Arquivo de Credenciais (Recomendado para desenvolvimento)

1. **Copie** o arquivo baixado para:
   ```
   backend/firebase-service-account.json
   ```

2. **Configure** a variável de ambiente:
   ```bash
   export FIREBASE_SERVICE_ACCOUNT_PATH="/caminho/para/firebase-service-account.json"
   ```

### 3.2 Opção B: Variável de Ambiente (Recomendado para produção)

1. **Abra** o arquivo JSON baixado
2. **Copie** todo o conteúdo JSON
3. **Configure** no Render:
   ```
   FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
   ```

---

## 🔧 Passo 4: Instalar Dependências

```bash
cd backend
pip install firebase-admin==6.5.0
```

---

## 🧪 Passo 5: Testar Configuração

```bash
cd backend
export FIREBASE_SERVICE_ACCOUNT_PATH="./firebase-service-account.json"
python3 -c "
from app.services.firebase_service import firebase_service
print('Firebase conectado:' if firebase_service.is_connected() else 'Firebase NÃO conectado')
"
```

---

## 📊 Estrutura dos Dados no Firebase

### Coleções que serão criadas:

#### 📝 `analises`
```json
{
  "ticket_numero": "12345",
  "usuario_nome": "João",
  "titulo_ticket": "Erro no sistema",
  "cliente_nome": "Cliente ABC",
  "tipo_identificado": "inconsistencia",
  "modulo_identificado": "Financeiro",
  "chamado_gerado": "VERSÃO DO SISTEMA...",
  "tempo_processamento_ms": 5000,
  "tokens_usados": 2500,
  "data_analise": "2025-10-16T19:30:00Z",
  "foi_copiado": false,
  "metadata": {...},
  "dados_movidesk_completos": {...}
}
```

#### 👍 `feedbacks`
```json
{
  "analise_id": "abc123",
  "foi_util": true,
  "nota": 5,
  "comentario": "Muito útil!",
  "texto_final_usado": "VERSÃO DO SISTEMA...",
  "data_feedback": "2025-10-16T19:35:00Z"
}
```

#### 💾 `tickets_cache`
```json
{
  "dados_movidesk": {...},
  "data_cache": "2025-10-16T19:30:00Z",
  "expira_em": "2025-10-17T19:30:00Z"
}
```

---

## 🚀 Deploy no Render

### Variáveis de Ambiente no Render:
```
GEMINI_API_KEY=AIzaSyC0PXSAHa8u40_TvGXrEIqRDtsaHY9dFRs
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

---

## ✅ Verificar se Funcionou

1. **Teste** um ticket no frontend
2. **Verifique** no console Firebase se os dados aparecem
3. **Logs** devem mostrar:
   ```
   ✅ Firebase inicializado com service account
   ✅ Firestore conectado com sucesso!
   ✅ Análise salva no Firebase com ID: abc123
   ```

---

## 🔒 Segurança

- **NUNCA** commite o arquivo `firebase-service-account.json`
- **Use** variáveis de ambiente em produção
- **Configure** regras do Firestore adequadamente
- **Monitore** o uso e custos no console Firebase

---

## 💰 Custos

- **Firestore:** Gratuito até 1GB de dados e 50.000 leituras/dia
- **Para** o uso atual do sistema, deve ficar dentro do plano gratuito
- **Monitore** no console Firebase → "Uso"

---

## 🆘 Troubleshooting

### Erro: "Permission denied"
- Verifique se o Firestore está no modo de teste
- Ou configure regras adequadas

### Erro: "Invalid credentials"
- Verifique se o arquivo JSON está correto
- Ou se a variável de ambiente está configurada

### Erro: "Project not found"
- Verifique se o project_id está correto
- E se o projeto Firebase existe
