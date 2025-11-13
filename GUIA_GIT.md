# Guia para Atualizar o Repositório Git

## 📋 Arquivos que DEVEM ser commitados (Etapa 3)

### ✅ Código Python (NOVO)
- `src/storytelling_viz.py` ⭐ **NOVO - IMPORTANTE**
- `src/cleaning.py` (se não existia antes)
- `src/io_utils.py` (se não existia antes)
- `src/plotting.py` (se não existia antes)

### ✅ Documentação LaTeX
- `docs/projeto_etapa3.tex` ⭐ **MODIFICADO - IMPORTANTE**
- `docs/compilar.sh` ⭐ **NOVO**
- `docs/INSTRUCOES_COMPILACAO.md` ⭐ **NOVO**

### ✅ Figuras Geradas
- `figs/eda/boxplot_bioma.png` (atualizado)
- `figs/eda/series_bioma.png` (atualizado)
- `figs/eda/top10_uf.png` (atualizado)
- `figs/storytelling/timeline_anomalies.png` ⭐ **NOVO**
- `figs/storytelling/series_envelope_bioma.png` ⭐ **NOVO**
- `figs/storytelling/heatmap_temporal.png` ⭐ **NOVO**
- `figs/storytelling/ranking_criticidade_municipios.png` ⭐ **NOVO**
- `figs/storytelling/anomalies_by_bioma.png` ⭐ **NOVO**

### ✅ Dependências
- `requirements.txt` (atualizado com seaborn, jupyter)

### ✅ Notebooks (se existirem)
- `notebooks/01_ingestao_validacao.ipynb` (se for novo)
- `notebooks/02_aed_univariada.ipynb` (se for novo)
- `notebooks/03_aed_temporal_espacial.ipynb` (se for novo)
- `notebooks/04_proposta_analitica_demo.ipynb` (se for novo)

## ❌ Arquivos que NÃO devem ser commitados

### Dados (muito grandes)
- `data/raw/` (já está no .gitignore)
- `data/processed/*.parquet` (já está no .gitignore)
- `data/interim/` (dados temporários)

### Arquivos temporários
- `__pycache__/` (já está no .gitignore)
- `*.pyc` (já está no .gitignore)
- `*.aux`, `*.log`, `*.out` (LaTeX temporários)
- `.DS_Store` (macOS)

### Arquivos opcionais (decidir se quer commit)
- `ETAPA3_RESUMO.md` (documentação interna - pode commit)
- `EXECUCOES_DIAGNOSTICO.md` (documentação interna - pode commit)
- `PROJ_APLIC_I_AULA_3_Storytelling.pdf` (muito grande - não recomendado)
- `requirements.txt.backup` (backup - não commit)
- `projeto_aplicado.tex` (duplicado na raiz - não commit)

## 🚀 Comandos Git para Atualizar o Reppositório

### 1. Verificar status atual
```bash
cd /Users/fredericoborges/Pythons/projeto_aplicado_grupo_12
git status
```

### 2. Adicionar arquivos importantes (Etapa 3)

```bash
# Código Python novo
git add src/storytelling_viz.py
git add src/cleaning.py src/io_utils.py src/plotting.py 2>/dev/null || true

# Documentação LaTeX
git add docs/projeto_etapa3.tex
git add docs/compilar.sh
git add docs/INSTRUCOES_COMPILACAO.md

# Figuras novas de storytelling
git add figs/storytelling/

# Figuras atualizadas de EDA
git add figs/eda/boxplot_bioma.png
git add figs/eda/series_bioma.png
git add figs/eda/top10_uf.png

# Dependências atualizadas
git add requirements.txt

# Notebooks (se quiser)
git add notebooks/*.ipynb 2>/dev/null || true

# Documentação opcional
git add ETAPA3_RESUMO.md EXECUCOES_DIAGNOSTICO.md 2>/dev/null || true
```

### 3. Verificar o que será commitado
```bash
git status
```

### 4. Fazer commit
```bash
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
```

### 5. Push para o GitHub
```bash
git push origin main
```

## 📝 Script Automatizado

Criei um script `atualizar_git.sh` que faz tudo automaticamente. Execute:

```bash
chmod +x atualizar_git.sh
./atualizar_git.sh
```

## 🔍 Verificação Pós-Commit

Após fazer push, verifique no GitHub:
1. ✅ `src/storytelling_viz.py` aparece no repositório
2. ✅ `docs/projeto_etapa3.tex` está atualizado
3. ✅ Pasta `figs/storytelling/` existe com 5 figuras
4. ✅ `requirements.txt` está atualizado

## ⚠️ Importante

- **NÃO commite** arquivos `.parquet` (muito grandes)
- **NÃO commite** `__pycache__` ou arquivos temporários
- **NÃO commite** PDFs grandes se não forem essenciais
- **SEMPRE** verifique com `git status` antes de fazer commit

## 📊 Tamanho Estimado dos Arquivos

- Figuras: ~1 MB total (8 figuras PNG)
- Código Python: ~20 KB
- LaTeX: ~30 KB
- **Total a ser commitado: ~1.05 MB** (muito razoável)

