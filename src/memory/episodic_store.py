"""Episodic memory store for task outcomes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _tokenize(text: str) -> set[str]:
	return {tok.strip(".,:;!?()[]{}\"'").lower() for tok in text.split() if tok.strip()}


class EpisodicStore:
	"""JSONL store where each line is one episode entry."""

	def __init__(self, file_path: str, max_return: int = 5) -> None:
		self.file_path = Path(file_path)
		self.file_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.file_path.exists():
			self.file_path.write_text("", encoding="utf-8")
		self.max_return = max_return

	def _read_all(self) -> list[dict[str, Any]]:
		episodes: list[dict[str, Any]] = []
		for line in self.file_path.read_text(encoding="utf-8").splitlines():
			line = line.strip()
			if not line:
				continue
			try:
				row = json.loads(line)
			except json.JSONDecodeError:
				continue
			if isinstance(row, dict):
				episodes.append(row)
		return episodes

	def retrieve(self, query: str, user_id: str) -> list[dict[str, Any]]:
		rows = [row for row in self._read_all() if row.get("user_id") == user_id]
		if not rows:
			return []
		q = _tokenize(query)
		if not q:
			return rows[-self.max_return :]

		scored: list[tuple[int, dict[str, Any]]] = []
		for row in rows:
			text = f"{row.get('summary', '')} {' '.join(row.get('tags', []))}"
			score = len(q.intersection(_tokenize(text)))
			scored.append((score, row))
		scored.sort(key=lambda item: item[0], reverse=True)
		best = [row for score, row in scored if score > 0]
		return (best or rows)[-self.max_return :]

	def save(self, payload: Any, user_id: str) -> None:
		if not isinstance(payload, dict):
			return
		summary = str(payload.get("summary", "")).strip()
		outcome = str(payload.get("outcome", "")).strip()
		if not summary or not outcome:
			return

		record = dict(payload)
		record["user_id"] = user_id
		with self.file_path.open("a", encoding="utf-8") as f:
			f.write(json.dumps(record, ensure_ascii=False) + "\n")
