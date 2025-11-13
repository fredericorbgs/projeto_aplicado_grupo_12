from __future__ import annotations
import os
import glob
from typing import List
import pandas as pd


def list_processed_files(base_dir: str) -> List[str]:
    pattern = os.path.join(base_dir, "data", "processed", "*.csv")
    return sorted(glob.glob(pattern))


def read_processed_concat(base_dir: str) -> pd.DataFrame:
    files = list_processed_files(base_dir)
    if not files:
        raise FileNotFoundError("No CSV files found in data/processed.")
    frames = []
    for path in files:
        try:
            df = pd.read_csv(path, encoding="utf-8", low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding="latin1", low_memory=False)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
