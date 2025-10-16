"""
Pipeline de Ingestão e Consolidação - Focos de Queimadas (2019-2024)

Este script:
- Carrega CSVs anuais de data/raw/queimadas/
- Normaliza encoding (UTF-8/latin1 fallback)
- Limpa e padroniza colunas (estado, município, bioma, datas)
- Valida coordenadas geográficas
- Gera campos derivados (dia, semana, mês, ano)
- Exporta para Parquet consolidado em data/processed/

Uso:
    python -m src.pipeline_ingestao
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

# Configurações
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw" / "queimadas"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Validações para território brasileiro (aproximado)
LAT_MIN, LAT_MAX = -33.8, 5.3
LON_MIN, LON_MAX = -74.1, -32.4


def read_csv_with_fallback(file_path: Path) -> pd.DataFrame:
    """Lê CSV com fallback de encoding (UTF-8 -> latin1)."""
    try:
        df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
        print(f"  ✓ {file_path.name} (UTF-8)")
        return df
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1", low_memory=False)
        print(f"  ✓ {file_path.name} (latin1 fallback)")
        return df


def load_and_concatenate() -> pd.DataFrame:
    """Carrega todos os CSVs de RAW_DIR e concatena."""
    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {RAW_DIR}. "
            "Coloque os arquivos focos_ams_ref_YYYY.csv e reexecute."
        )
    
    print(f"Carregando {len(csv_files)} arquivo(s):")
    frames = []
    for path in csv_files:
        df = read_csv_with_fallback(path)
        df["_source_file"] = path.name
        frames.append(df)
    
    raw = pd.concat(frames, ignore_index=True)
    print(f"Total de linhas: {len(raw):,}")
    return raw


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nomes de colunas (lowercase, sem espaços)."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def find_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """Retorna a primeira coluna que existe entre as candidatas."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


def clean_and_standardize(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e padroniza campos principais."""
    # Identificar colunas
    date_col = find_column(df, ["data_pas", "data", "dt", "datetime"])
    lat_col = find_column(df, ["lat", "latitude"])
    lon_col = find_column(df, ["lon", "longitude"])
    estado_col = find_column(df, ["estado", "uf"])
    municipio_col = find_column(df, ["municipio", "município", "munic"])
    bioma_col = find_column(df, ["bioma"])
    
    if not date_col:
        raise ValueError("Coluna de data não encontrada (ex.: data_pas)")
    
    # Converter data
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    invalid_dates = df["date"].isna().sum()
    if invalid_dates > 0:
        print(f"  ⚠ {invalid_dates:,} datas inválidas removidas")
        df = df[df["date"].notna()].copy()
    
    # Validar coordenadas (se existirem)
    if lat_col and lon_col:
        df["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
        df["lon"] = pd.to_numeric(df[lon_col], errors="coerce")
        
        invalid_coords = (
            (df["lat"] < LAT_MIN) | (df["lat"] > LAT_MAX) |
            (df["lon"] < LON_MIN) | (df["lon"] > LON_MAX)
        )
        n_invalid = invalid_coords.sum()
        if n_invalid > 0:
            print(f"  ⚠ {n_invalid:,} coordenadas fora do território BR removidas")
            df = df[~invalid_coords].copy()
    
    # Padronizar campos de texto
    for col in [estado_col, municipio_col, bioma_col]:
        if col and col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # Campos derivados
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["week_iso"] = df["date"].dt.isocalendar().week
    df["day"] = df["date"].dt.date
    
    # Chave composta (opcional)
    if bioma_col and estado_col:
        df["bioma_uf"] = df[bioma_col] + "_" + df[estado_col]
    
    print(f"Linhas após limpeza: {len(df):,}")
    return df


def export_parquet(df: pd.DataFrame) -> None:
    """Exporta para Parquet com compressão."""
    output_path = PROCESSED_DIR / "focos_2019_2024.parquet"
    df.to_parquet(output_path, engine="pyarrow", compression="snappy", index=False)
    print(f"Exportado: {output_path}")
    print(f"  Tamanho: {output_path.stat().st_size / 1024**2:.1f} MB")


def main() -> int:
    """Execução principal."""
    print("=== Pipeline de Ingestão - Focos de Queimadas ===\n")
    
    try:
        raw = load_and_concatenate()
        raw = normalize_columns(raw)
        clean = clean_and_standardize(raw)
        export_parquet(clean)
        
        print("\n✓ Pipeline concluído com sucesso!")
        return 0
    
    except Exception as e:
        print(f"\n✗ Erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
