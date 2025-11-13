#!/bin/bash
# Script para compilar o documento LaTeX da Etapa 3

echo "=== Compilando projeto_etapa3.tex ==="
echo ""

# Verificar se pdflatex está instalado
if ! command -v pdflatex &> /dev/null; then
    echo "❌ ERRO: pdflatex não está instalado!"
    echo ""
    echo "Para instalar no macOS:"
    echo "  brew install --cask mactex"
    echo ""
    echo "Ou use Overleaf (online): https://www.overleaf.com/"
    echo ""
    exit 1
fi

# Primeira compilação
echo "📄 Primeira compilação..."
pdflatex -interaction=nonstopmode projeto_etapa3.tex > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Erro na primeira compilação. Verifique os logs acima."
    exit 1
fi

# Segunda compilação (para referências cruzadas)
echo "📄 Segunda compilação (referências cruzadas)..."
pdflatex -interaction=nonstopmode projeto_etapa3.tex > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Erro na segunda compilação. Verifique os logs acima."
    exit 1
fi

# Limpar arquivos auxiliares
echo "🧹 Limpando arquivos auxiliares..."
rm -f *.aux *.log *.out *.toc *.lof *.lot 2>/dev/null

# Verificar se o PDF foi gerado
if [ -f "projeto_etapa3.pdf" ]; then
    PDF_SIZE=$(ls -lh projeto_etapa3.pdf | awk '{print $5}')
    echo ""
    echo "✅ PDF gerado com sucesso!"
    echo "   Arquivo: projeto_etapa3.pdf ($PDF_SIZE)"
    echo ""
else
    echo "❌ PDF não foi gerado. Verifique os erros acima."
    exit 1
fi

