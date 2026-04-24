"""Smoke tests for retrieval router and prompt injection."""

from pathlib import Path

from src.graph.nodes import build_prompt
from src.graph.router import retrieve_memory
from src.graph.state import MemoryState
from src.memory.episodic_store import EpisodicStore
from src.memory.manager import MemoryManager
from src.memory.profile_store import ProfileStore
from src.memory.semantic_store import SemanticStore
from src.memory.short_term import ShortTermMemory


def test_retrieve_memory_and_prompt_injection_sections() -> None:
	tmp = Path("tests/.tmp_retrieval")
	tmp.mkdir(parents=True, exist_ok=True)
	profile_path = tmp / "profile.json"
	episodic_path = tmp / "episodes.jsonl"
	kb_path = tmp / "kb.md"
	kb_path.write_text(
		"LangGraph router combines memory backends.\n\n"
		"Conflict handling updates allergies to newest value.",
		encoding="utf-8",
	)

	manager = MemoryManager(
		short_term=ShortTermMemory(window_size=8),
		profile=ProfileStore(str(profile_path)),
		episodic=EpisodicStore(str(episodic_path)),
		semantic=SemanticStore(str(kb_path), top_k=2),
	)
	manager.profile.save({"name": "Linh", "allergies": "dau nanh"}, user_id="u1")
	manager.episodic.save(
		{
			"summary": "Completed benchmark comparison for no-memory and with-memory.",
			"tags": ["benchmark"],
			"outcome": "completed",
		},
		user_id="u1",
	)

	state: MemoryState = {
		"user_id": "u1",
		"query": "how does conflict handling work in memory router",
		"messages": [
			{"role": "user", "content": "please explain memory router"},
			{"role": "assistant", "content": "ok"},
		],
		"memory_budget": 1200,
		"memory_manager": manager,
	}
	routed = retrieve_memory(state)
	prompt = build_prompt(routed)

	assert routed["user_profile"].get("name") == "Linh"
	assert len(routed["episodes"]) >= 1
	assert len(routed["semantic_hits"]) >= 1
	assert "[USER_PROFILE]" in prompt
	assert "[EPISODIC_MEMORIES]" in prompt
	assert "[SEMANTIC_HITS]" in prompt
	assert "[RECENT_CONVERSATION]" in prompt


def test_prompt_budget_trimming_keeps_structure() -> None:
	tmp = Path("tests/.tmp_retrieval")
	tmp.mkdir(parents=True, exist_ok=True)
	profile_path = tmp / "profile_2.json"
	episodic_path = tmp / "episodes_2.jsonl"
	kb_path = tmp / "kb_2.md"
	kb_path.write_text("very long chunk " * 200, encoding="utf-8")

	manager = MemoryManager(
		short_term=ShortTermMemory(window_size=8),
		profile=ProfileStore(str(profile_path)),
		episodic=EpisodicStore(str(episodic_path)),
		semantic=SemanticStore(str(kb_path), top_k=3),
	)

	state: MemoryState = {
		"user_id": "u2",
		"query": "long semantic query",
		"messages": [{"role": "user", "content": "test"}],
		"memory_budget": 40,
		"memory_manager": manager,
	}
	routed = retrieve_memory(state)
	prompt = build_prompt(routed)

	assert "[USER_PROFILE]" in prompt
	assert "[SEMANTIC_HITS]" in prompt
	assert len(prompt) > 0
