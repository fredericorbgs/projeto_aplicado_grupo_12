from __future__ import annotations
import pandas as pd
from unidecode import unidecode


def normalize_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .map(lambda x: unidecode(x).strip() if x is not None else x)
            )
    return df


def parse_datetime(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        df["ano"] = df[col].dt.year
        df["mes"] = df[col].dt.month
        df["dia"] = df[col].dt.day
        df["dia_da_semana"] = df[col].dt.dayofweek
        df["data"] = df[col].dt.date
    return df


def validate_coordinates(df: pd.DataFrame, lat_col: str = "lat", lon_col: str = "lon") -> pd.DataFrame:
    if lat_col in df.columns and lon_col in df.columns:
        df = df[(df[lat_col].between(-90, 90)) & (df[lon_col].between(-180, 180))]
    return df
