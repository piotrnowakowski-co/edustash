from functools import lru_cache, partial
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


@lru_cache(maxsize=1)
def load_pandas(*, name: str, ext: str = "csv", **kwargs):
    target = DATA_DIR / f"{name}.{ext}"
    return pd.read_csv(target.as_posix(), **kwargs)


load_speed_dating = partial(load, name="speed_dating", sep=",", encoding="latin1")
load_titanic = partial(load, name="titanic")
load_births = partial(load, name="births")
load_listings_summary = partial(load, name="listings_summary")
