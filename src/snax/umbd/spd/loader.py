from pathlib import Path


import pandas as pd

filepath = Path(__file__).parent / "data" / "speed_dating.csv"


def load_dataset():
    """Load the speed dating dataset from a CSV file.

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    return pd.read_csv(filepath, sep=",", encoding="latin1")
