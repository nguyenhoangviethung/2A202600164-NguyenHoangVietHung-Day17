# Reflection - Privacy and Limitations

## 1. What memory helps most?

Trong kiến trúc này, memory hữu ích nhất là **long-term profile** và **episodic memory**. Profile giúp agent ghi nhớ thông tin người dùng như tên, ngôn ngữ, preference, allergy và sử dụng lại trong các lượt sau. Episodic memory giúp agent ghi lại outcome của các tác vụ hoặc các session quan trọng để trả lời lại những câu hỏi như "Lần trước tôi đã làm gì?".

## 2. Which memory type is most privacy-sensitive?

Memory nhạy cảm nhất là **long-term profile** vì nó có thể chứa PII và dữ liệu sức khỏe như dị ứng, sở thích, nghề nghiệp. Nếu profile bị lộ hoặc retrieved sai, agent có thể đưa ra đề xuất sai lầm với hậu quả thực tiễn.

## 3. If user asks deletion, what backend(s) must be updated?

- `data/profile/profile.json`: xóa hoặc cập nhật facts của user.
- `data/episodic/episodes.jsonl`: xóa các entry session liên quan.
- Với semantic memory, nếu có repository vector thật, cũng cần xóa documents/chunks liên quan.
- Short-term memory không cần xóa lâu dài vì chỉ lưu trong phiên hiện tại.

## 4. What technical limitations exist?

- Phiên bản hiện tại dùng data file tĩnh nên khó scale khi số người dùng tăng.
- Semantic retrieval chưa có hệ thống vector thật (fallback keyword search vẫn ổn nhưng không đủ mạnh).
- Budget trimming chỉ là cắt chuỗi, chưa đo token chính xác nên có thể mất thông tin quan trọng.
- Conflict resolution phụ thuộc vào extractor đơn giản, nếu không xác định đúng câu sửa đổi thì profile vẫn có thể lưu thông tin cũ.

## 5. Privacy risks và hạn chế

- Nếu retrieval sai, `semantic_hits` có thể trả về chunk không liên quan và agent sẽ đưa ra câu trả lời sai.
- Dữ liệu dị ứng và sức khỏe là rủi ro cao nhất; cần cân nhắc consent, TTL và chế độ xóa khi người dùng yêu cầu.
- Khi scale, việc lưu file JSON/JSONL đồng bộ dễ gây race condition và mất tính nhất quán trong nhiều phiên concurrent.

## 6. Kết luận

Kiến trúc này phù hợp để demo full memory stack và prompt injection, nhưng cần mở rộng backend thật và token counting chính xác để dùng trong sản phẩm thực tế.
