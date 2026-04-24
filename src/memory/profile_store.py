"""Long-term profile memory with conflict resolution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProfileStore:
	"""JSON file store for user profile facts."""

	def __init__(self, file_path: str) -> None:
		self.file_path = Path(file_path)
		self.file_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.file_path.exists():
			self.file_path.write_text("{}\n", encoding="utf-8")

	def _read(self) -> dict[str, dict[str, Any]]:
		raw = self.file_path.read_text(encoding="utf-8").strip() or "{}"
		data = json.loads(raw)
		if not isinstance(data, dict):
			return {}
		return data

	def _write(self, data: dict[str, dict[str, Any]]) -> None:
		self.file_path.write_text(
			json.dumps(data, ensure_ascii=False, indent=2) + "\n",
			encoding="utf-8",
		)

	def retrieve(self, query: str, user_id: str) -> dict[str, Any]:
		del query
		return self._read().get(user_id, {})

	def save(self, payload: Any, user_id: str) -> None:
		if not isinstance(payload, dict):
			return
		db = self._read()
		current = db.get(user_id, {})
		# Last-write-wins conflict strategy.
		for key, value in payload.items():
			if value is None:
				continue
			current[key] = value
		db[user_id] = current
		self._write(db)
