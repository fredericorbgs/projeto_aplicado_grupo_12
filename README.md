# Dinâmica de Focos de Queimadas no Brasil (2019–2024) — Projeto Aplicado I

**Grupo:**  

- ANA CLARA SILVA DE SOUZA
- CID WALLACE ARAUJO DE OLIVEIRA
- EDUARDO MACHADO SILVA
- FREDERICO RIPAMONTE BORGES

**Repositório:** [github.com/fredericorbgs/projeto_aplicado_grupo_12](https://github.com/fredericorbgs/projeto_aplicado_grupo_12/)

## Objetivo do estudo

Desenvolver um estudo prático com dois produtos:

1) **Análise Exploratória de Dados (AED)** dos focos de queimadas no Brasil 
(2019–2024).  
2) **Proposta analítica** aplicável ao conjunto de dados selecionado (detecção de anomalias e priorização territorial).

## Contexto organizacional (origem dos dados)

Os dados são produzidos e mantidos pelo **INPE — Programa Queimadas** (organização pública federal), cujo objetivo é monitorar e divulgar informações sobre queimadas/incêndios florestais no território nacional e países vizinhos, apoiando políticas públicas e a gestão ambiental.

## Problema de pesquisa (caracterização)

Como **caracterizar a dinâmica espaço-temporal** dos focos de calor no Brasil, identificando **sazonalidade por bioma/UF/município**, **anomalias** (picos atípicos) e **áreas críticas** para priorização de ações?

## Base de dados (metadados-chave)

- **Arquivos:** CSVs anuais (2019–2024) — diretório: `/queimadas/focos/csv/anual/AMS_sat_ref/`  
- **Granularidade:** ponto (foco) com coordenadas geográficas e carimbo de data/hora  
- **Colunas mínimas (exemplo):** `id_bdq, foco_id, lat, lon, data_pas, pais, estado, municipio, bioma`  
- **Observações técnicas:** pode haver diferenças de encoding (ex.: `VIT√ÒRIA DA CONQUISTA` → *Vitória da Conquista*). Tratar com `encoding='latin1'` ou normalização UTF-8.

## Abordagem por etapas

- **Etapa 1 (30 dias, entrega 11/09/2025):** premissas, objetivos e metas, cronograma, definição de grupos e mapeamento de **Pensamento Computacional** ao contexto do INPE.  
- **Etapa 2 (30 dias):** AED completa + **proposta analítica** formal (alvo, features, métrica, validação).  
- **Etapa 3 (30 dias):** **Data Storytelling** (narrativa visual, painéis e relatório executivo).  
- **Etapa 4 (30 dias):** ajustes finais e apresentação.

## Proposta analítica (rascunho para Etapa 2)

- **Alvo:** detectar **dias/municípios anômalos** (picos de focos acima do esperado) por **bioma/UF**, usando tendência+sazonalidade (ex.: média móvel/ETS) e *z-score* robusto.  
- **Saídas:** ranking de **áreas críticas** com percentis e bandas de confiança; painel com *sparkline* por bioma/UF/município.  
- **Métricas:** precisão na identificação de picos históricos conhecidos; estabilidade das faixas (backtesting simples).

## Etapa 2 - Implementação Completa ✅

### Estrutura do Repositório

```
projeto_aplicado_grupo_12/
├── data/
│   ├── raw/queimadas/          # CSVs originais (2019-2024, não versionados)
│   └── processed/              # Dados processados e artefatos CSV
│       ├── focos_2019_2024.parquet  # Dataset consolidado (108 MB)
│       ├── resumo_colunas.csv
│       ├── estatisticas_gerais.csv
│       └── anomalias_top.csv
├── figs/eda/                   # Figuras geradas pela análise
│   ├── series_bioma.png
│   ├── boxplot_bioma.png
│   └── top10_uf.png
├── src/                        # Scripts Python
│   ├── pipeline_ingestao.py   # ETL e consolidação dos CSVs
│   └── eda_utils.py           # Análise exploratória e visualizações
├── notebooks/                  # Notebooks Jupyter
│   ├── EDA_inicial.ipynb
│   └── EDA_queimadas_etapa2.ipynb  # Notebook da Etapa 2
├── docs/                       # Documentação LaTeX
│   ├── projeto_aplicado.tex   # Documento principal
│   ├── projeto_aplicado.pdf   # PDF compilado (15 páginas)
│   ├── cronograma.md
│   └── etapa1_entrega.md
└── requirements.txt            # Dependências Python
```

### Como Executar

#### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 2. Executar Pipeline de Ingestão

Consolida os CSVs anuais (2019-2024) em um único arquivo Parquet:

```bash
python -m src.pipeline_ingestao
```

**Saída:**
- `data/processed/focos_2019_2024.parquet` (2.008.071 registros limpos)

#### 3. Executar Análise Exploratória

Gera estatísticas, figuras e detecção de anomalias:

```bash
python -m src.eda_utils
```

**Saídas:**
- `data/processed/resumo_colunas.csv`
- `data/processed/estatisticas_gerais.csv`
- `data/processed/anomalias_top.csv`
- `figs/eda/*.png` (3 figuras)

#### 4. Explorar com Jupyter Notebook

```bash
jupyter notebook notebooks/EDA_queimadas_etapa2.ipynb
```

#### 5. Compilar Documento LaTeX

```bash
cd docs/
pdflatex projeto_aplicado.tex
pdflatex projeto_aplicado.tex  # Segunda compilação para referências
```

**Saída:** `docs/projeto_aplicado.pdf`

### Artefatos da Etapa 2

- 📊 **Dataset consolidado**: 2M+ registros de focos (2019-2024)
- 📈 **3 figuras principais**: séries temporais, boxplots, rankings
- 📝 **4 CSVs de análise**: resumos, estatísticas e anomalias
- 📄 **Documento PDF**: 15 páginas com proposta analítica e AED completa
- 💻 **Código Python**: scripts modulares e notebook reproduzível

## Cronograma (Etapa 1)

Ver `docs/cronograma.md` para atividades, datas, responsáveis e milestones.

## Data Storytelling (visão — Etapa 3)

Três atos: **Onde e quando ocorre** (mapas e séries) → **Quão atípico é** (anomalias) → **O que priorizar** (ranking e recomendações).
