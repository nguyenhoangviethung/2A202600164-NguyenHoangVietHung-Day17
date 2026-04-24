"""Short-term memory implementation (window/buffer)."""

from collections import defaultdict
from typing import Any


class ShortTermMemory:
	"""In-memory sliding window buffer per user."""

	def __init__(self, window_size: int = 8) -> None:
		self.window_size = window_size
		self._store: dict[str, list[dict[str, Any]]] = defaultdict(list)

	def add_message(self, user_id: str, role: str, content: str) -> None:
		self._store[user_id].append({"role": role, "content": content})
		self._store[user_id] = self._store[user_id][-self.window_size :]

	def set_messages(self, user_id: str, messages: list[dict[str, Any]]) -> None:
		self._store[user_id] = messages[-self.window_size :]

	def retrieve(self, query: str, user_id: str) -> list[dict[str, Any]]:
		del query
		return list(self._store.get(user_id, []))

	def save(self, payload: Any, user_id: str) -> None:
		if isinstance(payload, list):
			self.set_messages(user_id=user_id, messages=payload)
