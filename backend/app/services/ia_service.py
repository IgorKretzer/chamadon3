import google.generativeai as genai
import os
from typing import Dict, Any
import json
import re

class IAService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        
        if api_key and api_key != "sua_chave_aqui":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.mock_mode = False
        else:
            self.mock_mode = True
            print("⚠️  Gemini API não configurada - usando modo MOCK para demonstração")
    
    async def analisar_ticket(self, dados_ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa o ticket e gera sugestão de chamado
        
        Args:
            dados_ticket: Dados do ticket do Movidesk
            
        Returns:
            Dicionário com tipo, módulo, texto do chamado e metadata
        """
        
        if self.mock_mode:
            return self._gerar_resposta_mock(dados_ticket)
        
        # Monta o prompt para a IA
        prompt = self._montar_prompt(dados_ticket)
        
        try:
            # Chama a IA
            response = self.model.generate_content(prompt)
            
            # Parse da resposta
            resultado = self._parse_resposta_ia(response.text)
            
            # Adiciona contagem de tokens
            resultado['tokens'] = response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao chamar IA: {str(e)}")
            return self._gerar_resposta_mock(dados_ticket)
    
    def _montar_prompt(self, dados_ticket: Dict[str, Any]) -> str:
        """Monta o prompt estruturado para a IA"""
        
        # Formata o histórico do chat
        historico_formatado = ""
        for msg in dados_ticket.get('historico_chat', []):
            historico_formatado += f"{msg['autor']}: {msg['mensagem']}\n"
        
        prompt = f"""
Você é um assistente especializado em criar chamados técnicos para o sistema SPONTE 
com base em tickets de suporte.

=== BASE DE CONHECIMENTO DO SISTEMA SPONTE ===

MÓDULOS DO SISTEMA:
- ACADÊMICO: Gestão de turmas, matrizes curriculares, quadro de horários, diário de classe, notas e frequências
- FINANCEIRO: Emissão de boletos, controle de inadimplência, renegociação, descontos
- SECRETARIA: Cadastro de alunos, matrículas, documentos, histórico escolar
- PORTAL DO ALUNO: Acesso do aluno a notas, faltas, boletos, documentos
- BIBLIOTECA: Controle de acervo, empréstimos, reservas

ERROS COMUNS:
- "Constraint violation" → Problema de dados duplicados ou regras de integridade do banco
- "Banco não configurado" → Problema na configuração de convênio bancário
- "Acesso negado" → Problema de permissões ou perfil de usuário
- "Timeout" → Problema de performance ou processamento pesado

=== TICKET #{dados_ticket.get('ticket_numero')} ===

TÍTULO: {dados_ticket.get('titulo', '')}
CLIENTE: {dados_ticket.get('cliente', '')}

HISTÓRICO DA CONVERSA:
{historico_formatado}

=== SUA TAREFA ===

1. Analise se este ticket reporta uma INCONSISTÊNCIA/BUG no sistema Sponte
2. Se SIM, extraia:
   - Módulo afetado
   - Tela/Menu específico
   - Ação que causou o erro
   - Mensagem de erro exata
   - Impacto (quantos usuários/registros)

3. Retorne APENAS um JSON válido no seguinte formato:

{{
  "tipo": "inconsistencia" ou "duvida" ou "outro",
  "modulo": "nome do módulo",
  "chamado_texto": "texto completo formatado do chamado",
  "metadata": {{
    "tela": "nome da tela",
    "acao": "ação realizada",
    "erro": "mensagem de erro",
    "impacto": "descrição do impacto"
  }}
}}

O campo "chamado_texto" deve seguir este formato:

TÍTULO: [Resumo em 1 linha]

MÓDULO: [Nome do módulo]

DESCRIÇÃO:
[Descrição clara do problema]

PASSOS PARA REPRODUZIR:
1. [Passo 1]
2. [Passo 2]
3. [Erro acontece aqui]

ERRO:
[Mensagem de erro exata se houver]

IMPACTO:
[Quantos afetados / urgência]

Se NÃO for inconsistência, retorne:
{{
  "tipo": "outro",
  "modulo": null,
  "chamado_texto": "Este ticket não parece reportar uma inconsistência do sistema Sponte.",
  "metadata": null
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional antes ou depois.
"""
        return prompt
    
    def _parse_resposta_ia(self, resposta: str) -> Dict[str, Any]:
        """Parse da resposta da IA"""
        try:
            # Remove markdown se houver
            resposta_limpa = resposta.strip()
            if resposta_limpa.startswith('```json'):
                resposta_limpa = resposta_limpa[7:]
            if resposta_limpa.startswith('```'):
                resposta_limpa = resposta_limpa[3:]
            if resposta_limpa.endswith('```'):
                resposta_limpa = resposta_limpa[:-3]
            
            resposta_limpa = resposta_limpa.strip()
            
            # Parse JSON
            resultado = json.loads(resposta_limpa)
            
            return {
                'tipo': resultado.get('tipo', 'outro'),
                'modulo': resultado.get('modulo'),
                'chamado_texto': resultado.get('chamado_texto', ''),
                'metadata': resultado.get('metadata'),
                'tokens': 0
            }
            
        except Exception as e:
            print(f"Erro ao fazer parse da resposta: {str(e)}")
            print(f"Resposta recebida: {resposta[:200]}...")
            
            # Fallback: tenta extrair informações da resposta
            return {
                'tipo': 'outro',
                'modulo': None,
                'chamado_texto': 'Erro ao processar resposta da IA. Por favor, tente novamente.',
                'metadata': None,
                'tokens': 0
            }
    
    def _gerar_resposta_mock(self, dados_ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Gera resposta mockada para demonstração"""
        
        chamado_texto = f"""TÍTULO: Erro ao salvar Quadro de Horários - Constraint violation

MÓDULO: Acadêmico

DESCRIÇÃO:
Ao acessar o menu Acadêmico > Quadro de Horários e tentar salvar as alterações da turma "ADS 3º Semestre", o sistema retorna erro de violação de constraint no banco de dados.

PASSOS PARA REPRODUZIR:
1. Acessar menu Acadêmico
2. Clicar em Quadro de Horários
3. Selecionar turma "ADS 3º Semestre"
4. Fazer alteração em qualquer horário
5. Clicar em "Salvar"
6. Sistema exibe erro

ERRO:
"Constraint violation on table TB_HORARIOS: duplicate key value violates unique constraint"

IMPACTO:
Coordenação acadêmica impossibilitada de ajustar quadro de horários.
Problema identificado em pelo menos 1 turma, pode afetar outras.
Urgência: ALTA - Início do semestre letivo próximo.

INFORMAÇÕES ADICIONAIS:
- Cliente: {dados_ticket.get('cliente', 'N/A')}
- Ticket: #{dados_ticket.get('ticket_numero', 'N/A')}
- Data do reporte: {dados_ticket.get('data_abertura', 'N/A')}
"""
        
        return {
            'tipo': 'inconsistencia',
            'modulo': 'Acadêmico',
            'chamado_texto': chamado_texto,
            'metadata': {
                'tela': 'Quadro de Horários',
                'acao': 'Salvar',
                'erro': 'Constraint violation on table TB_HORARIOS',
                'impacto': 'Coordenação bloqueada'
            },
            'tokens': 0
        }

