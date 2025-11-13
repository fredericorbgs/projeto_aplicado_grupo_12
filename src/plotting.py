from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def save_fig(fig, figures_dir: str, filename: str, dpi: int = 150) -> None:
    Path(figures_dir).mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(Path(figures_dir) / filename, dpi=dpi, bbox_inches="tight")


def plot_series_grouped(df: pd.DataFrame, date_col: str, count_col: str, group_col: str, figures_dir: str, fname: str):
    pivot = df.pivot_table(index=date_col, columns=group_col, values=count_col, aggfunc="sum").fillna(0)
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.rolling(7, min_periods=1).mean().plot(ax=ax, linewidth=1.6)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_title(f"Série temporal por {group_col} (média móvel 7d)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Contagem de focos")
    # legenda externa para não poluir a área do gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False)
    save_fig(fig, figures_dir, fname)


def plot_histograms(df: pd.DataFrame, columns: list[str], figures_dir: str, prefix: str = "hist"):
    for col in columns:
        if col in df.columns:
            fig, ax = plt.subplots(figsize=(6,4))
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"Distribuição de {col}")
            save_fig(fig, figures_dir, f"{prefix}_{col}.png")
            plt.close(fig)
