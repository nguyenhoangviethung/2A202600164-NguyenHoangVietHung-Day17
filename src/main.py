"""Entry point for Lab 17 agent."""

from __future__ import annotations

from pathlib import Path

from src.graph.nodes import build_prompt, save_memories
from src.graph.router import retrieve_memory
from src.graph.state import MemoryState
from src.memory.episodic_store import EpisodicStore
from src.memory.manager import MemoryManager
from src.memory.profile_store import ProfileStore
from src.memory.semantic_store import SemanticStore
from src.memory.short_term import ShortTermMemory


def _parse_simple_yaml(path: str) -> dict[str, str]:
    """Parse key: value lines from a simple YAML file."""
    result: dict[str, str] = {}
    file_path = Path(path)
    if not file_path.exists():
        return result

    for raw in file_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def _build_manager() -> tuple[MemoryManager, dict[str, str]]:
    cfg = _parse_simple_yaml("configs/settings.yaml")
    short_term = ShortTermMemory(window_size=int(cfg.get("window_size", "8")))
    profile = ProfileStore("data/profile/profile.json")
    episodic = EpisodicStore("data/episodic/episodes.jsonl")
    semantic = SemanticStore(
        kb_path="data/semantic/knowledge_base.md",
        top_k=int(cfg.get("semantic_top_k", "3")),
    )
    return MemoryManager(short_term, profile, episodic, semantic), cfg


def _generate_response(state: MemoryState) -> str:
    profile = state.get("user_profile", {})
    hits = state.get("semantic_hits", [])
    episodes = state.get("episodes", [])
    latest_user = next(
        (m.get("content", "") for m in reversed(state.get("messages", [])) if m.get("role") == "user"),
        "",
    )
    return (
        f"Mình đã ghi nhận yêu cầu: {latest_user}\n"
        f"Profile facts: {len(profile)} | Episodes: {len(episodes)} | Semantic hits: {len(hits)}."
    )


def main() -> None:
    manager, cfg = _build_manager()
    user_id = "user_123"
    messages: list[dict[str, str]] = []

    print("Lab17 Multi-Memory Agent (type 'exit' to quit)")
    while True:
        try:
            user_input = input("User> ").strip()
        except EOFError:
            print("Bye")
            break
        except KeyboardInterrupt:
            print("Bye")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("Bye")
            break

        messages.append({"role": "user", "content": user_input})

        state: MemoryState = {
            "user_id": user_id,
            "query": user_input,
            "messages": messages,
            "memory_budget": int(cfg.get("memory_budget", "1200")),
            "memory_manager": manager,
        }

        state = retrieve_memory(state)
        _ = build_prompt(state)

        reply = _generate_response(state)
        print(f"Assistant> {reply}")
        messages.append({"role": "assistant", "content": reply})

        state["messages"] = messages
        save_memories(state)


if __name__ == "__main__":
    main()
