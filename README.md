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

## Etapa 3 - Data Storytelling ✅

### Implementação Completa

A Etapa 3 implementa o **Data Storytelling** completo com narrativa estruturada, visualizações avançadas e documentação detalhada para a apresentação final.

### Estrutura Atualizada do Repositório

```
projeto_aplicado_grupo_12/
├── data/
│   ├── raw/queimadas/          # CSVs originais (2019-2024, não versionados)
│   ├── interim/                # Dados intermediários (não versionados)
│   └── processed/              # Dados processados e artefatos CSV
│       ├── focos_2019_2024.parquet  # Dataset consolidado (108 MB, não versionado)
│       ├── resumo_colunas.csv
│       ├── estatisticas_gerais.csv
│       └── anomalias_top.csv
├── figs/
│   ├── eda/                    # Figuras da análise exploratória
│   │   ├── series_bioma.png
│   │   ├── boxplot_bioma.png
│   │   └── top10_uf.png
│   └── storytelling/           # Figuras para apresentação (Etapa 3)
│       ├── timeline_anomalies.png
│       ├── series_envelope_bioma.png
│       ├── heatmap_temporal.png
│       ├── ranking_criticidade_municipios.png
│       └── anomalies_by_bioma.png
├── src/                        # Scripts Python
│   ├── pipeline_ingestao.py   # ETL e consolidação dos CSVs
│   ├── eda_utils.py           # Análise exploratória e visualizações básicas
│   ├── storytelling_viz.py    # Visualizações de storytelling (Etapa 3) ⭐ NOVO
│   ├── cleaning.py            # Utilitários de limpeza
│   ├── io_utils.py            # Utilitários de I/O
│   └── plotting.py            # Funções auxiliares de plotagem
├── notebooks/                  # Notebooks Jupyter
│   ├── EDA_inicial.ipynb
│   ├── EDA_queimadas_etapa2.ipynb
│   ├── 01_ingestao_validacao.ipynb
│   ├── 02_aed_univariada.ipynb
│   ├── 03_aed_temporal_espacial.ipynb
│   └── 04_proposta_analitica_demo.ipynb
├── docs/                       # Documentação LaTeX
│   ├── projeto_aplicado.tex   # Documento da Etapa 2
│   ├── projeto_etapa3.tex     # Documento da Etapa 3 ⭐ NOVO
│   ├── compilar.sh            # Script de compilação LaTeX ⭐ NOVO
│   ├── INSTRUCOES_COMPILACAO.md  # Instruções de compilação ⭐ NOVO
│   ├── cronograma.md
│   └── etapa1_entrega.md
├── requirements.txt            # Dependências Python
├── GUIA_GIT.md                # Guia para atualizar o repositório ⭐ NOVO
└── atualizar_git.sh           # Script para atualizar Git ⭐ NOVO
```

### Como Executar - Etapa 3

#### 1. Instalar Dependências (atualizado)

```bash
pip install -r requirements.txt
```

**Novas dependências adicionadas:**
- `seaborn>=0.13` - Visualizações avançadas
- `jupyter>=1.0` - Notebooks Jupyter
- `ipykernel>=6.29` - Kernel Jupyter

#### 2. Executar Pipeline de Ingestão (se necessário)

```bash
python -m src.pipeline_ingestao
```

**Saída:**
- `data/processed/focos_2019_2024.parquet` (2.008.071 registros limpos, 108 MB)

#### 3. Executar Análise Exploratória Básica

```bash
python -m src.eda_utils
```

**Saídas:**
- `data/processed/resumo_colunas.csv`
- `data/processed/estatisticas_gerais.csv`
- `data/processed/anomalias_top.csv`
- `figs/eda/*.png` (3 figuras)

#### 4. Gerar Visualizações de Storytelling ⭐ NOVO

```bash
python -m src.storytelling_viz
```

**Saídas:**
- `figs/storytelling/timeline_anomalies.png` - Linha do tempo de picos anômalos
- `figs/storytelling/series_envelope_bioma.png` - Séries com envelope sazonal
- `figs/storytelling/heatmap_temporal.png` - Heatmap temporal (mês/ano)
- `figs/storytelling/ranking_criticidade_municipios.png` - Ranking Top 15 municípios
- `figs/storytelling/anomalies_by_bioma.png` - Distribuição de anomalias por bioma

#### 5. Explorar com Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

**Notebooks disponíveis:**
- `EDA_queimadas_etapa2.ipynb` - Análise exploratória da Etapa 2
- `01_ingestao_validacao.ipynb` - Validação de ingestão
- `02_aed_univariada.ipynb` - AED univariada
- `03_aed_temporal_espacial.ipynb` - AED temporal e espacial
- `04_proposta_analitica_demo.ipynb` - Demonstração da proposta analítica

#### 6. Compilar Documento LaTeX da Etapa 3

**Opção A: Usando o script (recomendado)**

```bash
cd docs/
./compilar.sh
```

**Opção B: Manualmente**

```bash
cd docs/
pdflatex projeto_etapa3.tex
pdflatex projeto_etapa3.tex  # Segunda compilação para referências
```

**Opção C: Overleaf (online)**

1. Acesse: https://www.overleaf.com/
2. Faça upload de `docs/projeto_etapa3.tex` e toda a pasta `figs/`
3. Clique em "Recompile"

**Saída:** `docs/projeto_etapa3.pdf`

### Artefatos da Etapa 3

#### 📊 Visualizações de Storytelling (5 novas figuras)
- **Linha do tempo de anomalias**: Picos críticos de 2020 e 2024
- **Séries com envelope sazonal**: Envelopes Q25-Q75 por bioma
- **Heatmap temporal**: Distribuição de focos por mês/ano
- **Ranking de criticidade**: Top 15 municípios por número de focos
- **Anomalias por bioma**: Distribuição de z-scores robustos

#### 📝 Documentação
- **Documento LaTeX completo**: `docs/projeto_etapa3.tex`
  - Narrativa estruturada em três atos (Setup, Conflito, Resolução)
  - Storyboard completo (10 slides)
  - Roteiro de falas por pessoa
  - Descrição detalhada de todas as variáveis
  - Análise completa de valores ausentes e outliers
- **Scripts de compilação**: `docs/compilar.sh`
- **Instruções**: `docs/INSTRUCOES_COMPILACAO.md`

#### 💻 Código Python
- **Script de storytelling**: `src/storytelling_viz.py`
  - 5 funções de visualização
  - Código bem documentado
  - Boas práticas de organização
- **Scripts auxiliares**: `cleaning.py`, `io_utils.py`, `plotting.py`

#### 📈 Dados Processados
- **Dataset consolidado**: 2.008.071 registros (2019-2024)
- **Estatísticas**: Resumos, anomalias, agregações temporais
- **CSVs processados**: 6 arquivos de análise

### Narrativa de Storytelling

A narrativa segue a estrutura clássica em três atos:

1. **Setup (Slides 1-3)**: Apresentação, contexto dos biomas, dados disponíveis
2. **Conflito (Slides 4-6)**: Onde está o fogo, sazonalidade, picos anômalos
3. **Resolução (Slides 7-10)**: Proposta analítica, resultados pretendidos, próximos passos

**Nome do projeto:** "Fogo sob Controle: priorização territorial de focos de queimadas (2019-2024)"

### Checklist da Rubrica - Etapa 3

#### ✅ Esboço do Storytelling (4 pts - ÓTIMO)
- ✅ Apresentação do grupo
- ✅ Nome do projeto
- ✅ Empresa/Organização (INPE)
- ✅ Área do problema
- ✅ Descrição do problema/gap
- ✅ Proposta analítica
- ✅ Dados disponíveis
- ✅ Análise exploratória
- ✅ Resultados pretendidos

#### ✅ Scripts da Análise Exploratória (3 pts - ÓTIMO)
- ✅ Scripts inseridos no GitHub
- ✅ Notebooks Jupyter
- ✅ Escritos em Python
- ✅ Comentários e boas práticas

#### ✅ Seção de AED no Documento (3 pts - ÓTIMO)
- ✅ Descrição completa das variáveis
- ✅ Número de exemplares, máx/min, variância, desvio padrão
- ✅ Distribuições
- ✅ Análise de NAs e outliers
- ✅ Gráficos para detalhar a amostra

### Próximos Passos

1. ✅ **Etapa 3 concluída** - Todos os artefatos implementados
2. ✅ **Compilar LaTeX** - Gerar PDF final da Etapa 3
3. ✅ **Preparar apresentação** - Seguir storyboard do documento LaTeX
4. ✅ **Etapa 4** - Ajustes finais e apresentação

## Etapa 4 - Entrega Final ✅

### Apresentação Gravada

**Vídeo no YouTube:** [Assistir Apresentação](https://www.youtube.com/watch?v=a1U5Kp_8TQI)

A apresentação do projeto foi gravada e disponibilizada no YouTube, com duração entre 5 e 10 minutos, apresentando todos os elementos solicitados:
- ✅ Apresentação do grupo
- ✅ Nome do projeto: "Fogo sob Controle: priorização territorial de focos de queimadas (2019-2024)"
- ✅ Empresa/Organização de estudo: INPE - Programa Queimadas
- ✅ Área do problema: Monitoramento ambiental e gestão de riscos
- ✅ Descrição do problema/gap
- ✅ Proposta analítica
- ✅ Dados disponíveis
- ✅ Análise exploratória
- ✅ Resultados pretendidos

### Documento Final

O documento final do projeto está disponível no repositório:

- **Apresentação (Slides):** [`entrega_final/Fogo_sob_Controle_Priorização_de_Queimadas.pdf`](entrega_final/Fogo_sob_Controle_Priorização_de_Queimadas.pdf)
- **Relatório Final:** [`entrega_final/Etapa_Final.pdf`](entrega_final/Etapa_Final.pdf)

### Estrutura da Entrega Final

```
projeto_aplicado_grupo_12/
├── entrega_final/                    # ⭐ NOVO - Entrega Final
│   ├── Fogo_sob_Controle_Priorização_de_Queimadas.pdf  # Apresentação
│   └── Etapa_Final.pdf               # Relatório Final
└── ...
```

### Checklist da Rubrica - Etapa 4

#### ✅ Apresentação Gravada (5 pts - ÓTIMO)
- ✅ Apresentação disponibilizada no YouTube
- ✅ Link disponibilizado no GitHub (README.md)
- ✅ Duração entre 5 e 10 minutos
- ✅ Apresenta todos os elementos solicitados:
  - ✅ Apresentação do grupo
  - ✅ Nome do projeto
  - ✅ Empresa/Organização de estudo
  - ✅ Área do problema
  - ✅ Descrição do problema/gap
  - ✅ Proposta analítica
  - ✅ Dados disponíveis
  - ✅ Análise exploratória
  - ✅ Resultados pretendidos

#### ✅ Documento Final (5 pts - ÓTIMO)
- ✅ Documento encaminhado no Canvas
- ✅ Documento inserido no GitHub (`entrega_final/`)
- ✅ Documento devidamente organizado
- ✅ Apresenta todos os elementos solicitados no início do projeto

## Cronograma (Etapa 1)

Ver `docs/cronograma.md` para atividades, datas, responsáveis e milestones.
