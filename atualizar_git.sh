#!/bin/bash
# Script para atualizar o repositório Git com os arquivos da Etapa 3

echo "=== Atualizando Repositório Git - Etapa 3 ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "docs/projeto_etapa3.tex" ]; then
    echo "❌ Erro: Execute este script a partir da raiz do projeto"
    exit 1
fi

# Verificar status do Git
echo "📊 Status atual do Git:"
git status --short | head -20
echo ""

# Adicionar arquivos importantes
echo "📦 Adicionando arquivos da Etapa 3..."

# Código Python novo
echo "  ✓ Código Python..."
git add src/storytelling_viz.py 2>/dev/null
[ -f "src/cleaning.py" ] && git add src/cleaning.py 2>/dev/null
[ -f "src/io_utils.py" ] && git add src/io_utils.py 2>/dev/null
[ -f "src/plotting.py" ] && git add src/plotting.py 2>/dev/null

# Documentação LaTeX
echo "  ✓ Documentação LaTeX..."
git add docs/projeto_etapa3.tex
[ -f "docs/compilar.sh" ] && git add docs/compilar.sh
[ -f "docs/INSTRUCOES_COMPILACAO.md" ] && git add docs/INSTRUCOES_COMPILACAO.md

# Figuras
echo "  ✓ Figuras..."
git add figs/storytelling/ 2>/dev/null
git add figs/eda/boxplot_bioma.png figs/eda/series_bioma.png figs/eda/top10_uf.png 2>/dev/null

# Dependências
echo "  ✓ Dependências..."
git add requirements.txt

# Notebooks (opcional)
echo "  ✓ Notebooks..."
git add notebooks/*.ipynb 2>/dev/null || true

# Documentação opcional
echo "  ✓ Documentação adicional..."
[ -f "ETAPA3_RESUMO.md" ] && git add ETAPA3_RESUMO.md
[ -f "EXECUCOES_DIAGNOSTICO.md" ] && git add EXECUCOES_DIAGNOSTICO.md

echo ""
echo "📋 Arquivos preparados para commit:"
git status --short
echo ""

# Perguntar se deseja fazer commit
read -p "Deseja fazer commit agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "💾 Fazendo commit..."
    git commit -m "feat: Implementa Etapa 3 - Data Storytelling

- Adiciona script storytelling_viz.py com visualizações para apresentação
- Atualiza documento LaTeX projeto_etapa3.tex com narrativa completa
- Gera 5 novas figuras de storytelling (timeline, heatmap, ranking, envelopes)
- Atualiza figuras EDA existentes
- Adiciona script de compilação LaTeX e instruções
- Atualiza requirements.txt com dependências necessárias

Artefatos:
- 5 figuras de storytelling em figs/storytelling/
- Documento LaTeX completo com storytelling estruturado
- Scripts Python para geração de visualizações"
    
    echo ""
    echo "✅ Commit realizado!"
    echo ""
    
    # Perguntar se deseja fazer push
    read -p "Deseja fazer push para o GitHub agora? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo ""
        echo "🚀 Fazendo push..."
        git push origin main
        echo ""
        echo "✅ Push realizado com sucesso!"
    else
        echo ""
        echo "ℹ️  Para fazer push depois, execute: git push origin main"
    fi
else
    echo ""
    echo "ℹ️  Arquivos adicionados ao staging. Para fazer commit depois:"
    echo "   git commit -m 'feat: Implementa Etapa 3 - Data Storytelling'"
    echo "   git push origin main"
fi

echo ""
echo "=== Concluído ==="

