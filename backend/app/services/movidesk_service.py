import httpx
import os
from typing import Dict, Any, Optional

class MovideskService:
    def __init__(self):
        self.api_token = os.getenv("MOVIDESK_API_TOKEN", "")
        self.api_url = os.getenv("MOVIDESK_API_URL", "https://api.movidesk.com/public/v1")
        
    async def get_ticket(self, ticket_numero: str) -> Dict[str, Any]:
        """
        Busca informações de um ticket no Movidesk via API oficial
        
        Endpoint: GET /tickets?token=XXX&id=ID&$expand=actions
        Documentação: https://atendimento.movidesk.com/kb/pt-br/article/256/movidesk-ticket-api
        
        Args:
            ticket_numero: Número/ID do ticket (ex: "156789")
            
        Returns:
            Dicionário com dados do ticket e histórico de chat
        """
        
        # Se não tiver token configurado, retorna dados mockados para demonstração
        if not self.api_token or self.api_token == "seu_token_aqui":
            return self._get_mock_ticket(ticket_numero)
        
        try:
            async with httpx.AsyncClient() as client:
                # Endpoint oficial do Movidesk
                url = f"{self.api_url}/tickets"
                
                # Movidesk usa token como query param, não Bearer header
                params = {
                    "token": self.api_token,
                    "id": ticket_numero,
                    "$expand": "actions"  # Expande as ações/mensagens do ticket
                }
                
                # Headers simples
                headers = {
                    "Content-Type": "application/json"
                }
                
                print(f"🔍 Buscando ticket {ticket_numero} no Movidesk...")
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Ticket {ticket_numero} obtido com sucesso!")
                    return self._parse_ticket_data(data)
                else:
                    # Se falhar, retorna mock
                    print(f"❌ Erro ao buscar ticket: HTTP {response.status_code}")
                    print(f"Resposta: {response.text[:200]}")
                    return self._get_mock_ticket(ticket_numero)
                    
        except Exception as e:
            print(f"❌ Erro na chamada Movidesk: {str(e)}")
            return self._get_mock_ticket(ticket_numero)
    
    def _parse_ticket_data(self, data: Dict) -> Dict[str, Any]:
        """
        Parse dos dados retornados pela API do Movidesk
        
        Estrutura do JSON retornado:
        - id: ID do ticket
        - subject: Assunto/título
        - client: { businessName, email, ... }
        - owner: { businessName, ... } - Agente responsável
        - createdDate: Data de criação
        - actions: [
            {
              type: 1 (mensagem), 2 (email), etc
              origin: 1 (email), 2 (manual), 5 (chat online), 6 (chat offline), etc
              description: Texto puro da mensagem
              htmlDescription: HTML da mensagem
              createdBy: { businessName, ... }
              createdDate: Data da ação
            }
          ]
        """
        
        # Extrair ações/mensagens do ticket (histórico de chat/conversas)
        historico = []
        
        if 'actions' in data and data['actions']:
            for action in data['actions']:
                # Filtros para pegar mensagens relevantes:
                # type == 1: Mensagem/comentário
                # Pode filtrar por origin se quiser apenas chats:
                #   origin == 5: Chat online
                #   origin == 6: Chat offline
                
                action_type = action.get('type')
                action_origin = action.get('origin')
                
                # Pega todas as mensagens (type = 1)
                # Se quiser APENAS chats, descomente a linha abaixo:
                # if action_type == 1 and action_origin in [5, 6]:
                
                if action_type == 1:  # Mensagens
                    # Usa htmlDescription se disponível, senão description
                    mensagem = action.get('htmlDescription') or action.get('description', '')
                    
                    # Remove HTML tags se necessário (básico)
                    import re
                    mensagem_limpa = re.sub(r'<[^>]+>', '', mensagem) if '<' in mensagem else mensagem
                    
                    historico.append({
                        'autor': action.get('createdBy', {}).get('businessName', 'Cliente'),
                        'mensagem': mensagem_limpa.strip(),
                        'mensagem_html': mensagem,  # Mantém HTML original também
                        'data': action.get('createdDate', ''),
                        'tipo': 'chat' if action_origin in [5, 6] else 'comentario',
                        'origin': action_origin
                    })
        
        # Ordena por data (mais antigas primeiro - ordem cronológica)
        historico.sort(key=lambda x: x.get('data', ''))
        
        return {
            'ticket_numero': str(data.get('id', '')),
            'titulo': data.get('subject', ''),
            'cliente': data.get('client', {}).get('businessName', '') if data.get('client') else '',
            'cliente_email': data.get('client', {}).get('email', '') if data.get('client') else '',
            'responsavel': data.get('owner', {}).get('businessName', '') if data.get('owner') else '',
            'data_abertura': data.get('createdDate', ''),
            'status': data.get('status', ''),
            'categoria': data.get('category', ''),
            'historico_chat': historico,
            'total_mensagens': len(historico)
        }
    
    def _get_mock_ticket(self, ticket_numero: str) -> Dict[str, Any]:
        """Retorna dados mockados para demonstração"""
        return {
            'ticket_numero': ticket_numero,
            'titulo': 'Erro ao salvar quadro de horários',
            'cliente': 'Faculdade Exemplo',
            'responsavel': 'Suporte N3',
            'data_abertura': '2025-10-13T10:30:00',
            'historico_chat': [
                {
                    'autor': 'Cliente',
                    'mensagem': 'Olá, estou tendo problema no sistema',
                    'data': '2025-10-13T10:30:00'
                },
                {
                    'autor': 'Suporte',
                    'mensagem': 'Olá! Pode me dar mais detalhes do problema?',
                    'data': '2025-10-13T10:31:00'
                },
                {
                    'autor': 'Cliente',
                    'mensagem': 'Quando vou no menu Acadêmico e tento salvar o quadro de horários da turma ADS 3º Semestre, aparece um erro',
                    'data': '2025-10-13T10:32:00'
                },
                {
                    'autor': 'Suporte',
                    'mensagem': 'Qual erro aparece?',
                    'data': '2025-10-13T10:32:30'
                },
                {
                    'autor': 'Cliente',
                    'mensagem': 'Aparece: "Constraint violation on table TB_HORARIOS: duplicate key value violates unique constraint"',
                    'data': '2025-10-13T10:33:00'
                },
                {
                    'autor': 'Suporte',
                    'mensagem': 'Entendi. Vou abrir um chamado para o desenvolvimento resolver isso.',
                    'data': '2025-10-13T10:34:00'
                }
            ]
        }

