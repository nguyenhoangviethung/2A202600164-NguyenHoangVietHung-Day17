"""Fact and episode extraction helpers."""

from __future__ import annotations

import re
from typing import Any


def _normalize(text: str) -> str:
	return " ".join(text.strip().split()).lower()


def extract_profile_facts(user_text: str) -> dict[str, str]:
	text = _normalize(user_text)
	facts: dict[str, str] = {}

	def clean_value(value: str) -> str:
		value = value.strip(" .,!?")
		for separator in [" chu khong phai ", " khong phai ", " thay cho ", " thay vi "]:
			if separator in value:
				value = value.split(separator, 1)[0].strip()
		return value

	name_match = re.search(r"(?:toi la|ten toi la|my name is)\s+([\w\s]+)", text)
	if name_match:
		facts["name"] = name_match.group(1).strip(" .,!?")

	allergy_match = re.search(r"di ung\s+([\w\s]+)", text)
	if allergy_match:
		facts["allergies"] = clean_value(allergy_match.group(1))

	correction_match = re.search(
		r"(?:a nham|nham|sua lai|correction).*?di ung\s+([\w\s]+)",
		text,
	)
	if correction_match:
		facts["allergies"] = clean_value(correction_match.group(1))

	drink_match = re.search(r"(?:thich uong|favorite drink is)\s+([\w\s]+)", text)
	if drink_match:
		facts["favorite_drink"] = drink_match.group(1).strip(" .,!?")

	language_match = re.search(r"(?:noi|speak)\s+([\w\s]+)", text)
	if language_match and "tieng" in language_match.group(1):
		facts["preferred_language"] = language_match.group(1).strip(" .,!?")

	return facts


def extract_episode_from_messages(messages: list[dict[str, Any]]) -> dict[str, Any] | None:
	if len(messages) < 2:
		return None

	latest_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
	latest_assistant = next(
		(m for m in reversed(messages) if m.get("role") == "assistant"),
		None,
	)
	if not latest_user or not latest_assistant:
		return None

	assistant_text = str(latest_assistant.get("content", "")).strip().lower()
	outcome = "completed" if any(
		marker in assistant_text
		for marker in ["done", "completed", "xong", "hoan tat", "da tao"]
	) else "noted"

	return {
		"summary": (
			f"User asked: {latest_user.get('content', '')}. "
			f"Assistant replied: {latest_assistant.get('content', '')}"
		)[:500],
		"tags": ["conversation", "lab17"],
		"outcome": outcome,
	}
