# 2A202600164-NguyenHoangVietHung-Day17

## Lab 17 - Multi-Memory Agent

### Mục tiêu

Dự án triển khai agent với full memory stack theo rubric:
- Short-term memory: sliding window conversation buffer.
- Long-term profile memory: JSON profile store.
- Episodic memory: JSONL log store cho outcome theo session.
- Semantic memory: keyword-based retrieval trên knowledge base (fallback cho vector DB).

Agent có flow tương đương LangGraph với các bước:
1. Retrieve memory từ nhiều backend.
2. Inject memory vào prompt theo section rõ ràng.
3. Generate response.
4. Save/update memory với conflict handling.

### Cấu trúc chính

- `src/main.py`: entrypoint chạy chat loop demo.
- `src/graph/state.py`: định nghĩa `MemoryState`.
- `src/graph/router.py`: node `retrieve_memory(state)`.
- `src/graph/nodes.py`: `build_prompt(state)` + `save_memories(state)`.
- `src/memory/`: 4 backend memory + manager.
- `src/utils/`: extractor và token budget helpers.
- `tests/`: test conflict update + test retrieval/prompt sections.
- `tests/conversations/`: 10 case multi-turn cho benchmark.

### Cài đặt

```bash
pip install -r requirements.txt
```

### Chạy demo

```bash
python -m src.main
```

Gõ `exit` để thoát.

### Chạy test

```bash
pytest -q
```

### Checklist rubric

- [x] Full memory stack 4 loại.
- [x] Router gom multi-backend vào state.
- [x] Prompt injection đủ profile/episodic/semantic/recent conversation.
- [x] Save/update memory + conflict handling (last-write-wins).
- [x] Benchmark 10 multi-turn conversation (no-memory vs with-memory).
- [x] Reflection privacy/limitations.

### Ghi chú mở rộng (bonus)

- Có thể thay semantic fallback bằng Chroma/FAISS backend thực.
- Có thể thay token estimate bằng tokenizer thực để đo budget tốt hơn.
