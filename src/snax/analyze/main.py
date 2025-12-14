from abc import ABC, abstractmethod
from functools import wraps

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger


class Component:
    is_procesed: bool = False
    __slots__ = (
        "key",
        "series",
        "is_categorical",
        "is_numerical",
        "unique",
        "nunique",
        "min",
        "max",
        "mean",
        "median",
        "null_count",
        "non_null_count",
        "value_counts",
    )

    def __init__(self, key: str, series):
        self.key = key
        self.series = series
        self.is_categorical = (
            series.dtype == "object" or series.dtype.name == "category"
        )
        self.is_numerical = pd.api.types.is_numeric_dtype(series)
        self.unique = None
        self.nunique = None
        self.min = None
        self.max = None
        self.mean = None
        self.median = None
        self.null_count = None
        self.non_null_count = None
        self.value_counts = None

    def __repr__(self):
        return f"Component(key={self.key!r}, is_numerical={self.is_numerical}, is_categorical={self.is_categorical})"

    def quantiles(self, q=[0.25, 0.5, 0.75]):
        if self.is_numerical:
            return self.series.quantile(q)
        else:
            raise ValueError("Quantiles can only be computed for numerical components.")

    def to_dict(self):
        return {
            "key": self.key,
            "is_numerical": self.is_numerical,
            "is_categorical": self.is_categorical,
            "unique": self.unique,
            "nunique": self.nunique,
            "min": self.min,
            "max": self.max,
            "mean": self.mean,
            "median": self.median,
            "null_count": self.null_count,
            "non_null_count": self.non_null_count,
            "value_counts": (
                self.value_counts.to_dict() if self.value_counts is not None else None
            ),
        }

    def process(self):
        if self.is_procesed:
            logger.debug(f"Component {self.key} already processed.")
            return
        self.unique = self.series.nunique(dropna=True)
        self.null_count = self.series.isnull().sum()
        self.non_null_count = self.series.notnull().sum()

        if self.is_numerical:
            self.min = self.series.min()
            self.max = self.series.max()
            self.mean = self.series.mean()
            self.median = self.series.median()
            self.nunique = self.series.nunique(dropna=True)

        if self.is_categorical:
            self.value_counts = self.series.value_counts(dropna=True)

    def hist(self, bins=10):
        if self.is_numerical:
            sns.histplot(self.series.dropna(), bins=bins)
        elif self.is_categorical:
            sns.countplot(y=self.series.dropna())

    def sample(self, n=5):
        return self.series.sample(n)

    def boxplot(self):
        if self.is_numerical:
            sns.boxplot(x=self.series.dropna())


class ComponentContainer:
    def __init__(self):
        self.components: dict[str, Component] = {}

    def __getattr__(self, item):
        val = self.components.get(item)
        if val is None:
            raise AttributeError(f"No component '{item}' found.")
        return val

    def add_component(self, component: Component):
        self.components[component.key] = component

    def get_component(self, key: str) -> Component:
        return self.components.get(key)

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        return iter(self.components.items())

    def fragment(self, keys: list[str]):
        fragment = ComponentContainer()
        for key in keys:
            if key in self.components:
                fragment.add_component(self.components[key])
        return fragment

    def to_list(self):
        return list(self.components.values())

    def to_pandas(self):
        data = [comp.to_dict() for comp in self.components.values()]
        return pd.DataFrame(data)


def mutated(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        logger.info(f"Method {method.__name__} returns new DataExplorer instance.")
        result = method(self, *args, **kwargs)

        return DataFrameExplorer(result).analyze()

    return wrapper


class BaseExplorer(ABC):
    @abstractmethod
    def analyze(self) -> "BaseExplorer":
        pass


class PlottingMixin:
    components: ComponentContainer

    def histgrid(self, bins=10, numerical_only: bool = False):
        n_components = len(self.components)
        n_cols = 3
        n_rows = (n_components + n_cols - 1) // n_cols
        _, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        axes = axes.flatten()
        for i, (key, component) in enumerate(self.components):
            if numerical_only and not component.is_numerical:
                continue
            plt.sca(axes[i])
            component.hist(bins=bins)
            plt.title(f"Histogram of {key}")
        plt.tight_layout()
        plt.show()

    def boxgrid(self, numerical_only: bool = False):
        n_components = len(self.components)
        n_cols = 3
        n_rows = (n_components + n_cols - 1) // n_cols
        _, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        axes = axes.flatten()
        for i, (key, component) in enumerate(self.components):
            if numerical_only and not component.is_numerical:
                continue
            plt.sca(axes[i])
            component.boxplot()
            plt.title(f"Boxplot of {key}")
        plt.tight_layout()
        plt.show()


class DataFrameExplorer(PlottingMixin, BaseExplorer):
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.components: ComponentContainer = ComponentContainer()
        self.c = self.components  # shortcut

    @property
    def numerical(self):
        return self.components.fragment(
            [key for key, comp in self.components if comp.is_numerical]
        )

    @property
    def categorical(self):
        return self.components.fragment(
            [key for key, comp in self.components if comp.is_categorical]
        )

    def sample(self, n: int = 5):
        return self.data.sample(n)

    @mutated
    def dropna(self, threshold: float = 0.5):
        thresh_count = int(len(self.data) * threshold)
        return self.data.dropna(axis=1, thresh=thresh_count)

    def analyze(self):
        for column in self.data.columns:
            component = Component(column, self.data[column])
            component.process()
            self.components.add_component(component)
        return self


def analyze(data):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")
    return DataFrameExplorer(data).analyze()
