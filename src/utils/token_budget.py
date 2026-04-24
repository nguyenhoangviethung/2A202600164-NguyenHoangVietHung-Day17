"""Token/length budget helpers."""

from __future__ import annotations

from typing import Any


def estimate_tokens(text: str) -> int:
	"""Cheap token estimate for lab benchmarking."""
	if not text:
		return 0
	return max(1, len(text) // 4)


def trim_messages(messages: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
	if max_items <= 0:
		return []
	return messages[-max_items:]


def trim_list_by_budget(items: list[str], budget: int) -> list[str]:
	kept: list[str] = []
	used = 0
	for item in items:
		t = estimate_tokens(item)
		if used + t > budget:
			break
		kept.append(item)
		used += t
	return kept


def trim_sections_by_budget(sections: dict[str, str], budget: int) -> dict[str, str]:
	"""Keep sections in insertion order while respecting total budget."""
	kept: dict[str, str] = {}
	used = 0
	for key, content in sections.items():
		t = estimate_tokens(content)
		if used + t > budget:
			kept[key] = ""
			continue
		kept[key] = content
		used += t
	return kept
