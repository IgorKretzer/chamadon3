# 📚 Módulos Oficiais do Sistema SPONTE

## 🎯 Lista Oficial de Módulos

O sistema SPONTE possui **6 módulos principais**. A IA deve usar APENAS estes módulos ao analisar tickets:

### 1. 📝 CADASTROS
**Descrição**: Cadastro de alunos, responsáveis, funcionários, professores, dados cadastrais gerais

**Telas/Funcionalidades**:
- Cadastro de alunos
- Cadastro de responsáveis financeiros
- Cadastro de funcionários
- Cadastro de professores
- Dados cadastrais gerais
- Importação de cadastros

---

### 2. 🎓 PEDAGÓGICO
**Descrição**: Gestão de turmas, matrizes curriculares, quadro de horários, diário de classe, notas, frequências, boletins

**Telas/Funcionalidades**:
- Gestão de turmas
- Matrizes curriculares
- Quadro de horários
- Diário de classe
- Lançamento de notas
- Lançamento de frequências
- Geração de boletins
- Conceitos e avaliações

---

### 3. 💰 FINANCEIRO
**Descrição**: Emissão de boletos, controle de inadimplência, renegociação, descontos, processamento de retorno bancário

**Telas/Funcionalidades**:
- Emissão de boletos
- Segunda via de boletos
- Controle de inadimplência
- Renegociação de dívidas
- Aplicação de descontos
- Processamento de arquivo de retorno bancário
- Conciliação bancária
- Convênios bancários
- Configuração de layouts de remessa/retorno

---

### 4. 📊 RELATÓRIOS
**Descrição**: Geração de relatórios diversos do sistema

**Telas/Funcionalidades**:
- Relatórios acadêmicos
- Relatórios financeiros
- Relatórios de cadastro
- Relatórios personalizados
- Exportação de dados

---

### 5. 📈 GERENCIAL
**Descrição**: Dashboards, indicadores, gestão e visão gerencial

**Telas/Funcionalidades**:
- Dashboards gerenciais
- Indicadores de desempenho
- Análises estratégicas
- Visão executiva
- Métricas e KPIs

---

### 6. 🔧 UTILITÁRIOS
**Descrição**: Ferramentas auxiliares, configurações, importações, exportações

**Telas/Funcionalidades**:
- Configurações do sistema
- Importação de dados
- Exportação de dados
- Ferramentas de manutenção
- Backup e restore
- Logs do sistema
- Parametrizações

---

## ⚠️ IMPORTANTE

A IA deve usar **APENAS** estes 6 módulos ao classificar tickets. Não criar ou usar outros nomes de módulos.

### ❌ Módulos que NÃO devem ser usados:
- ~~Acadêmico~~ → Use **Pedagógico**
- ~~Secretaria~~ → Use **Cadastros**
- ~~Portal do Aluno~~ → Use o módulo correspondente ao problema (geralmente **Financeiro** para boletos ou **Pedagógico** para notas)
- ~~Biblioteca~~ → Use **Utilitários** ou **Cadastros**
- ~~Administrativo~~ → Use **Gerencial** ou **Utilitários**

---

## 🎯 Como a IA deve Classificar

### Exemplos de Classificação:

| Problema | Módulo Correto | Justificativa |
|----------|----------------|---------------|
| Erro ao salvar dados do aluno | **Cadastros** | Relacionado a cadastro de alunos |
| Erro ao lançar notas | **Pedagógico** | Relacionado ao processo pedagógico |
| Boleto não está sendo gerado | **Financeiro** | Relacionado a processos financeiros |
| Relatório de inadimplência não abre | **Relatórios** | Problema com geração de relatório |
| Dashboard não carrega dados | **Gerencial** | Problema em visualização gerencial |
| Erro ao importar planilha | **Utilitários** | Ferramentas auxiliares do sistema |

---

## 📝 Atualização

**Última atualização**: Outubro 2025  
**Versão**: 1.0  
**Status**: ✅ Documentação oficial

---

## 🔄 Histórico de Mudanças

### v1.0 - Outubro 2025
- ✅ Definição dos 6 módulos oficiais
- ✅ Lista de funcionalidades de cada módulo
- ✅ Exemplos de classificação
- ✅ Lista de módulos obsoletos

---

**Nota**: Esta é a documentação oficial dos módulos do SPONTE. Qualquer dúvida sobre classificação deve consultar este arquivo.

