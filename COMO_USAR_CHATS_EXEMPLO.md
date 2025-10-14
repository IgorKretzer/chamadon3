# 🎯 Guia Rápido - Chats de Exemplo

## 📖 Resumo

Agora o sistema possui uma funcionalidade de **chats de exemplo** que permite testar a IA sem precisar acessar o Movidesk.

## 🚀 Como Usar em 3 Passos

### 1. Digite o número do ticket de exemplo

No campo de entrada do sistema, digite: `123456`

### 2. Clique em "Analisar Ticket"

O sistema automaticamente:
- ✅ Detecta que é um chat de exemplo
- ✅ Carrega o chat armazenado
- ✅ Analisa com a IA
- ✅ Gera o chamado formatado

### 3. Copie o resultado

O chamado será gerado no formato padrão:

```
VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
R = 

CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
R = 2938 e 68330

JUSTIFICATIVA DA URGÊNCIA:
R = Impossibilidade de processar arquivo de retorno...

MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
R = Financeiro > Processamento de Arquivo de Retorno > Banco Inter

BRIEFING:
R = Cliente reportou erro ao tentar processar arquivo de retorno...

EXEMPLOS (OBRIGATÓRIO):
R = Unidades afetadas: 2938 e 68330
Arquivo: ucn.ret
Banco: Inter...

OBS:
R = Cliente forneceu email gb_thiago@yahoo.com.br para retorno...
```

## 📁 Chat de Exemplo Disponível

### Ticket 123456

**Problema**: Erro ao processar arquivo de retorno do Banco Inter

**Detalhes**:
- Cliente: Teste
- Erro: "Conversion from string to type 'Double' is not valid"
- Bases afetadas: 2938 e 68330
- Banco: Inter
- Ticket relacionado: 1150208

**Chat completo**: 44 mensagens entre cliente e atendente Cirlene

## ➕ Como Adicionar Seus Próprios Chats

### Passo 1: Crie o arquivo JSON

Vá para: `backend/chats_exemplo/`

Crie um arquivo: `ticket_SEU_NUMERO.json`

### Passo 2: Use este template

```json
{
  "ticket_numero": "SEU_NUMERO",
  "cliente": "Teste",
  "titulo": "Descrição do problema",
  "data_abertura": "2025-10-14T10:00:00",
  "historico_chat": [
    {
      "autor": "Cliente",
      "mensagem": "Olá, estou com um problema..."
    },
    {
      "autor": "Atendente",
      "mensagem": "Pode me dar mais detalhes?"
    }
  ]
}
```

### Passo 3: Teste

Digite o número do seu ticket no sistema e veja a mágica acontecer! ✨

## 🧪 Testar via Terminal

```bash
cd backend
python3 test_chat_exemplo.py
```

Este script testa:
- ✅ Carregamento do chat
- ✅ Análise da IA
- ✅ Geração do chamado
- ✅ Validação do resultado

## 📚 Documentação Completa

Para mais detalhes, consulte:
- `CHATS_EXEMPLO.md` - Documentação completa
- `backend/chats_exemplo/README.md` - Detalhes técnicos
- `backend/chats_exemplo/ticket_123456.json` - Exemplo real

## 💡 Casos de Uso

✅ **Desenvolvimento**: Testar sem depender do Movidesk
✅ **Treinamento**: Mostrar exemplos para novos usuários
✅ **Demonstração**: Apresentar o sistema sem dados reais
✅ **Debug**: Reproduzir problemas específicos

## 🎓 Dicas

1. **Use cliente "Teste"** para identificar facilmente chats de exemplo
2. **Mantenha conversas realistas** para treinar melhor a IA
3. **Documente o resultado esperado** no campo `analise_esperada`
4. **Organize por tipo de problema** (financeiro, acadêmico, etc)

## ⚠️ Importante

- Os chats de exemplo **têm prioridade** sobre o Movidesk
- Se existir `ticket_123456.json`, ele será usado em vez de buscar no Movidesk
- Use números de ticket diferentes dos reais para evitar conflitos

## 🎯 Benefícios

- ⚡ **Testes rápidos** sem configurar API do Movidesk
- 🎓 **Treinamento eficiente** com casos reais
- 🔍 **Debug facilitado** de problemas específicos
- 📊 **Validação de qualidade** da IA

---

**Criado em**: Outubro 2025
**Ticket de exemplo**: 123456
**Status**: ✅ Funcionando

