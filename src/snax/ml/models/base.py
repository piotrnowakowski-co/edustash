from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ModelProtocol(Protocol):
    def fit(self, X: Any, y: Any) -> None: ...

    def predict(self, X: Any) -> Any: ...
