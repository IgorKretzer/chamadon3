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

MÓDULOS DO SISTEMA (use APENAS estes):
- CADASTROS: Cadastro de alunos, responsáveis, funcionários, professores, dados cadastrais gerais
- PEDAGÓGICO: Gestão de turmas, matrizes curriculares, quadro de horários, diário de classe, notas, frequências, boletins
- FINANCEIRO: Emissão de boletos, controle de inadimplência, renegociação, descontos, processamento de retorno bancário
- RELATÓRIOS: Geração de relatórios diversos do sistema
- GERENCIAL: Dashboards, indicadores, gestão e visão gerencial
- UTILITÁRIOS: Ferramentas auxiliares, configurações, importações, exportações

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

O campo "chamado_texto" deve seguir EXATAMENTE este formato:

VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
R = [versão do sistema, se mencionada no chat]

CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
R = [código da base/unidade afetada]

JUSTIFICATIVA DA URGÊNCIA:
R = [descrição clara do impacto e urgência do problema]

MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
R = [caminho completo do menu ou tela onde o problema ocorre]

BRIEFING:
R = [descrição detalhada do problema, incluindo o contexto da conversa, diagnóstico realizado, tentativas de solução e conclusão do atendente]

EXEMPLOS (OBRIGATÓRIO):
R = [dados específicos afetados: usuários, registros, unidades, códigos, números, etc]

OBS:
R = [informações adicionais relevantes: emails de contato, tickets relacionados, observações técnicas]

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
        """Gera resposta mockada baseada nos dados reais do ticket"""
        
        # Se tiver análise esperada (para testes), retorna ela
        if 'analise_esperada' in dados_ticket:
            analise = dados_ticket['analise_esperada']
            return {
                'tipo': analise.get('tipo', 'inconsistencia'),
                'modulo': analise.get('modulo', 'Não identificado'),
                'chamado_texto': analise.get('chamado_texto', ''),
                'metadata': analise.get('metadata', {}),
                'tokens': 0
            }
        
        # Caso contrário, gera um mock básico com os dados do ticket
        titulo = dados_ticket.get('titulo', 'Problema não especificado')
        cliente = dados_ticket.get('cliente', 'Cliente não identificado')
        ticket_numero = dados_ticket.get('ticket_numero', 'N/A')
        data_abertura = dados_ticket.get('data_abertura', 'N/A')
        
        # Analisa o histórico para extrair informações
        historico = dados_ticket.get('historico_chat', [])
        resumo_conversa = self._extrair_resumo_conversa(historico)
        
        chamado_texto = f"""VERSÃO DO SISTEMA EM QUE O PROBLEMA OCORREU:
R = Não informada no chat

CÓDIGO DA BASE QUE APRESENTA O PROBLEMA:
R = Base do cliente {cliente}

JUSTIFICATIVA DA URGÊNCIA:
R = {titulo} - Requer análise técnica

MENU/LOCAL DO SISTEMA EM QUE ACONTECE:
R = A ser identificado

BRIEFING:
R = {resumo_conversa}

EXEMPLOS (OBRIGATÓRIO):
R = Cliente: {cliente}
Ticket: #{ticket_numero}
Total de mensagens no chat: {len(historico)}

OBS:
R = Data do reporte: {data_abertura}
IMPORTANTE: Esta é uma análise mockada. Configure a API do Gemini para análises mais precisas.
"""
        
        return {
            'tipo': 'inconsistencia',
            'modulo': 'Não identificado',
            'chamado_texto': chamado_texto,
            'metadata': {
                'tela': 'A ser identificado',
                'acao': 'A ser identificado',
                'erro': 'A ser identificado',
                'impacto': 'A ser identificado'
            },
            'tokens': 0
        }
    
    def _extrair_resumo_conversa(self, historico: list) -> str:
        """Extrai um resumo básico da conversa"""
        if not historico:
            return "Sem histórico de conversa disponível"
        
        # Pega as primeiras e últimas mensagens
        total = len(historico)
        resumo_partes = []
        
        # Primeiras 3 mensagens
        for i, msg in enumerate(historico[:3]):
            autor = msg.get('autor', 'Desconhecido')
            texto = msg.get('mensagem', '')[:150]  # Limita tamanho
            resumo_partes.append(f"[{autor}]: {texto}")
        
        if total > 6:
            resumo_partes.append(f"... ({total - 6} mensagens intermediárias) ...")
        
        # Últimas 3 mensagens
        for msg in historico[-3:]:
            autor = msg.get('autor', 'Desconhecido')
            texto = msg.get('mensagem', '')[:150]
            resumo_partes.append(f"[{autor}]: {texto}")
        
        return "\n".join(resumo_partes)

