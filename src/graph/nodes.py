"""Graph nodes for retrieval, prompting, generation, and persistence."""

import json

from src.memory.manager import MemoryManager
from src.utils.token_budget import trim_messages, trim_sections_by_budget

from .state import MemoryState


def build_prompt(state: MemoryState) -> str:
    """Inject profile, episodic, semantic, and recent conversation sections."""
    user_profile = state.get("user_profile", {})
    episodes = state.get("episodes", [])
    semantic_hits = state.get("semantic_hits", [])
    messages = state.get("messages", [])
    manager = state.get("memory_manager")
    window_size = 8
    if isinstance(manager, MemoryManager):
        window_size = manager.short_term.window_size
    recent_messages = trim_messages(messages, window_size)

    sections = {
        "USER_PROFILE": json.dumps(user_profile, ensure_ascii=False, indent=2)
        if user_profile
        else "(none)",
        "EPISODIC_MEMORIES": "\n".join(
            [f"- {ep.get('summary', '')}" for ep in episodes]
        )
        or "(none)",
        "SEMANTIC_HITS": "\n".join([f"- {hit}" for hit in semantic_hits]) or "(none)",
        "RECENT_CONVERSATION": "\n".join(
            [f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in recent_messages]
        )
        or "(none)",
    }

    budget = int(state.get("memory_budget", 1200))
    trimmed = trim_sections_by_budget(sections, budget=budget)

    prompt = (
        "[USER_PROFILE]\n"
        f"{trimmed['USER_PROFILE']}\n\n"
        "[EPISODIC_MEMORIES]\n"
        f"{trimmed['EPISODIC_MEMORIES']}\n\n"
        "[SEMANTIC_HITS]\n"
        f"{trimmed['SEMANTIC_HITS']}\n\n"
        "[RECENT_CONVERSATION]\n"
        f"{trimmed['RECENT_CONVERSATION']}\n\n"
        "[INSTRUCTIONS]\n"
        "Answer with best effort using these memory sections."
    )
    state["prompt"] = prompt
    return prompt


def save_memories(state: MemoryState) -> MemoryState:
    """Extract/save profile facts and episodic summaries."""
    manager = state.get("memory_manager")
    if not isinstance(manager, MemoryManager):
        raise ValueError("state['memory_manager'] must be a MemoryManager instance")

    user_id = str(state.get("user_id", "default_user"))
    messages = state.get("messages", [])
    saved = manager.save_all(messages=messages, user_id=user_id)

    state["user_profile"] = saved.get("user_profile", state.get("user_profile", {}))
    state["episodes"] = saved.get("episodes", state.get("episodes", []))
    return state
