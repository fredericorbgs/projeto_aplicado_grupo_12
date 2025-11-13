# Instruções para Compilar o Documento LaTeX

## ⚠️ LaTeX não está instalado no sistema

Para compilar o documento `projeto_etapa3.tex`, você precisa instalar uma distribuição LaTeX.

## Opção 1: Instalar LaTeX no macOS (Recomendado)

### Usando Homebrew:
```bash
brew install --cask mactex
```

**Nota:** MacTeX é grande (~4GB). Após instalar, você precisará reiniciar o terminal ou executar:
```bash
export PATH="/usr/local/texlive/2024/bin/universal-darwin:$PATH"
```

### Depois de instalar, execute:
```bash
cd docs/
./compilar.sh
```

Ou manualmente:
```bash
cd docs/
pdflatex projeto_etapa3.tex
pdflatex projeto_etapa3.tex  # Segunda vez para referências
```

## Opção 2: Usar Overleaf (Online - Mais Rápido)

1. Acesse: https://www.overleaf.com/
2. Crie uma conta gratuita (se necessário)
3. Clique em "New Project" → "Upload Project"
4. Faça upload do arquivo `projeto_etapa3.tex`
5. **IMPORTANTE:** Você também precisa fazer upload das figuras:
   - `figs/eda/boxplot_bioma.png`
   - `figs/eda/series_bioma.png`
   - `figs/eda/top10_uf.png`
   - `figs/storytelling/timeline_anomalies.png`
   - `figs/storytelling/heatmap_temporal.png`
   - `figs/storytelling/ranking_criticidade_municipios.png`
   - `figs/storytelling/series_envelope_bioma.png`
   - `figs/storytelling/anomalies_by_bioma.png`

6. No Overleaf, mantenha a estrutura de diretórios:
   ```
   projeto_etapa3.tex
   figs/
     eda/
       boxplot_bioma.png
       series_bioma.png
       top10_uf.png
     storytelling/
       timeline_anomalies.png
       heatmap_temporal.png
       ranking_criticidade_municipios.png
       series_envelope_bioma.png
       anomalies_by_bioma.png
   ```

7. Clique em "Recompile" no Overleaf

## Opção 3: Instalar LaTeX Básico (Menor)

Se não quiser instalar o MacTeX completo (4GB), pode instalar apenas o básico:

```bash
brew install basictex
```

Depois:
```bash
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
sudo tlmgr install babel-portuges
```

## Verificação

Após instalar, verifique se funciona:
```bash
pdflatex --version
```

Se funcionar, execute:
```bash
cd /Users/fredericoborges/Pythons/projeto_aplicado_grupo_12/docs
./compilar.sh
```

## Estrutura de Arquivos Necessária

O LaTeX precisa encontrar as figuras. Certifique-se de que a estrutura está assim:

```
projeto_aplicado_grupo_12/
├── docs/
│   └── projeto_etapa3.tex
└── figs/
    ├── eda/
    │   ├── boxplot_bioma.png
    │   ├── series_bioma.png
    │   └── top10_uf.png
    └── storytelling/
        ├── timeline_anomalies.png
        ├── heatmap_temporal.png
        ├── ranking_criticidade_municipios.png
        ├── series_envelope_bioma.png
        └── anomalies_by_bioma.png
```

## Troubleshooting

### Erro: "File not found" para figuras
- Certifique-se de que está compilando a partir do diretório `docs/`
- Verifique se os caminhos das figuras no `.tex` estão corretos (relativos ao diretório `docs/`)

### Erro: "Package babel-portuges not found"
- Instale o pacote: `sudo tlmgr install babel-portuges`

### Erro: "Package tikz not found"
- Instale: `sudo tlmgr install pgf tikz-cd`

## Status Atual

✅ Documento LaTeX criado: `docs/projeto_etapa3.tex`
✅ Todas as figuras geradas e prontas
✅ Script de compilação criado: `docs/compilar.sh`
⏳ Aguardando instalação do LaTeX para compilação

