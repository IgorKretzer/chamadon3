# 📁 Chats de Exemplo - Guia de Uso

Este documento explica como usar o sistema de chats de exemplo para testar e treinar a IA.

## 📋 O que são Chats de Exemplo?

Chats de exemplo são conversas reais de atendimento armazenadas em arquivos JSON que o sistema pode usar para:

- **Testes**: Validar o funcionamento da IA sem precisar de acesso ao Movidesk
- **Treinamento**: Fornecer exemplos de como a IA deve analisar diferentes tipos de problemas
- **Demonstração**: Mostrar o sistema funcionando com dados reais

## 🗂️ Localização

Os chats de exemplo ficam armazenados em:

```
backend/chats_exemplo/
```

## 📝 Como Funciona

1. Quando você busca um ticket pelo número (ex: `123456`)
2. O sistema **primeiro verifica** se existe um arquivo `ticket_123456.json` na pasta `chats_exemplo`
3. Se existir, usa esse chat de exemplo
4. Se não existir, busca no Movidesk normalmente

## 🎯 Como Usar

### Testar com Chat de Exemplo

1. Abra o sistema normalmente
2. Digite o número do ticket de exemplo: `123456`
3. O sistema carregará automaticamente o chat armazenado
4. A IA analisará e gerará o chamado no formato correto

### Adicionar Novo Chat de Exemplo

1. Vá para a pasta: `backend/chats_exemplo/`
2. Crie um arquivo: `ticket_NUMERO.json` (ex: `ticket_789012.json`)
3. Use a estrutura abaixo:

```json
{
  "ticket_numero": "789012",
  "cliente": "Teste",
  "titulo": "Descrição breve do problema",
  "data_abertura": "2025-10-14T10:00:00",
  "historico_chat": [
    {
      "autor": "Nome do Autor",
      "mensagem": "Texto da mensagem"
    },
    {
      "autor": "Outro Autor",
      "mensagem": "Outra mensagem"
    }
  ],
  "analise_esperada": {
    "versao_sistema": "12.0.1",
    "codigo_base": "60714",
    "justificativa_urgencia": "Descrição do impacto",
    "menu_local": "Menu > Submenu > Tela",
    "briefing": "Descrição detalhada",
    "exemplos": "Dados específicos",
    "obs": "Observações adicionais"
  }
}
```

## 📊 Chats Disponíveis

### Ticket 123456 - Erro ao processar arquivo de retorno - Banco Inter

**Descrição**: Cliente com erro ao processar arquivo de retorno do Banco Inter. Problema de conversão de string para double e erro na leitura de posições do arquivo.

**Como testar**:
1. Digite `123456` no campo de ticket
2. Clique em "Analisar Ticket"
3. Veja a análise completa do problema

**Resultado esperado**:
- Versão: Não mencionada no chat
- Base: 2938 e 68330
- Módulo: Financeiro
- Local: Financeiro > Processamento de Arquivo de Retorno > Banco Inter
- Erro principal: Conversion from string to type 'Double' is not valid

## 🎓 Template do Chamado

A IA deve gerar o chamado neste formato:

```
VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
R = [versão do sistema]

CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
R = [código da base/unidade]

JUSTIFICATIVA DA URGÊNCIA:
R = [descrição do impacto e urgência]

MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
R = [caminho completo do menu]

BRIEFING:
R = [descrição detalhada do problema]

EXEMPLOS (OBRIGATÓRIO):
R = [dados específicos afetados]

OBS:
R = [informações adicionais]
```

## 🔍 Dicas para Criar Bons Chats de Exemplo

### ✅ BOM - Chat Completo
```json
{
  "historico_chat": [
    {
      "autor": "Cliente",
      "mensagem": "Estou com erro ao gerar boleto. Aparece: Banco não configurado"
    },
    {
      "autor": "Atendente",
      "mensagem": "Em qual unidade está acontecendo?"
    },
    {
      "autor": "Cliente",
      "mensagem": "Unidade 12345, no menu Financeiro > Emissão de Boletos"
    }
  ]
}
```

### ❌ RUIM - Chat Incompleto
```json
{
  "historico_chat": [
    {
      "autor": "Cliente",
      "mensagem": "Deu erro"
    }
  ]
}
```

## 📌 Campos Importantes

### historico_chat (Obrigatório)
Array com as mensagens da conversa. Cada mensagem deve ter:
- `autor`: Nome de quem escreveu
- `mensagem`: Texto da mensagem

### analise_esperada (Opcional)
Use para documentar o resultado esperado. Útil para:
- Validar se a IA está analisando corretamente
- Treinar novos modelos
- Documentar casos de uso

## 🚀 Próximos Passos

1. **Teste o chat de exemplo existente** (ticket 123456)
2. **Crie seus próprios chats** baseados em tickets reais
3. **Valide os resultados** comparando com `analise_esperada`
4. **Ajuste o prompt da IA** se necessário

## 💡 Casos de Uso

### Desenvolvimento
- Testar novas funcionalidades sem depender do Movidesk
- Validar mudanças no prompt da IA
- Debug de problemas específicos

### Treinamento
- Mostrar exemplos para novos usuários
- Documentar casos de sucesso
- Criar biblioteca de problemas conhecidos

### Demonstração
- Apresentar o sistema para stakeholders
- Fazer demos sem dados reais de produção
- Mostrar diferentes tipos de análise

## ⚙️ Configuração Técnica

O sistema automaticamente:

1. Verifica a pasta `backend/chats_exemplo/` ao buscar um ticket
2. Carrega o arquivo JSON se existir
3. Converte para o formato esperado pela IA
4. Marca a fonte como `"fonte": "chat_exemplo"`

Nenhuma configuração adicional é necessária!

## 📞 Dúvidas?

Se tiver dúvidas sobre:
- **Estrutura do JSON**: Consulte `backend/chats_exemplo/README.md`
- **Como a IA analisa**: Consulte `backend/app/services/ia_service.py`
- **Formato do Movidesk**: Consulte `backend/app/services/movidesk_service.py`

---

**Última atualização**: Outubro 2025

