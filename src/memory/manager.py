"""Compose all memory backends into one manager API."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.utils.extractors import extract_episode_from_messages, extract_profile_facts

from .episodic_store import EpisodicStore
from .profile_store import ProfileStore
from .semantic_store import SemanticStore
from .short_term import ShortTermMemory


class MemoryManager:
	"""Aggregates all memory systems behind one API."""

	def __init__(
		self,
		short_term: ShortTermMemory,
		profile: ProfileStore,
		episodic: EpisodicStore,
		semantic: SemanticStore,
	) -> None:
		self.short_term = short_term
		self.profile = profile
		self.episodic = episodic
		self.semantic = semantic

	def retrieve_all(self, query: str, user_id: str) -> dict[str, Any]:
		return {
			"recent_messages": self.short_term.retrieve(query=query, user_id=user_id),
			"user_profile": self.profile.retrieve(query=query, user_id=user_id),
			"episodes": self.episodic.retrieve(query=query, user_id=user_id),
			"semantic_hits": self.semantic.retrieve(query=query, user_id=user_id),
		}

	def save_all(self, messages: list[dict[str, Any]], user_id: str) -> dict[str, Any]:
		# Keep short-term window updated every turn.
		self.short_term.save(messages, user_id=user_id)

		if messages:
			latest_user = next(
				(m for m in reversed(messages) if m.get("role") == "user"),
				None,
			)
			if latest_user:
				facts = extract_profile_facts(str(latest_user.get("content", "")))
				if facts:
					self.profile.save(facts, user_id=user_id)

		episode = extract_episode_from_messages(messages)
		if episode:
			episode.setdefault("timestamp", datetime.now(tz=timezone.utc).isoformat())
			self.episodic.save(episode, user_id=user_id)

		return {
			"user_profile": self.profile.retrieve(query="", user_id=user_id),
			"episodes": self.episodic.retrieve(query="", user_id=user_id),
		}
