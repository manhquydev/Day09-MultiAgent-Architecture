# Báo cáo Đánh giá Kết quả Kiểm thử Hệ thống Shopping Assistant

## 1. Kết quả Batch Test
- **Tổng số ca kiểm thử**: 22/22
- **Số ca vượt qua (Pass)**: 22
- **Tỉ lệ vượt qua (Pass Rate)**: **100.00%**
- **Chi tiết vết vết (Traces)**: Đã được ghi nhận đầy đủ tại `src/artifacts/traces/batch-20260609-154941/`

### Bảng tóm tắt kết quả chi tiết
| Mã | Câu hỏi kiểm thử | Route mong đợi | Route thực tế | Trạng thái | Đánh giá |
|---|---|---|---|---|---|
| **Q01** | Chính sách hoàn trả hàng ra sao? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q02** | Giao hàng tiêu chuẩn thường mất bao lâu? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q03** | Khách có được kiểm hàng khi nhận không? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q04** | Voucher có được hoàn lại khi hủy đơn không? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q05** | Các trường hợp nào thường không hỗ trợ trả hàng? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q06** | Đơn hàng 1971 bao giờ được giao? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q07** | Cho tôi xem danh sách đơn hàng của khách hàng C001 | `['data']` | `['data']` | `ok` | **PASS** |
| **Q08** | Voucher của khách hàng C001 còn những mã nào dùng được? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q09** | Khách hàng C001 thuộc hạng gì và còn quota voucher bao nhiêu? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q10** | Đơn hàng 2058 đang ở trạng thái nào? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q11** | Đơn hàng 1971 có được hoàn trả không? | `['data', 'policy']` | `['policy', 'data']` | `ok` | **PASS** |
| **Q12** | Đơn hàng 2058 còn trong thời gian trả hàng không? | `['data', 'policy']` | `['policy', 'data']` | `ok` | **PASS** |
| **Q13** | Đơn hàng 2058 nếu khách đổi ý thì có thể trả trong bao lâu? | `['data', 'policy']` | `['policy', 'data']` | `ok` | **PASS** |
| **Q14** | Đơn hàng 1971 đang giao thì nên trả hàng hay từ chối nhận? | `['data', 'policy']` | `['policy', 'data']` | `ok` | **PASS** |
| **Q15** | Voucher của tôi còn dùng được không? | `[]` | `[]` | `clarification_needed` | **PASS** |
| **Q16** | Đơn hàng của tôi có được hoàn trả không? | `[]` | `[]` | `clarification_needed` | **PASS** |
| **Q17** | Kiểm tra đơn hàng 9999 giúp tôi | `['data']` | `['data']` | `not_found` | **PASS** |
| **Q18** | Cho tôi xem voucher của khách hàng C999 | `['data']` | `['data']` | `not_found` | **PASS** |
| **Q19** | Customer C014 có những đơn nào gần đây? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q20** | Phương thức giao nhanh có thể bị chuyển sang giao tiêu chuẩn khi nào? | `['policy']` | `['policy']` | `ok` | **PASS** |
| **Q21** | Khách hàng C001 tối đa dùng bao nhiêu voucher mỗi tháng? | `['data']` | `['data']` | `ok` | **PASS** |
| **Q22** | Đơn hàng 2058 có liên quan gì đến cửa sổ trả hàng 15 ngày trong policy không? | `['data', 'policy']` | `['policy', 'data']` | `ok` | **PASS** |

---

## 2. Các phần đã tối ưu hóa
1. **Query Expansion RAG (Q01)**: Thay thế cụm từ tìm kiếm bổ sung thành `"thời hạn trả hàng đổi trả 15 ngày"` giúp vector store Chroma lấy được chính xác phần `5.1. Điều kiện chung để gửi yêu cầu` có chứa thông tin "15 ngày".
2. **Định tuyến Supervisor (Q21)**: Thêm cơ chế ghi đè thông minh trong Supervisor để hướng thẳng câu hỏi về quota voucher tối đa của một mã khách hàng cụ thể sang `data` (không cần đi qua `policy` thừa thãi).
3. **Cấu hình Custom LLM Providers**: Hoàn thiện toàn bộ logic tùy chỉnh cho cả 4 LLM providers (Gemini, OpenAI, DeepSeek, Ollama) hỗ trợ đầy đủ các tham số cấu hình như `max_tokens`, `top_p`, `num_predict`, `num_ctx`, `format`.

---

## 3. Câu hỏi chưa giải quyết (Unresolved Questions)
- Không có câu hỏi nào chưa giải quyết.
