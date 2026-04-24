# Lab 17 - Multi-Memory Agent

## Mục tiêu

Xây dựng một agent có đủ 4 memory types theo rubric:
- Short-term memory (conversation buffer)
- Long-term profile memory
- Episodic memory
- Semantic memory

Và thiết kế flow retrieval/prompt injection tương đương LangGraph, cùng benchmark so sánh `no-memory` vs `with-memory`.

## Cấu trúc thư mục

- `src/` - mã nguồn Python của agent (không chỉnh sửa file `.py` này theo yêu cầu hiện tại)
- `src/prompts/system_prompt.md` - mẫu prompt có section memory
- `configs/settings.yaml` - cấu hình runtime và budget
- `data/profile/profile.json` - mock long-term profile memory
- `data/episodic/episodes.jsonl` - mock episodic memory log
- `data/semantic/knowledge_base.md` - mock semantic knowledge chunks
- `BENCHMARK.md` - benchmark 10 hội thoại so sánh no-memory vs with-memory
- `REFLECTION.md` - phân tích privacy, giới hạn, và backend nhạy cảm
- `tests/conversations/` - 10 kịch bản multi-turn để tự kiểm tra behavior

## Hướng dẫn sử dụng

1. Cài dependencies trong `requirements.txt`.
2. Hoàn thiện code trong `src/` theo cấu trúc đã định.
3. Chạy benchmark bằng cách kiểm tra challenge trong `tests/conversations/*.md`.
4. Ghi lại kết quả thực tế vào `BENCHMARK.md`.
5. Hoàn thiện `REFLECTION.md` bằng quan sát privacy và giới hạn kỹ thuật.

## Ghi chú quan trọng

- Không sửa file `.py` theo yêu cầu của lần này; chỉ chỉnh file tài liệu và dữ liệu.
- File data đã có mock sample để bạn dùng khi phát triển semantic/profile/episodic.
- `BENCHMARK.md` và `REFLECTION.md` cần được hoàn thành trước khi nộp.
# 2A202600164-NguyenHoangVietHung-Day17
# 2A202600164-NguyenHoangVietHung-Day17
