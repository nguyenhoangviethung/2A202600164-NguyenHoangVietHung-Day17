# BENCHMARK - No-memory vs With-memory

Đây là bảng benchmark cho 10 kịch bản multi-turn. Sau khi chạy agent, bạn nên điền kết quả thực tế vào cột `No-memory result` và `With-memory result`.

## Benchmark table

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Recall user name after 6 turns | Forget or generic response | Recalls name and preferences | Pending |
| 2 | Allergy conflict update | Still uses old allergy or is uncertain | Uses corrected allergy `đậu nành` | Pending |
| 3 | Episodic recall of prior task | Cannot recall previous session | Recalls summary from episodic log | Pending |
| 4 | Semantic retrieval of knowledge chunk | Answers shallowly or incorrectly | Returns exact knowledge chunk | Pending |
| 5 | Long conversation with trim budget | Loses earlier context | Keeps recent context and key memory facts | Pending |
| 6 | Preference recall in new session | Ignores stored favorite drink | Uses stored drink preference | Pending |
| 7 | Task outcome saves episodic memory | No persistent summary saved | Episode summary is stored and retrieved | Pending |
| 8 | Correction of profile after wrong fact | Maintains outdated profile | Updates profile to newest fact | Pending |
| 9 | Semantic search for FAQ detail | Misses domain-specific answer | Uses knowledge base chunk correctly | Pending |
| 10 | Multi-memory composite response | Answers incomplete or disjoint | Uses profile + episodic + semantic coherently | Pending |

## Hướng dẫn benchmark

- Mỗi scenario phải là multi-turn, không chỉ 1 câu hỏi.
- Nhớ kiểm tra cả `no-memory` và `with-memory` để thấy sự khác biệt.
- Bổ sung thông tin `Pass?` sau khi xác nhận hành vi.
- Nếu có thể, ghi thêm `Actual output` ngắn trong phần ghi chú test.

## Ghi chú

- Nhóm scenario cần bao phủ: profile recall, conflict update, episodic recall, semantic retrieval, budget trimming.
- Nếu agent chưa chạy được, bảng này vẫn là checklist để bạn hoàn thiện sau.
