"""
Módulo de download/ingestão do dataset escolhido.
Preencha com a lógica de download, leitura e salvamento em data/raw ou data/processed.
"""

from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def download_dataset():
    """
    Baixe/ingira o dataset e salve em RAW_DIR.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    # TODO: implementar lógica de download/ingestão
    return RAW_DIR


if __name__ == "__main__":
    path = download_dataset()
    print(f"Dados disponíveis em: {path}")
