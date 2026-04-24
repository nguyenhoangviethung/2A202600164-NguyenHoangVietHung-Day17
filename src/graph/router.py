"""Memory retrieval router."""

from .state import MemoryState


def retrieve_memory(state: MemoryState) -> MemoryState:
    """TODO: fan-out retrieval to profile/episodic/semantic + trim by budget."""
    raise NotImplementedError
