"""Semantic retrieval backend (vector or keyword fallback)."""

from __future__ import annotations

from pathlib import Path


def _tokenize(text: str) -> set[str]:
	return {tok.strip(".,:;!?()[]{}\"'").lower() for tok in text.split() if tok.strip()}


class SemanticStore:
	"""Simple semantic store using keyword overlap fallback."""

	def __init__(self, kb_path: str, top_k: int = 3) -> None:
		self.kb_path = Path(kb_path)
		self.top_k = top_k

	def _chunks(self) -> list[str]:
		if not self.kb_path.exists():
			return []
		text = self.kb_path.read_text(encoding="utf-8")
		blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
		return [b for b in blocks if not b.startswith("#")]

	def retrieve(self, query: str, user_id: str) -> list[str]:
		del user_id
		chunks = self._chunks()
		if not chunks:
			return []
		q = _tokenize(query)
		if not q:
			return chunks[: self.top_k]

		scored: list[tuple[int, str]] = []
		for chunk in chunks:
			score = len(q.intersection(_tokenize(chunk)))
			scored.append((score, chunk))
		scored.sort(key=lambda item: item[0], reverse=True)
		return [chunk for score, chunk in scored if score > 0][: self.top_k]

	def save(self, payload: object, user_id: str) -> None:
		del user_id
		if not isinstance(payload, str) or not payload.strip():
			return
		self.kb_path.parent.mkdir(parents=True, exist_ok=True)
		with self.kb_path.open("a", encoding="utf-8") as f:
			f.write("\n\n" + payload.strip() + "\n")
