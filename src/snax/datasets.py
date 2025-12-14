from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


@lru_cache(maxsize=1)
def load_pandas(*, name: str, ext: str = "csv", **kwargs):
    target = DATA_DIR / f"{name}.{ext}"
    return pd.read_csv(target.as_posix(), **kwargs)
