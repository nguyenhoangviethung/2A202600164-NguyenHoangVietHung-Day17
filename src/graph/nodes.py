"""Graph nodes for retrieval, prompting, generation, and persistence."""

from .state import MemoryState


def build_prompt(state: MemoryState) -> str:
    """TODO: inject profile, episodic, semantic, and recent conversation sections."""
    raise NotImplementedError


def save_memories(state: MemoryState) -> MemoryState:
    """TODO: extract facts/outcomes and update memory stores."""
    raise NotImplementedError
