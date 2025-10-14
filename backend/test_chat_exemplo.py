#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar os chats de exemplo
"""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório do app ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.movidesk_service import MovideskService
from app.services.ia_service import IAService


async def testar_chat_exemplo():
    """Testa o carregamento e análise de um chat de exemplo"""
    
    print("=" * 80)
    print("🧪 TESTE DE CHAT DE EXEMPLO")
    print("=" * 80)
    print()
    
    # Inicializa serviços
    movidesk = MovideskService()
    ia = IAService()
    
    # Testa ticket de exemplo
    ticket_numero = "123456"
    
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
    
    # 4. Valida contra análise esperada (se disponível)
    if 'analise_esperada' in dados_ticket:
        print("4️⃣ Validando contra resultado esperado...")
        esperado = dados_ticket['analise_esperada']
        
        chamado = resultado.get('chamado_texto', '')
        
        validacoes = {
            'Código da base mencionado': esperado.get('codigo_base', '') in chamado,
            'Menu/Local mencionado': any(palavra in chamado for palavra in esperado.get('menu_local', '').split('>')),
            'Banco Inter mencionado': 'Inter' in chamado or 'inter' in chamado.lower(),
            'Erro de conversão mencionado': 'convers' in chamado.lower() or 'double' in chamado.lower(),
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
    
    # Resumo
    print("=" * 80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print()
    print("📝 Próximos passos:")
    print("   1. Teste no frontend digitando o ticket: 123456")
    print("   2. Crie novos chats de exemplo na pasta: backend/chats_exemplo/")
    print("   3. Ajuste o prompt da IA se necessário")
    print()
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(testar_chat_exemplo())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

