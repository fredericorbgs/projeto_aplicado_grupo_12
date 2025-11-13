"""
Storytelling Visualizations - Visualizações para Data Storytelling (Etapa 3)

Este script gera visualizações específicas para a apresentação de storytelling:
- Linha do tempo de picos anômalos (2020 e 2024)
- Séries temporais com envelopes sazonais
- Heatmap temporal (calor por mês/ano)
- Ranking de criticidade por município/UF/bioma
- Gráficos de anomalias com destaque visual

Uso:
    python -m src.storytelling_viz
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

# Configurações
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FIGS_DIR = PROJECT_ROOT / "figs" / "storytelling"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"] = 11
sns.set_style("whitegrid")
sns.set_palette("husl")


def load_data() -> pd.DataFrame:
    """Carrega Parquet consolidado."""
    # Tentar primeiro em processed, depois em interim
    parquet_path = PROCESSED_DIR / "focos_2019_2024.parquet"
    if not parquet_path.exists():
        interim_path = DATA_DIR / "interim" / "focos_2019_2024.parquet"
        if interim_path.exists():
            parquet_path = interim_path
        else:
            raise FileNotFoundError(
                f"Arquivo não encontrado em {PROCESSED_DIR} nem em {interim_path}. "
                "Execute pipeline_ingestao.py primeiro."
            )
    
    df = pd.read_parquet(parquet_path)
    df['date'] = pd.to_datetime(df['date'])
    print(f"Carregados {len(df):,} registros de {parquet_path.name}")
    return df


def plot_timeline_anomalies(df: pd.DataFrame) -> None:
    """Linha do tempo destacando picos anômalos de 2020 e 2024."""
    # Agregar por dia
    by_day = df.groupby('day').size().reset_index(name='focos')
    by_day['day'] = pd.to_datetime(by_day['day'])
    by_day = by_day.sort_values('day')
    
    # Detectar anomalias
    median_focos = by_day['focos'].median()
    mad = (by_day['focos'] - median_focos).abs().median()
    by_day['z_score'] = (by_day['focos'] - median_focos) / (1.4826 * mad)
    by_day['anomalia'] = by_day['z_score'].abs() >= 3
    
    # Filtrar anos críticos
    by_day['year'] = by_day['day'].dt.year
    critical_years = by_day[by_day['year'].isin([2020, 2024])].copy()
    anomalies = critical_years[critical_years['anomalia']].copy()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Plotar série completa
    ax.plot(by_day['day'], by_day['focos'], 
            color='lightgray', linewidth=0.8, alpha=0.5, label='Série completa')
    
    # Destacar anos críticos
    for year in [2020, 2024]:
        year_data = by_day[by_day['year'] == year]
        ax.plot(year_data['day'], year_data['focos'], 
                linewidth=2, label=f'{year}', alpha=0.8)
    
    # Marcar anomalias
    ax.scatter(anomalies['day'], anomalies['focos'], 
              color='red', s=100, zorder=5, alpha=0.7, 
              label='Picos anômalos (|z| ≥ 3)', marker='^')
    
    # Linha de referência (mediana)
    ax.axhline(y=median_focos, color='blue', linestyle='--', 
               linewidth=1.5, alpha=0.7, label=f'Mediana: {median_focos:.0f}')
    
    # Banda superior (mediana + 3*MAD)
    upper_band = median_focos + 3 * 1.4826 * mad
    ax.axhline(y=upper_band, color='orange', linestyle='--', 
               linewidth=1, alpha=0.5, label=f'Banda superior: {upper_band:.0f}')
    
    ax.set_title('Linha do Tempo: Picos Anômalos de Focos de Queimadas (2020 e 2024)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Número de focos por dia', fontsize=12)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = FIGS_DIR / "timeline_anomalies.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ {output_path.name}")


def plot_series_with_envelope(df: pd.DataFrame) -> None:
    """Série temporal mensal com envelope sazonal por bioma."""
    # Filtrar biomas válidos
    df_filtered = df[df['bioma'].notna() & (df['bioma'] != 'Nan') & (df['bioma'] != 'nan')].copy()
    
    # Agregar por mês e bioma
    df_filtered['year_month'] = df_filtered['date'].dt.to_period('M')
    by_month_bioma = df_filtered.groupby(['year_month', 'bioma']).size().reset_index(name='focos')
    by_month_bioma['year_month'] = by_month_bioma['year_month'].astype(str)
    by_month_bioma['date'] = pd.to_datetime(by_month_bioma['year_month'])
    
    # Focar nos principais biomas
    top_biomas = ['Amazônia', 'Cerrado', 'Caatinga', 'Mata Atlântica']
    by_month_bioma = by_month_bioma[by_month_bioma['bioma'].isin(top_biomas)]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    for idx, bioma in enumerate(top_biomas):
        ax = axes[idx]
        bioma_data = by_month_bioma[by_month_bioma['bioma'] == bioma].copy()
        bioma_data = bioma_data.sort_values('date')
        
        # Calcular estatísticas mensais (sazonalidade)
        bioma_data['month'] = bioma_data['date'].dt.month
        monthly_stats = bioma_data.groupby('month')['focos'].agg(['median'])
        monthly_stats['q25'] = bioma_data.groupby('month')['focos'].quantile(0.25)
        monthly_stats['q75'] = bioma_data.groupby('month')['focos'].quantile(0.75)
        
        # Plotar série
        ax.plot(bioma_data['date'], bioma_data['focos'], 
                linewidth=1.5, alpha=0.7, label='Série observada')
        
        # Envelope sazonal (usando mediana mensal)
        for month in range(1, 13):
            month_data = bioma_data[bioma_data['month'] == month]
            if len(month_data) > 0:
                dates = month_data['date']
                median_val = monthly_stats.loc[month, 'median']
                q25_val = monthly_stats.loc[month, 'q25']
                q75_val = monthly_stats.loc[month, 'q75']
                
                # Preencher envelope
                ax.fill_between(dates, q25_val, q75_val, 
                               alpha=0.2, color='orange', label='Envelope sazonal (Q25-Q75)' if month == 1 else '')
                ax.axhline(y=median_val, color='orange', linestyle='--', 
                         linewidth=1, alpha=0.5)
        
        ax.set_title(f'{bioma}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Data', fontsize=10)
        ax.set_ylabel('Focos mensais', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        if idx == 0:
            ax.legend(fontsize=8, loc='upper left')
    
    fig.suptitle('Séries Temporais com Envelope Sazonal por Bioma (2019-2024)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    output_path = FIGS_DIR / "series_envelope_bioma.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ {output_path.name}")


def plot_heatmap_temporal(df: pd.DataFrame) -> None:
    """Heatmap temporal: focos por mês e ano."""
    df_filtered = df[df['bioma'].notna() & (df['bioma'] != 'Nan') & (df['bioma'] != 'nan')].copy()
    
    # Agregar por ano e mês
    df_filtered['year'] = df_filtered['date'].dt.year
    df_filtered['month'] = df_filtered['date'].dt.month
    
    heatmap_data = df_filtered.groupby(['year', 'month']).size().reset_index(name='focos')
    heatmap_pivot = heatmap_data.pivot(index='month', columns='year', values='focos')
    heatmap_pivot = heatmap_pivot.fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.heatmap(heatmap_pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Número de focos'}, 
                linewidths=0.5, linecolor='gray', ax=ax)
    
    ax.set_title('Heatmap Temporal: Focos de Queimadas por Mês e Ano (2019-2024)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Mês', fontsize=12)
    
    # Nomes dos meses
    month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    ax.set_yticklabels(month_names, rotation=0)
    
    plt.tight_layout()
    
    output_path = FIGS_DIR / "heatmap_temporal.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ {output_path.name}")


def plot_ranking_criticidade(df: pd.DataFrame) -> None:
    """Ranking de criticidade: Top 15 municípios por número de focos."""
    df_filtered = df[df['municipio'].notna()].copy()
    
    # Agregar por município (contar registros)
    by_municipio = df_filtered.groupby('municipio').agg({
        'estado': 'first',
        'bioma': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
    }).reset_index()
    counts = df_filtered.groupby('municipio').size().reset_index(name='total_focos')
    by_municipio = by_municipio.merge(counts, on='municipio')
    
    # Top 15
    top15 = by_municipio.nlargest(15, 'total_focos')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Criar rótulos com município e UF
    labels = [f"{row['municipio']} ({row['estado']})" 
              for _, row in top15.iterrows()]
    
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(top15)))
    bars = ax.barh(range(len(top15)), top15['total_focos'], color=colors)
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(top15.iterrows()):
        ax.text(row['total_focos'] + 500, i, 
               f"{int(row['total_focos']):,}", 
               va='center', fontsize=9)
    
    ax.set_yticks(range(len(top15)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Total de focos (2019-2024)', fontsize=12)
    ax.set_title('Ranking de Criticidade: Top 15 Municípios por Focos de Queimadas', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()
    
    plt.tight_layout()
    
    output_path = FIGS_DIR / "ranking_criticidade_municipios.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ {output_path.name}")


def plot_anomalies_by_bioma(df: pd.DataFrame) -> None:
    """Gráfico de anomalias por bioma: distribuição de z-scores."""
    df_filtered = df[df['bioma'].notna() & (df['bioma'] != 'Nan') & (df['bioma'] != 'nan')].copy()
    
    # Agregar por dia e bioma
    by_day_bioma = df_filtered.groupby(['day', 'bioma']).size().reset_index(name='focos')
    by_day_bioma['day'] = pd.to_datetime(by_day_bioma['day'])
    
    # Calcular z-score robusto por bioma
    anomalies_list = []
    for bioma in by_day_bioma['bioma'].unique():
        bioma_data = by_day_bioma[by_day_bioma['bioma'] == bioma]['focos']
        median_val = bioma_data.median()
        mad = (bioma_data - median_val).abs().median()
        
        if mad > 0:
            z_scores = (bioma_data - median_val) / (1.4826 * mad)
            anomalies_list.append({
                'bioma': bioma,
                'z_score': z_scores.values,
                'focos': bioma_data.values
            })
    
    # Plotar
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    top_biomas = ['Amazônia', 'Cerrado', 'Caatinga', 'Mata Atlântica', 'Pantanal', 'Pampa']
    
    for idx, bioma in enumerate(top_biomas):
        ax = axes[idx]
        bioma_anomalies = [a for a in anomalies_list if a['bioma'] == bioma]
        
        if bioma_anomalies:
            data = bioma_anomalies[0]
            z_scores = data['z_score']
            focos = data['focos']
            
            # Scatter plot
            scatter = ax.scatter(focos, z_scores, alpha=0.5, s=20, c=z_scores, 
                                cmap='RdYlGn_r', vmin=-5, vmax=20)
            
            # Linhas de referência
            ax.axhline(y=3, color='red', linestyle='--', linewidth=1.5, 
                      label='Limiar anomalia (z=3)')
            ax.axhline(y=-3, color='red', linestyle='--', linewidth=1.5)
            ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
            
            ax.set_title(f'{bioma}', fontsize=11, fontweight='bold')
            ax.set_xlabel('Focos por dia', fontsize=9)
            ax.set_ylabel('Z-score robusto', fontsize=9)
            ax.grid(True, alpha=0.3)
            
            if idx == 0:
                ax.legend(fontsize=8)
    
    # Remover eixos extras
    for idx in range(len(top_biomas), len(axes)):
        fig.delaxes(axes[idx])
    
    fig.suptitle('Distribuição de Anomalias por Bioma (Z-score Robusto)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_path = FIGS_DIR / "anomalies_by_bioma.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ {output_path.name}")


def main() -> int:
    """Execução principal."""
    print("=== Storytelling Visualizations ===\n")
    
    try:
        df = load_data()
        
        print("\nGerando visualizações de storytelling:")
        plot_timeline_anomalies(df)
        plot_series_with_envelope(df)
        plot_heatmap_temporal(df)
        plot_ranking_criticidade(df)
        plot_anomalies_by_bioma(df)
        
        print("\n✓ Visualizações de storytelling concluídas!")
        print(f"Artefatos salvos em: {FIGS_DIR}")
        return 0
    
    except Exception as e:
        print(f"\n✗ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

