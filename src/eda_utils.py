"""
EDA Utils - Análise Exploratória de Dados

Este script:
- Carrega o Parquet consolidado
- Gera estatísticas descritivas (posição, dispersão, CV)
- Cria visualizações (séries temporais, boxplots, histogramas)
- Detecta anomalias (z-score robusto e IQR)
- Exporta artefatos (CSVs de resumo e figuras)

Uso:
    python -m src.eda_utils
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Configurações
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FIGS_DIR = PROJECT_ROOT / "figs" / "eda"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["figure.dpi"] = 100
plt.rcParams["font.size"] = 10


def load_data() -> pd.DataFrame:
    """Carrega Parquet consolidado."""
    parquet_path = PROCESSED_DIR / "focos_2019_2024.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(
            f"{parquet_path} não encontrado. Execute pipeline_ingestao.py primeiro."
        )
    
    df = pd.read_parquet(parquet_path)
    print(f"Carregados {len(df):,} registros de {parquet_path.name}")
    return df


def generate_summary_stats(df: pd.DataFrame) -> None:
    """Gera estatísticas de resumo das colunas."""
    info_list = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        n_missing = df[col].isna().sum()
        n_unique = df[col].nunique()
        
        # Min/Max para numéricos
        if pd.api.types.is_numeric_dtype(df[col]):
            col_min = df[col].min()
            col_max = df[col].max()
        else:
            col_min = None
            col_max = None
        
        info_list.append({
            "coluna": col,
            "tipo": dtype,
            "n_missing": n_missing,
            "pct_missing": round(n_missing / len(df) * 100, 2),
            "n_unique": n_unique,
            "min": col_min,
            "max": col_max,
        })
    
    info_df = pd.DataFrame(info_list)
    output_path = PROCESSED_DIR / "resumo_colunas.csv"
    info_df.to_csv(output_path, index=False)
    print(f"✓ {output_path.name}")


def generate_general_stats(df: pd.DataFrame) -> None:
    """Estatísticas gerais: contagem de registros por bioma, UF, ano."""
    stats = {
        "total_registros": len(df),
        "anos": df["year"].nunique() if "year" in df.columns else 0,
        "periodo": f"{df['date'].min().date()} a {df['date'].max().date()}" if "date" in df.columns else "N/A",
    }
    
    # Por bioma
    bioma_col = None
    for candidate in ["bioma"]:
        if candidate in df.columns:
            bioma_col = candidate
            break
    
    if bioma_col:
        by_bioma = df[bioma_col].value_counts().head(10)
        for bioma, count in by_bioma.items():
            stats[f"bioma_{bioma}"] = count
    
    # Por UF
    uf_col = None
    for candidate in ["estado", "uf"]:
        if candidate in df.columns:
            uf_col = candidate
            break
    
    if uf_col:
        by_uf = df[uf_col].value_counts().head(10)
        for uf, count in by_uf.items():
            stats[f"uf_{uf}"] = count
    
    stats_df = pd.DataFrame([stats]).T
    stats_df.columns = ["valor"]
    output_path = PROCESSED_DIR / "estatisticas_gerais.csv"
    stats_df.to_csv(output_path)
    print(f"✓ {output_path.name}")


def plot_series_by_bioma(df: pd.DataFrame) -> None:
    """Plota séries temporais de focos por dia, agrupadas por bioma."""
    bioma_col = None
    for candidate in ["bioma"]:
        if candidate in df.columns:
            bioma_col = candidate
            break
    
    if not bioma_col:
        print("  ⚠ Coluna 'bioma' não encontrada, pulando gráfico por bioma")
        return
    
    # Agregar por dia e bioma
    by_day_bioma = df.groupby(["day", bioma_col]).size().reset_index(name="focos")
    by_day_bioma["day"] = pd.to_datetime(by_day_bioma["day"])
    
    # Plotar
    fig, ax = plt.subplots(figsize=(14, 6))
    for bioma in by_day_bioma[bioma_col].unique():
        subset = by_day_bioma[by_day_bioma[bioma_col] == bioma]
        ax.plot(subset["day"], subset["focos"], label=bioma, alpha=0.7, linewidth=1)
    
    ax.set_title("Focos por dia (2019-2024) - Por Bioma")
    ax.set_xlabel("Data")
    ax.set_ylabel("Número de focos")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = FIGS_DIR / "series_bioma.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✓ {output_path.name}")


def plot_boxplot_by_bioma(df: pd.DataFrame) -> None:
    """Boxplot de focos diários por bioma."""
    bioma_col = None
    for candidate in ["bioma"]:
        if candidate in df.columns:
            bioma_col = candidate
            break
    
    if not bioma_col:
        print("  ⚠ Coluna 'bioma' não encontrada, pulando boxplot")
        return
    
    by_day_bioma = df.groupby(["day", bioma_col]).size().reset_index(name="focos")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    biomas = sorted(by_day_bioma[bioma_col].unique())
    data_to_plot = [by_day_bioma[by_day_bioma[bioma_col] == b]["focos"] for b in biomas]
    
    ax.boxplot(data_to_plot, tick_labels=biomas, patch_artist=True)
    ax.set_title("Distribuição de focos diários por Bioma")
    ax.set_ylabel("Focos por dia")
    ax.set_xlabel("Bioma")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    
    output_path = FIGS_DIR / "boxplot_bioma.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✓ {output_path.name}")


def plot_top_uf(df: pd.DataFrame) -> None:
    """Gráfico de barras - Top 10 UFs por focos."""
    uf_col = None
    for candidate in ["estado", "uf"]:
        if candidate in df.columns:
            uf_col = candidate
            break
    
    if not uf_col:
        print("  ⚠ Coluna de UF não encontrada, pulando gráfico Top UF")
        return
    
    top_uf = df[uf_col].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_uf.plot(kind="barh", ax=ax, color="coral")
    ax.set_title("Top 10 UFs por número de focos (2019-2024)")
    ax.set_xlabel("Número de focos")
    ax.set_ylabel("UF")
    ax.invert_yaxis()
    plt.tight_layout()
    
    output_path = FIGS_DIR / "top10_uf.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✓ {output_path.name}")


def detect_anomalies_simple(df: pd.DataFrame) -> None:
    """Detecta anomalias simples por z-score robusto (MAD) em focos diários."""
    # Agregar por dia
    by_day = df.groupby("day").size().reset_index(name="focos")
    by_day["day"] = pd.to_datetime(by_day["day"])
    
    # Z-score robusto (MAD)
    median_focos = by_day["focos"].median()
    mad = (by_day["focos"] - median_focos).abs().median()
    
    if mad == 0:
        print("  ⚠ MAD = 0, sem detecção de anomalias")
        return
    
    by_day["z_score_robust"] = (by_day["focos"] - median_focos) / (1.4826 * mad)
    by_day["anomalia"] = by_day["z_score_robust"].abs() >= 3
    
    anomalies = by_day[by_day["anomalia"]].copy()
    anomalies = anomalies.sort_values("focos", ascending=False).head(50)
    
    output_path = PROCESSED_DIR / "anomalias_top.csv"
    anomalies.to_csv(output_path, index=False)
    print(f"✓ {output_path.name} ({len(anomalies)} anomalias detectadas)")


def main() -> int:
    """Execução principal."""
    print("=== EDA - Análise Exploratória de Dados ===\n")
    
    try:
        df = load_data()
        
        print("\nGerando artefatos:")
        generate_summary_stats(df)
        generate_general_stats(df)
        
        print("\nGerando figuras:")
        plot_series_by_bioma(df)
        plot_boxplot_by_bioma(df)
        plot_top_uf(df)
        
        print("\nDetectando anomalias:")
        detect_anomalies_simple(df)
        
        print("\n✓ EDA concluída com sucesso!")
        return 0
    
    except Exception as e:
        print(f"\n✗ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
