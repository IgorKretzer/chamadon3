#!/bin/bash

echo "╔════════════════════════════════════════════╗"
echo "║   🚀 DEPLOY IA CHAMADOS SPONTE - VERCEL   ║"
echo "╚════════════════════════════════════════════╝"
echo ""

echo "📦 Projeto preparado para deploy!"
echo ""
echo "✅ Checklist:"
echo "  [✓] Build criado (frontend/dist)"
echo "  [✓] Vercel CLI instalado"
echo "  [✓] Configurações prontas"
echo "  [✓] Seção empty state removida"
echo ""

echo "🔐 Passo 1: Login no Vercel"
echo "Execute: vercel login"
echo ""
echo "Isso vai:"
echo "  → Pedir seu email"
echo "  → Enviar email de confirmação"
echo "  → Autenticar sua conta"
echo ""

read -p "Pressione ENTER para fazer login no Vercel..." dummy
vercel login

echo ""
echo "🚀 Passo 2: Deploy do Projeto"
echo ""
echo "Configurações recomendadas:"
echo "  → Scope: igorkretzers-projects"
echo "  → Nome: ia-chamados-sponte"
echo "  → Diretório: ./frontend"
echo ""

read -p "Pressione ENTER para iniciar o deploy..." dummy
vercel --prod

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "🌐 Acesse:"
echo "  → Dashboard: https://vercel.com/igorkretzers-projects"
echo "  → Projeto: [URL será exibida acima]"
echo ""
