"""Required test: profile conflict update behavior."""

from pathlib import Path

from src.graph.nodes import save_memories
from src.graph.state import MemoryState
from src.memory.episodic_store import EpisodicStore
from src.memory.manager import MemoryManager
from src.memory.profile_store import ProfileStore
from src.memory.semantic_store import SemanticStore
from src.memory.short_term import ShortTermMemory


def test_allergy_conflict_resolution() -> None:
    tmp = Path("tests/.tmp_conflict")
    tmp.mkdir(parents=True, exist_ok=True)
    profile_path = tmp / "profile.json"
    episodic_path = tmp / "episodes.jsonl"
    kb_path = tmp / "kb.md"
    kb_path.write_text("allergy facts\n", encoding="utf-8")

    manager = MemoryManager(
        short_term=ShortTermMemory(window_size=8),
        profile=ProfileStore(str(profile_path)),
        episodic=EpisodicStore(str(episodic_path)),
        semantic=SemanticStore(str(kb_path)),
    )

    state1: MemoryState = {
        "user_id": "user_test",
        "messages": [
            {"role": "user", "content": "Toi di ung sua bo."},
            {"role": "assistant", "content": "Da ghi nhan."},
        ],
        "memory_manager": manager,
    }
    save_memories(state1)

    state2: MemoryState = {
        "user_id": "user_test",
        "messages": [
            {"role": "user", "content": "A nham, toi di ung dau nanh chu khong phai sua bo."},
            {"role": "assistant", "content": "Da cap nhat thong tin."},
        ],
        "memory_manager": manager,
    }
    updated = save_memories(state2)

    assert updated["user_profile"].get("allergies") == "dau nanh"
