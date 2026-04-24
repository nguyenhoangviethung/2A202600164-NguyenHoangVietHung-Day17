"""Memory retrieval router."""

from src.memory.manager import MemoryManager

from .state import MemoryState


def retrieve_memory(state: MemoryState) -> MemoryState:
    """Fan-out retrieval to profile/episodic/semantic/short-term backends."""
    manager = state.get("memory_manager")
    if not isinstance(manager, MemoryManager):
        raise ValueError("state['memory_manager'] must be a MemoryManager instance")

    user_id = str(state.get("user_id", "default_user"))
    query = str(state.get("query", "")).strip()
    if not query:
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if msg.get("role") == "user":
                query = str(msg.get("content", ""))
                break

    retrieved = manager.retrieve_all(query=query, user_id=user_id)
    state["user_profile"] = retrieved.get("user_profile", {})
    state["episodes"] = retrieved.get("episodes", [])
    state["semantic_hits"] = retrieved.get("semantic_hits", [])

    if not state.get("messages"):
        state["messages"] = retrieved.get("recent_messages", [])

    return state
