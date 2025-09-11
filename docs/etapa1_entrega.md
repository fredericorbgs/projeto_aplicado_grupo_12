# Dinâmica de Focos de Queimadas no Brasil (2019–2024) — **Etapa 1**

**Grupo:** Ana Clara · Cid Wallace · Eduardo Machado · Frederico Ripamonte
**Data:** 11/09/2025
**Repositório:** https://github.com/fredericorbgs/projeto_aplicado_grupo_12/

## Sumário
 
- [Glossário](#glossário)
- [Objetivo do estudo](#objetivo-do-estudo)
- [Apresentação da organização e problema de pesquisa](#apresentação-da-organização-e-problema-de-pesquisa)
- [Metadados e identificação da base de dados](#metadados-e-identificação-da-base-de-dados)
- [Pensamento computacional no contexto organizacional](#pensamento-computacional-no-contexto-organizacional)
- [Cronograma e responsabilidades (Etapa 1)](#cronograma-e-responsabilidades-etapa-1)
- [Síntese da proposta analítica (rascunho para Etapa 2)](#síntese-da-proposta-analítica-rascunho-para-etapa-2)
- [Lista de Figuras](#lista-de-figuras)
- [Lista de Tabelas](#lista-de-tabelas)
- [Referências](#referências)

## Glossário
 
- **Foco de queimada (hotspot):** detecção por satélite de alta temperatura associada a fogo ativo.
- **Bioma:** grande conjunto de ecossistemas (Amazônia, Cerrado, Caatinga, Mata Atlântica, Pampa, Pantanal).
- **Sazonalidade:** padrão recorrente no tempo (ex.: “estação de fogo”).
- **Anomalia:** observação acima/abaixo do esperado considerando tendência e sazonalidade.
- **Data storytelling:** narrativa que integra achados, gráficos e contexto.

## Objetivo do estudo
 
Conduzir um **estudo prático** com dois produtos:
1. **Análise Exploratória de Dados (AED)** de focos de queimadas no Brasil (2019–2024).
2. **Proposta analítica** aplicável à base, para **detecção de anomalias e priorização territorial**.

## Apresentação da organização e problema de pesquisa
 
**Organização geradora dos dados:** **INPE — Programa Queimadas** (instituição pública federal).
**Problema:** como **descrever e priorizar** a dinâmica espaço-temporal dos focos, identificando **biomas/UFs/municípios críticos** e **picos atípicos**?
**Questões-guia:**
- Qual a **sazonalidade** por bioma e UF entre 2019 e 2024?
- Quais **municípios** concentram picos recorrentes?
- Como **medir anomalias** em relação ao comportamento esperado?

## Metadados e identificação da base de dados
 
- **Arquivos:** CSVs anuais baixados do diretório:
  `/queimadas/focos/csv/anual/AMS_sat_ref/`
- **Exemplo de colunas:**
  `id_bdq, foco_id, lat, lon, data_pas, pais, estado, municipio, bioma`
- **Período:** 2019–2024 (amostra atual).
- **Escopo desta etapa:** Brasil; pontos georreferenciados com data/hora (**data_pas**).
- **Cuidados técnicos:** normalização de encoding (acentos), consistência de nomes de municípios, fusos horários/UTC, e validação de coordenadas fora do Brasil.

## Pensamento computacional no contexto organizacional
 
- **Decomposição:** separar o problema em (i) ingestão/limpeza; (ii) agregações por bioma/UF/município; (iii) séries temporais (diário/semanal/mensal); (iv) detecção de anomalias; (v) visualização e narrativa.
- **Abstração/modelagem:** definir chaves `bioma|uf|municipio|data` e **métricas** (focos/dia, médias móveis 7/30, percentis).
- **Reconhecimento de padrões:** sazonalidade por bioma e janelas típicas de pico.
- **Automação:** scripts de ETL (Pandas/GeoPandas), *notebooks* de EDA e geração automática de gráficos/tabelas.

## Cronograma e responsabilidades (Etapa 1)
 
| Data | Atividade | Responsável | Marco |
|---|---|---|---|
| 11/09 | Repo criado + README + relatório Etapa 1 | Frederico (PM) / Ana (Doc) | **Entrega Etapa 1** |
| 13/09 | Kickoff + alinhamento de escopo e dúvidas | Todos | Go/No-Go |
| 18/09 | Mensagem ao professor (proposta + dúvidas) | Frederico | Orientação |
| 22/09 | Ingestão inicial + *data card* (metadados) | Cid | Dados prontos |
| 27/09 | EDA V0.1 (séries por bioma/UF/município) | Eduardo | V0.1 |
| 30/09 | Revisão interna + ajustes | Todos | V0.2 |
| 04/10 | Desenho detalhado da proposta analítica | Cid/Eduardo | Plano do modelo |
| 07/10 | Checkpoint com professor | Frederico | OK |

## Síntese da proposta analítica (rascunho para Etapa 2)
 
- **Objetivo:** detectar **dias/locais anômalos** por bioma/UF/município.  
- **Método-base:** séries agregadas (diário/semanal) com **tendência + sazonalidade** (média móvel/ETS) e **z-score robusto** para flag de picos; ranking por **desvio relativo** e **percentil**.  
- **Saídas:**  
  - Painel com **mapa choropleth** (UF/município) e *sparklines* por bioma.  
  - **Top-10 áreas críticas** por ano/estação.  
- **Validação:** checagem histórica de períodos de pico (ex.: meses secos) e comparação entre anos (2019–2024).

## Lista de Figuras
 
- **Figura 1.** Mapa de referência do Brasil por bioma (a inserir na Etapa 2).  
- **Figura 2.** Série temporal agregada (focos/dia) por bioma (a inserir).  

## Lista de Tabelas
 
- **Tabela 1.** Dicionário de colunas mínimas do CSV (esta seção).  
- **Tabela 2.** Cronograma de atividades (seção anterior).

## Referências
 
- INPE — Programa Queimadas (página e documentação pública).  
- Documentação dos arquivos CSV (metadados oficiais do INPE).  
- Materiais da disciplina (Etapas 1–4: objetivo, EDA e data storytelling).
