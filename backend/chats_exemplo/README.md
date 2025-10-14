# Pasta de Chats de Exemplo

Esta pasta contém chats de exemplo que podem ser usados para testar e treinar a IA.

## Como funciona

Quando você buscar um ticket com o cliente "Teste", o sistema irá buscar primeiro nesta pasta antes de consultar o Movidesk.

## Formato do arquivo

Cada arquivo deve seguir o padrão: `ticket_NUMERO.json`

Exemplo: `ticket_123456.json`

## Estrutura do JSON

```json
{
  "ticket_numero": "123456",
  "cliente": "Teste",
  "titulo": "Título do ticket",
  "data_abertura": "2025-10-10T16:10:00",
  "chat_completo": "Chat completo em texto...",
  "historico_chat": [
    {
      "autor": "Nome do autor",
      "mensagem": "Mensagem"
    }
  ],
  "analise_esperada": {
    "versao_sistema": "12.0.1",
    "codigo_base": "60714",
    "justificativa_urgencia": "Descrição da urgência",
    "menu_local": "Menu > Submenu",
    "briefing": "Descrição do problema",
    "exemplos": "Exemplos e casos afetados",
    "obs": "Observações adicionais"
  }
}
```

## Template de Chamado

A IA deve converter o chat no seguinte formato:

```
VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
R = [versão]

CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
R = [código]

JUSTIFICATIVA DA URGÊNCIA:
R = [justificativa]

MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
R = [menu/local]

BRIEFING:
R = [descrição detalhada do problema]

EXEMPLOS (OBRIGATÓRIO):
R = [exemplos específicos]

OBS:
R = [observações]
```

## Como adicionar novos chats de exemplo

1. Crie um novo arquivo JSON seguindo o padrão `ticket_NUMERO.json`
2. Preencha todos os campos obrigatórios
3. Opcionalmente, adicione a seção `analise_esperada` com o resultado esperado da análise
4. O sistema carregará automaticamente o novo chat quando o ticket for buscado

## Tickets disponíveis

- `123456` - Erro ao processar arquivo de retorno - Banco Inter
- `1234567` - Cadastro grupo split não permanece salvo ao trocar unidade

