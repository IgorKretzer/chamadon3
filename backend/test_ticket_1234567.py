#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o ticket 1234567 - Grupo Split
"""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório do app ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.movidesk_service import MovideskService
from app.services.ia_service import IAService


async def testar_ticket_1234567():
    """Testa o ticket 1234567 - Grupo Split"""
    
    print("=" * 80)
    print("🧪 TESTE DO TICKET 1234567 - GRUPO SPLIT")
    print("=" * 80)
    print()
    
    # Inicializa serviços
    movidesk = MovideskService()
    ia = IAService()
    
    ticket_numero = "1234567"
    
    print(f"📋 Testando ticket: {ticket_numero}")
    print()
    
    # 1. Busca o ticket
    print("1️⃣ Buscando ticket...")
    dados_ticket = await movidesk.get_ticket(ticket_numero)
    
    if dados_ticket.get('fonte') == 'chat_exemplo':
        print("   ✅ Chat de exemplo carregado com sucesso!")
    else:
        print("   ⚠️  Chat de exemplo NÃO foi carregado")
        return False
    
    print()
    print(f"   Cliente: {dados_ticket.get('cliente')}")
    print(f"   Título: {dados_ticket.get('titulo')}")
    print(f"   Mensagens: {len(dados_ticket.get('historico_chat', []))}")
    print()
    
    # 2. Analisa com IA
    print("2️⃣ Analisando com IA...")
    resultado = await ia.analisar_ticket(dados_ticket)
    
    print()
    print(f"   Tipo: {resultado.get('tipo')}")
    print(f"   Módulo: {resultado.get('modulo')}")
    print()
    
    # 3. Exibe o chamado gerado
    print("3️⃣ Chamado Gerado:")
    print("=" * 80)
    print(resultado.get('chamado_texto'))
    print("=" * 80)
    print()
    
    # 4. Valida contra análise esperada
    if 'analise_esperada' in dados_ticket:
        print("4️⃣ Validando contra resultado esperado...")
        esperado = dados_ticket['analise_esperada']
        
        chamado = resultado.get('chamado_texto', '').lower()
        
        validacoes = {
            'Unidade 73955 mencionada': '73955' in chamado,
            'Grupo split mencionado': 'split' in chamado,
            'Problema de compartilhamento mencionado': 'compartilha' in chamado or 'compartilh' in chamado,
            'PIX mencionado': 'pix' in chamado,
            'Email de contato incluído': 'ppnipapelaria' in chamado or '@gmail.com' in chamado,
        }
        
        print()
        for item, passou in validacoes.items():
            icone = "✅" if passou else "❌"
            print(f"   {icone} {item}")
        
        print()
        
        total = len(validacoes)
        passou = sum(1 for v in validacoes.values() if v)
        percentual = (passou / total) * 100
        
        print(f"📊 Score: {passou}/{total} ({percentual:.0f}%)")
        print()
        
        # Verifica módulo
        print("5️⃣ Validação de Módulo:")
        modulo_esperado = "Financeiro"
        modulo_recebido = resultado.get('modulo', '')
        
        if modulo_recebido == modulo_esperado:
            print(f"   ✅ Módulo correto: {modulo_recebido}")
        else:
            print(f"   ⚠️  Módulo: {modulo_recebido} (esperado: {modulo_esperado})")
        print()
    
    # Resumo
    print("=" * 80)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 80)
    print()
    print("📝 Detalhes do caso:")
    print("   • Problema: Grupo split não salva ao trocar unidade")
    print("   • Causa: Categoria compartilhada entre unidades")
    print("   • Solução: Descompartilhar categoria")
    print("   • Módulo esperado: Financeiro")
    print()
    print("🧪 Para testar no frontend:")
    print("   Digite: 1234567")
    print()
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(testar_ticket_1234567())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

