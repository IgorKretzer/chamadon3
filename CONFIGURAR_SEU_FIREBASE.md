# 🔥 Configurar Firebase - Projeto ia-chamado-n3

## ✅ Projeto já criado!
- **Projeto:** `ia-chamado-n3`
- **URL:** https://console.firebase.google.com/u/0/project/ia-chamado-n3/firestore/databases/-default-/data

---

## 🔑 Passo 1: Gerar Service Account

### 1.1 Acesse o Console
1. **Abra:** https://console.firebase.google.com/u/0/project/ia-chamado-n3/settings/serviceaccounts/adminsdk
2. **Faça login** com sua conta Google

### 1.2 Gerar Chave Privada
1. **Selecione:** "Python" na seção "SDK do Admin"
2. **Clique:** "Gerar nova chave privada"
3. **Baixe** o arquivo JSON (ex: `ia-chamado-n3-firebase-adminsdk-xxxxx.json`)

---

## ⚙️ Passo 2: Configurar no Sistema

### 2.1 Copiar arquivo para o projeto
```bash
# Copie o arquivo baixado para o backend
cp ~/Downloads/ia-chamado-n3-firebase-adminsdk-xxxxx.json /home/eduardo/Desktop/IaChamadoN3/backend/firebase-service-account.json
```

### 2.2 Configurar variável de ambiente
```bash
export FIREBASE_SERVICE_ACCOUNT_PATH="/home/eduardo/Desktop/IaChamadoN3/backend/firebase-service-account.json"
```

---

## 🧪 Passo 3: Testar Conexão

```bash
cd /home/eduardo/Desktop/IaChamadoN3/backend
export FIREBASE_SERVICE_ACCOUNT_PATH="./firebase-service-account.json"
python3 -c "
from app.services.firebase_service import firebase_service
print('🔥 Firebase Status:')
print(f'   Conectado: {firebase_service.is_connected()}')
if firebase_service.is_connected():
    print('   ✅ Pronto para salvar análises no Firebase!')
else:
    print('   ❌ Verifique as credenciais')
"
```

---

## 🚀 Passo 4: Testar com Análise Real

```bash
# Com o backend rodando
curl -X POST http://localhost:8000/api/analise/ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_numero": "12345", "usuario_nome": "Teste Firebase"}'
```

---

## 📊 Verificar no Console Firebase

Após o teste, acesse:
https://console.firebase.google.com/u/0/project/ia-chamado-n3/firestore/databases/-default-/data

Você deve ver as coleções:
- 📝 `analises` - com os dados da análise
- 👍 `feedbacks` - quando houver feedback
- 💾 `tickets_cache` - cache dos tickets

---

## 🔧 Para Produção (Render)

No dashboard do Render, adicione:
```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"ia-chamado-n3",...}
```

(Use o conteúdo completo do arquivo JSON como valor da variável)
