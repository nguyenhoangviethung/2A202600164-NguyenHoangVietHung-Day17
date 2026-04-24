"""Base interfaces for memory backends."""

from typing import Protocol, Any


class MemoryBackend(Protocol):
    def retrieve(self, query: str, user_id: str) -> Any:
        ...

    def save(self, payload: Any, user_id: str) -> None:
        ...
