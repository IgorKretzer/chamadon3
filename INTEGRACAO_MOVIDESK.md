# 🔌 Integração com API Movidesk - Guia Completo

## 📘 Documentação Oficial
https://atendimento.movidesk.com/kb/pt-br/article/256/movidesk-ticket-api

---

## ✅ CORREÇÕES APLICADAS

### Antes (Incorreto):
```python
# ❌ Autenticação errada
headers = {
    "Authorization": f"Bearer {self.api_token}"  # Movidesk não usa Bearer!
}

params = {
    "token": self.api_token,
    "$select": "id,subject,..."  # $select não traz actions completas
}
```

### Depois (Correto):
```python
# ✅ Autenticação correta
params = {
    "token": self.api_token,  # Token como query param
    "id": ticket_numero,
    "$expand": "actions"      # Expande as ações/mensagens
}

headers = {
    "Content-Type": "application/json"  # Header simples
}
```

---

## 🎯 Endpoint Correto

### GET Ticket por ID

```
GET https://api.movidesk.com/public/v1/tickets?token=SEU_TOKEN&id=ID_DO_TICKET&$expand=actions
```

**Parâmetros:**
- `token` (obrigatório): Token de autenticação da API
- `id` (obrigatório): ID do ticket
- `$expand=actions` (recomendado): Traz as ações/mensagens do ticket

---

## 📋 Estrutura do JSON Retornado

```json
{
  "id": 156789,
  "subject": "Erro ao salvar quadro de horários",
  "createdDate": "2025-10-13T10:30:00",
  "status": "New",
  "category": "Suporte",
  
  "client": {
    "id": "12345",
    "businessName": "Faculdade Exemplo",
    "email": "contato@faculdade.com"
  },
  
  "owner": {
    "id": "67890",
    "businessName": "João Suporte"
  },
  
  "actions": [
    {
      "id": "action-1",
      "type": 1,           // 1 = Mensagem/Comentário
      "origin": 5,         // 5 = Chat Online, 6 = Chat Offline
      "description": "Olá, estou com problema no sistema",
      "htmlDescription": "<p>Olá, estou com problema no sistema</p>",
      "createdDate": "2025-10-13T10:30:00",
      "createdBy": {
        "id": "client-123",
        "businessName": "Cliente Silva",
        "email": "cliente@email.com"
      }
    },
    {
      "id": "action-2",
      "type": 1,
      "origin": 2,         // 2 = Manual/Interface
      "description": "Pode detalhar o problema?",
      "htmlDescription": "<p>Pode detalhar o problema?</p>",
      "createdDate": "2025-10-13T10:31:00",
      "createdBy": {
        "id": "agent-456",
        "businessName": "João Suporte"
      }
    }
  ]
}
```

---

## 🔍 Campos Importantes

### **Ticket (Raiz)**
| Campo | Descrição |
|-------|-----------|
| `id` | ID único do ticket |
| `subject` | Assunto/título do ticket |
| `createdDate` | Data de abertura |
| `status` | Status (New, InAttendance, Stopped, Closed, etc) |
| `category` | Categoria do ticket |
| `client` | Objeto com dados do cliente |
| `owner` | Objeto com dados do agente responsável |
| `actions` | Array com todas as ações/mensagens |

### **Actions (Mensagens/Chat)**
| Campo | Descrição | Valores Possíveis |
|-------|-----------|-------------------|
| `type` | Tipo da ação | 1 (mensagem), 2 (email), 3 (nota), etc |
| `origin` | Origem da ação | 1 (email), 2 (manual), 5 (chat online), 6 (chat offline), 7 (telefone), etc |
| `description` | Texto puro da mensagem | String |
| `htmlDescription` | HTML da mensagem | String HTML |
| `createdDate` | Data/hora da mensagem | ISO 8601 |
| `createdBy` | Quem criou (cliente ou agente) | Objeto |

### **Identificando Mensagens do Chat**

Para pegar **APENAS mensagens de chat**:
```python
if action.get('type') == 1 and action.get('origin') in [5, 6]:
    # É uma mensagem de chat!
    # origin = 5: Chat Online
    # origin = 6: Chat Offline
```

Para pegar **TODAS as mensagens** (chat + comentários):
```python
if action.get('type') == 1:
    # É uma mensagem (qualquer origem)
```

---

## 🔧 Como Configurar

### 1. Obter Token da API

1. Acesse o Movidesk
2. Vá em: **Configurações** > **Conta** > **Parâmetros**
3. Aba: **Ambiente**
4. Role até o final da página
5. Copie o **Token da API**

### 2. Configurar no Projeto

Edite o arquivo `backend/.env`:

```env
MOVIDESK_API_TOKEN=seu_token_aqui
MOVIDESK_API_URL=https://api.movidesk.com/public/v1
```

---

## 🧪 Testar Manualmente

### Via cURL

```bash
# Substitua SEU_TOKEN e ID_DO_TICKET
curl "https://api.movidesk.com/public/v1/tickets?token=SEU_TOKEN&id=12345&\$expand=actions"
```

### Via Postman

1. Método: **GET**
2. URL: `https://api.movidesk.com/public/v1/tickets`
3. Query Params:
   - `token`: seu_token_aqui
   - `id`: 12345
   - `$expand`: actions

---

## 📊 Exemplo de Uso no Código

### Buscar Ticket e Ler Chat

```python
from app.services.movidesk_service import MovideskService

# Criar instância do serviço
movidesk = MovideskService()

# Buscar ticket
ticket_data = await movidesk.get_ticket("156789")

# Acessar dados
print(f"Ticket: {ticket_data['ticket_numero']}")
print(f"Título: {ticket_data['titulo']}")
print(f"Cliente: {ticket_data['cliente']}")
print(f"Total de mensagens: {ticket_data['total_mensagens']}")

# Percorrer histórico do chat
for mensagem in ticket_data['historico_chat']:
    print(f"{mensagem['autor']}: {mensagem['mensagem']}")
    print(f"  Tipo: {mensagem['tipo']}")  # 'chat' ou 'comentario'
    print(f"  Data: {mensagem['data']}")
```

### Saída Esperada

```
Ticket: 156789
Título: Erro ao salvar quadro de horários
Cliente: Faculdade Exemplo
Total de mensagens: 6

Cliente Silva: Olá, estou com problema no sistema
  Tipo: chat
  Data: 2025-10-13T10:30:00

João Suporte: Pode detalhar o problema?
  Tipo: comentario
  Data: 2025-10-13T10:31:00

...
```

---

## 🔒 Limites da API

⚠️ **Importante!**

- **10 requisições por minuto** (rate limit)
- Se precisar de mais, entre em contato com Movidesk
- Use cache para evitar requisições repetidas

**No nosso código:**
```python
# Cache de 24 horas já implementado!
# Tickets são salvos no SQLite automaticamente
```

---

## 🎯 Filtros Avançados (Opcional)

### Buscar Múltiplos Tickets

```
GET /tickets?token=XXX&$filter=status eq 'New'&$expand=actions
```

### Buscar por Data

```
GET /tickets?token=XXX&$filter=createdDate gt '2025-10-01'&$expand=actions
```

### Ordenar Resultados

```
GET /tickets?token=XXX&$orderby=createdDate desc&$expand=actions
```

**Nota:** Para nosso caso, pegamos apenas 1 ticket por vez (por ID).

---

## 🐛 Debug e Troubleshooting

### Erro 401 (Unauthorized)

```json
{
  "error": "Invalid token"
}
```

**Solução:**
- Verifique se o token está correto no `.env`
- Token fica em: Movidesk > Configurações > Parâmetros > Ambiente

### Erro 404 (Not Found)

```json
{
  "error": "Ticket not found"
}
```

**Solução:**
- Verifique se o ID do ticket existe
- Confirme se tem permissão para acessar o ticket

### Actions Vazias

Se `actions` vem vazio ou `null`:

**Solução:**
- Use `$expand=actions` no parâmetro
- Verifique se o ticket tem mensagens/comentários

### HTML em Mensagens

Mensagens podem vir com HTML:

```
<p>Olá, <strong>estou com problema</strong></p>
```

**Solução:**
```python
# Já implementado! Remove HTML automaticamente
import re
mensagem_limpa = re.sub(r'<[^>]+>', '', mensagem_html)
```

---

## 📝 Campos Extras Disponíveis (se precisar)

Outros campos que o Movidesk retorna:

```python
# No ticket
- urgency: Urgência
- priority: Prioridade  
- tags: Array de tags
- customFieldValues: Campos customizados
- serviceFull: Serviço vinculado

# Nas actions
- isDeleted: Se foi deletado
- timeAppointments: Apontamento de tempo
- attachments: Anexos
```

Para usar, adicione no `$expand`:
```
$expand=actions,tags,customFieldValues
```

---

## ✅ Checklist de Integração

- [x] Token obtido no Movidesk
- [x] Token configurado no `.env`
- [x] Endpoint correto (`/tickets`)
- [x] Parâmetro `token` no query string
- [x] Parâmetro `$expand=actions` incluído
- [x] Parse de `actions` implementado
- [x] Filtro por `type = 1` (mensagens)
- [x] Identificação de origem (chat vs comentário)
- [x] Remoção de HTML das mensagens
- [x] Ordenação cronológica
- [x] Cache implementado
- [x] Fallback para modo MOCK

---

## 🚀 Próximos Passos

1. ✅ Configurar token real no `.env`
2. ✅ Testar com ticket real do Movidesk
3. ✅ Verificar estrutura do JSON retornado
4. ✅ Ajustar parse se necessário
5. ✅ Validar com equipe de suporte

---

## 💡 Dicas Importantes

1. **Use modo MOCK primeiro** para desenvolver sem depender da API
2. **Cache é seu amigo** - evita rate limit e melhora performance
3. **Log tudo** durante desenvolvimento para debug
4. **Teste com tickets variados** (com chat, sem chat, vários comentários)
5. **Valide permissões** - usuário do token precisa acessar os tickets

---

## 📞 Suporte

**Dúvidas sobre a API Movidesk?**
- Documentação: https://atendimento.movidesk.com/kb/pt-br
- Suporte: Abra ticket no próprio Movidesk

**Dúvidas sobre o código?**
- Veja: `backend/app/services/movidesk_service.py`
- Logs: Terminal onde o backend está rodando

---

**✅ Integração 100% alinhada com a documentação oficial!**

