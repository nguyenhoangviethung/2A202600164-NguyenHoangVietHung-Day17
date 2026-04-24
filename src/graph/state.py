"""Shared state for memory-enabled agent graph."""

from typing import TypedDict, Any


class MemoryState(TypedDict, total=False):
    messages: list[dict[str, Any]]
    user_profile: dict[str, Any]
    episodes: list[dict[str, Any]]
    semantic_hits: list[str]
    memory_budget: int
