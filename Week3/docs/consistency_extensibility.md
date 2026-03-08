# Consistency & Extensibility trong RESTful API

---

## 1. Tính Nhất Quán (Consistency) – JSON Payload

**Quy tắc vàng:** Chọn **một** phong cách đặt tên field và áp dụng **đồng nhất** cho toàn bộ hệ thống.

### ❌ API thiếu nhất quán (Problematic)

```json
{
  "UserName": "nguyenvana",
  "email_address": "a@gmail.com",
  "Phone": "0123456789",
  "createdAt": "2024-01-15",
  "is_active": true
}
```

**Phân tích lỗi:**
- `UserName` → PascalCase
- `email_address` → snake_case
- `Phone` → Capitalized
- `createdAt` → camelCase
- `is_active` → snake_case

> Trộn lẫn 4 quy ước khác nhau trong cùng một response → Developer phải đoán tên field → Dễ bug khi tích hợp.

---

### ✅ API nhất quán – Dùng snake_case (Python/Ruby convention)

```json
{
  "username": "nguyenvana",
  "email_address": "a@gmail.com",
  "phone_number": "0123456789",
  "created_at": "2024-01-15",
  "is_active": true
}
```

### ✅ API nhất quán – Dùng camelCase (JavaScript/Java convention)

```json
{
  "username": "nguyenvana",
  "emailAddress": "a@gmail.com",
  "phoneNumber": "0123456789",
  "createdAt": "2024-01-15",
  "isActive": true
}
```

> **Lưu ý:** Chọn một trong hai. Quan trọng là **nhất quán**, không phải bạn chọn cái nào.

---

## 2. Tính Mở Rộng (Extensibility) – Response Structure

### ❌ Trả về mảng trực tiếp (Anti-pattern)

```json
[
  {"id": "ord_123", "status": "completed"},
  {"id": "ord_124", "status": "pending"}
]
```

**Vấn đề:**
- Muốn thêm `pagination`? → Phải **phá vỡ** cấu trúc hiện tại → **Client cũ bị lỗi**
- Không có chỗ trả về `metadata` (tổng số record, thời gian xử lý, v.v.)
- Không có chỗ trả về `errors` hay `warnings` bên cạnh data

---

### ✅ Bọc dữ liệu trong Envelope Object (Best Practice)

**GET /v1/orders** → Response thành công:

```json
{
  "success": true,
  "data": [
    {
      "id": "ord_123",
      "status": "completed",
      "total_amount": 150000,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "ord_124",
      "status": "pending",
      "total_amount": 89000,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total_records": 50,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  },
  "meta": {
    "request_id": "req_abc123",
    "response_time_ms": 42
  }
}
```

**GET /v1/orders/ord_999** → Response thất bại (404):

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Order with id 'ord_999' does not exist.",
    "details": null
  }
}
```

**POST /v1/orders** → Response validation lỗi (400):

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request body contains invalid fields.",
    "details": [
      {"field": "total_amount", "issue": "Must be a positive number"},
      {"field": "items", "issue": "Cannot be empty"}
    ]
  }
}
```

---

## 3. Tại Sao Envelope Pattern Quan Trọng?

| Tình huống | Mảng trực tiếp ❌ | Envelope Object ✅ |
|---|---|---|
| Thêm pagination | Phá vỡ contract cũ | Thêm key `pagination` – client cũ không ảnh hưởng |
| Trả lỗi nhất quán | Không có chuẩn | Luôn có `success`, `error` |
| Thêm metadata | Không thể | Thêm vào `meta` – dễ dàng |
| Versioning nội dung | Phức tạp | Thêm `version` vào envelope |

---

## 4. Nguyên tắc Thiết Kế Chung

```
1. KISS   – Keep It Simple, Stupid
2. YAGNI  – You Aren't Gonna Need It (đừng over-engineer)
3. DRY    – Don't Repeat Yourself (nhất quán naming, structure)
4. RFC 7807 – Standard cho Problem Details in HTTP APIs
```
