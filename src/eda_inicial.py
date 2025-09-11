"""
EDA inicial — Focos de Queimadas (2019–2024)

Este script reproduz a análise básica do notebook `notebooks/EDA_inicial.ipynb`:
- Carrega e concatena CSVs de `data/raw/`
- Normaliza datas e alguns campos de texto
- Gera contagens por dia e agregações por bioma/UF (se existirem as colunas)
- Plota gráficos simples
- Exporta artefatos em `data/processed/`

Uso:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python src/eda_inicial.py

Requisitos: pandas, numpy, matplotlib, seaborn
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações globais
pd.set_option("display.max_columns", 100)
sns.set(style="whitegrid", context="notebook")

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DIR: Path = DATA_DIR / "raw"
PROCESSED_DIR: Path = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def list_csv_files(directory: Path) -> list[Path]:
    csv_files = sorted(directory.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {directory}. Coloque arquivos .csv no diretório e reexecute."
        )
    return csv_files


def read_csv_with_fallback(file_path: Path, usecols: Optional[Iterable[str]] = None) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, encoding="utf-8", sep=",", usecols=usecols, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="latin1", sep=",", usecols=usecols, low_memory=False)


def concatenate_csv_files(csv_files: Iterable[Path], usecols: Optional[Iterable[str]] = None) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for file_path in csv_files:
        df = read_csv_with_fallback(file_path, usecols=usecols)
        df["_source_file"] = file_path.name
        frames.append(df)
    if not frames:
        raise RuntimeError("Nenhum DataFrame carregado. Verifique os arquivos de entrada.")
    return pd.concat(frames, ignore_index=True)


def build_lower_to_original_map(columns: Iterable[str]) -> Dict[str, str]:
    return {column.lower(): column for column in columns}


def resolve_first_present_column(lower_to_original: Dict[str, str], candidates: Iterable[str]) -> Optional[str]:
    for candidate in candidates:
        if candidate in lower_to_original:
            return lower_to_original[candidate]
    return None


def normalize_and_derive_columns(raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Optional[str]]]:
    lower_to_original = build_lower_to_original_map(raw.columns)
    date_col = resolve_first_present_column(lower_to_original, ["data_pas", "data", "dt", "datetime"])  # type: ignore[arg-type]
    bioma_col = resolve_first_present_column(lower_to_original, ["bioma"])  # type: ignore[arg-type]
    uf_col = resolve_first_present_column(lower_to_original, ["estado", "uf"])  # type: ignore[arg-type]
    muni_col = resolve_first_present_column(lower_to_original, ["municipio", "município", "munic"])  # type: ignore[arg-type]

    if date_col is None:
        raise KeyError("Não encontrei coluna de data (ex.: data_pas). Atualize o mapeamento.")

    raw = raw.copy()
    raw["date"] = pd.to_datetime(raw[date_col], errors="coerce")
    if raw["date"].isna().all():
        raise ValueError("Falha ao converter datas. Verifique o formato em data_pas.")

    for text_col in [bioma_col, uf_col, muni_col]:
        if text_col and text_col in raw.columns:
            raw[text_col] = raw[text_col].astype(str).str.strip()

    raw["year"] = raw["date"].dt.year
    raw["month"] = raw["date"].dt.to_period("M").astype(str)
    raw["day"] = raw["date"].dt.date

    column_map = {
        "date": date_col,
        "bioma": bioma_col,
        "uf": uf_col,
        "municipio": muni_col,
    }
    return raw, column_map


def summarize_and_plot(raw: pd.DataFrame, column_map: Dict[str, Optional[str]]) -> None:
    print("Linhas:", len(raw))
    print("Colunas:", raw.shape[1])
    print("Período:", raw["date"].min(), "->", raw["date"].max())

    by_day = raw.groupby("day").size().rename("focos").reset_index()
    by_day.to_csv(PROCESSED_DIR / "focos_por_dia.csv", index=False)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(by_day["day"], by_day["focos"], color="tab:red", linewidth=1)
    ax.set_title("Focos por dia (total)")
    ax.set_xlabel("Dia")
    ax.set_ylabel("Focos")
    plt.tight_layout()
    plt.show()

    bioma_col = column_map.get("bioma")
    if bioma_col and bioma_col in raw.columns:
        by_bioma = raw.groupby([bioma_col, "month"]).size().rename("focos").reset_index()
        pivot_bioma = by_bioma.pivot(index="month", columns=bioma_col, values="focos").fillna(0)
        pivot_bioma.to_csv(PROCESSED_DIR / "focos_mes_bioma.csv")

        fig, ax = plt.subplots(figsize=(12, 5))
        pivot_bioma.plot(ax=ax)
        ax.set_title("Focos por mês e bioma")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Focos")
        plt.tight_layout()
        plt.show()

    uf_col = column_map.get("uf")
    if uf_col and uf_col in raw.columns:
        by_uf = raw.groupby([uf_col, "month"]).size().rename("focos").reset_index()
        pivot_uf = by_uf.pivot(index="month", columns=uf_col, values="focos").fillna(0)
        pivot_uf.to_csv(PROCESSED_DIR / "focos_mes_uf.csv")

        fig, ax = plt.subplots(figsize=(12, 5))
        pivot_uf.plot(ax=ax)
        ax.set_title("Focos por mês e UF")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Focos")
        plt.tight_layout()
        plt.show()


def main() -> int:
    print("Project root:", PROJECT_ROOT)
    print("Raw dir:", RAW_DIR)
    print("Processed dir:", PROCESSED_DIR)

    csv_files = list_csv_files(RAW_DIR)
    raw = concatenate_csv_files(csv_files, usecols=None)
    raw, column_map = normalize_and_derive_columns(raw)
    summarize_and_plot(raw, column_map)

    print("Arquivos exportados em:", PROCESSED_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
