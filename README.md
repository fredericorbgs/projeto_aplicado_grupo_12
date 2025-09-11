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

## Cronograma (Etapa 1)

Ver `docs/cronograma.md` para atividades, datas, responsáveis e milestones.

## Data Storytelling (visão — Etapa 3)

Três atos: **Onde e quando ocorre** (mapas e séries) → **Quão atípico é** (anomalias) → **O que priorizar** (ranking e recomendações).