# 🎯 Bài Tập Nhóm – Thiết Kế RESTful API

> **Thời gian:** 45 phút  
> **Kết quả nộp:** File `peer_review_template.md` đã điền đầy đủ + trình bày 5 phút

---

## Bối Cảnh Bài Tập

Mỗi nhóm sẽ thiết kế API cho **một hệ thống được phân công** dưới đây:

| Nhóm | Hệ thống |
|------|---------|
| Nhóm 1 | 📚 Quản lý thư viện (sách, độc giả, mượn/trả) |
| Nhóm 2 | 🏥 Quản lý phòng khám (bác sĩ, bệnh nhân, lịch hẹn) |
| Nhóm 3 | 🎓 Quản lý khóa học trực tuyến (khóa học, học viên, bài học) |
| Nhóm 4 | 🛒 Quản lý cửa hàng tạp hóa (sản phẩm, đơn hàng, kho) |
| Nhóm 5 | 🏨 Quản lý khách sạn (phòng, đặt phòng, dịch vụ) |

---

## Yêu Cầu Bắt Buộc

Thiết kế **tối thiểu 5 endpoints** cho hệ thống của nhóm, đảm bảo:

### ✅ Naming Conventions
- [ ] URL dùng danh từ số nhiều (plural nouns)
- [ ] Không dùng động từ trong URL
- [ ] Dùng kebab-case và chữ thường
- [ ] Có versioning (`/v1/`)
- [ ] Thể hiện hierarchy (ít nhất 1 sub-resource)

### ✅ Consistency
- [ ] Chọn **một** naming convention cho JSON fields (snake_case hoặc camelCase) và áp dụng đồng nhất
- [ ] Format ngày tháng nhất quán (ISO 8601)
- [ ] Error response có cấu trúc nhất quán

### ✅ Extensibility
- [ ] Dùng envelope pattern (`success`, `data`, `error`)
- [ ] Danh sách có pagination trong response

### ✅ HTTP Semantics
- [ ] HTTP Method phù hợp với từng action
- [ ] HTTP Status Code chính xác

---

## Gợi Ý Endpoints (Ví Dụ Cho Hệ Thống Thư Viện)

```
GET    /v1/books                    → Danh sách sách (có pagination, filter)
POST   /v1/books                    → Thêm sách mới
GET    /v1/books/{book_id}          → Chi tiết một cuốn sách
PATCH  /v1/books/{book_id}          → Cập nhật thông tin sách
DELETE /v1/books/{book_id}          → Xóa sách

GET    /v1/readers/{reader_id}/borrows   → Lịch sử mượn sách của độc giả
POST   /v1/borrows                        → Tạo yêu cầu mượn sách
PATCH  /v1/borrows/{borrow_id}           → Cập nhật trạng thái (return)
```

---

## Tiêu Chí Đánh Giá Trình Bày

| Tiêu chí | Điểm |
|----------|------|
| Naming Conventions đúng | 20 |
| Consistency trong JSON | 20 |
| Extensibility (envelope + pagination) | 20 |
| HTTP Methods & Status Codes | 20 |
| Chất lượng trình bày & giải thích | 20 |
| **Tổng** | **100** |
