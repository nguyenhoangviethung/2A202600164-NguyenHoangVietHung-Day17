# Knowledge Base

## LangGraph memory router

LangGraph router là thành phần điều phối truy vấn tới nhiều backend memory khác nhau: profile store, episodic log, semantic index, và short-term conversation buffer.

## Prompt injection structure

Agent cần chia prompt thành 4 phần rõ ràng:
1. User profile
2. Episodic memory summaries
3. Semantic hits / knowledge chunks
4. Recent conversation history

## Token budget trimming

Khi tổng nội dung quá dài, agent nên cắt bớt:
- recent conversation chỉ giữ N turn cuối
- semantic hits chỉ dùng top-K chunk
- profile chỉ giữ facts quan trọng nhất
- episodic chỉ giữ các summary liên quan nhất đến nhiệm vụ hiện tại

## Semantic retrieval examples

- Nếu user hỏi về cách dùng Chroma/FAISS, semantic memory trả về chunk giải thích architecture và indexing.
- Nếu user hỏi lại nội dung bài lab, semantic memory trả về câu trả lời dựa trên knowledge base thay vì phụ thuộc hoàn toàn vào LLM prompt.

## Conflict handling principle

Profile facts phải được cập nhật theo thông tin mới nhất. Nếu user nói "Tôi dị ứng sữa bò" rồi sửa lại "Tôi dị ứng đậu nành", hệ thống phải ghi đè allergy = đậu nành.

## Privacy note

Sensitive data như allergy, health, địa chỉ, số điện thoại cần được xử lý cẩn thận. Nếu có yêu cầu xóa, phải xóa profile store và episodic log liên quan.
