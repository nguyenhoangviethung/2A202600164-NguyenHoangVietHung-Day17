# BENCHMARK - No-memory vs With-memory

Thiết kế benchmark gồm 10 hội thoại multi-turn để so sánh rõ ràng giữa hai cấu hình:
- `no-memory`: chỉ dùng input hiện tại, không retrieve profile/episodic/semantic.
- `with-memory`: dùng full stack memory + prompt injection.

## Benchmark Table

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Recall user name after 6 turns | Quên tên hoặc trả lời chung chung | Nhớ đúng tên `Linh` | Pass |
| 2 | Allergy conflict update | Vẫn giữ thông tin cũ `sữa bò` | Cập nhật đúng `đậu nành` | Pass |
| 3 | Recall previous debug lesson | Không nhớ task trước đó | Nhắc lại đúng outcome từ episodic memory | Pass |
| 4 | Retrieve memory architecture note | Trả lời mơ hồ về router | Trích đúng chunk semantic về router | Pass |
| 5 | Long context with trim budget | Bị loạn/ngắt mạch khi nhiều turn | Giữ được nội dung quan trọng sau trim | Pass |
| 6 | Preference recall in new session | Không nhớ đồ uống yêu thích | Nhớ `cà phê đen` từ profile | Pass |
| 7 | Outcome persistence after task done | Không lưu tóm tắt task | Có episode mới với outcome rõ | Pass |
| 8 | Profile correction after contradiction | Lưu cả 2 facts mâu thuẫn | Ghi đè fact mới theo last-write-wins | Pass |
| 9 | Semantic retrieval for FAQ-like question | Thiếu context chuyên môn | Trả lời dựa trên knowledge chunk phù hợp | Pass |
| 10 | Composite answer (profile+episodic+semantic) | Câu trả lời rời rạc, thiếu liên kết | Câu trả lời cá nhân hóa + chính xác + nhất quán | Pass |

## Token/Budget Observation

- Budget mặc định dùng: `memory_budget = 1200`.
- Ở hội thoại dài, `with-memory` vẫn ổn định do trim theo section.
- Chi phí ước lượng dùng heuristic ký tự/token, chưa dùng tokenizer thật.

## Kết luận benchmark

Cấu hình `with-memory` vượt trội rõ ràng ở cả 5 nhóm tiêu chí rubric:
- profile recall
- conflict update
- episodic recall
- semantic retrieval
- trim/token budget
