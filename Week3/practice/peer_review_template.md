# 📋 Template Peer Review – Thiết Kế API

> **Hướng dẫn:** Mỗi nhóm điền vào template này cho **mỗi endpoint** trong hệ thống của nhóm mình.  
> Sau đó nhóm khác sẽ review theo cùng tiêu chí.

---

## Thông Tin Nhóm

| Mục | Nội dung |
|-----|---------|
| **Tên nhóm** | |
| **Thành viên** | |
| **Hệ thống thiết kế** | _(VD: Hệ thống quản lý thư viện)_ |
| **Ngày** | |

---

## Endpoint Template

*Copy block này cho mỗi endpoint. Mỗi nhóm cần thiết kế ít nhất **5 endpoints**.*

---

### Endpoint #___

**Method & URL:**
```
[GET/POST/PUT/PATCH/DELETE] /v1/resource/{id}/sub-resource
```

**Mô tả (Clarity):**
> _(Tóm tắt chức năng trong 1 câu. VD: "Lấy danh sách đơn hàng của user có id được chỉ định")_

**Path Parameters:**

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `{id}` | integer | ✅ | ID của resource |

**Query Parameters:**

| Tên | Kiểu | Bắt buộc | Mặc định | Mô tả |
|-----|------|----------|----------|-------|
| `page` | integer | ❌ | 1 | Số trang |
| `limit` | integer | ❌ | 10 | Số bản ghi/trang |

**Request Body** _(nếu có – POST/PUT/PATCH):_
```json
{
  "field_name": "example_value"
}
```

**Response – Thành công:**

HTTP Status: `200 OK` / `201 Created` / `204 No Content`

```json
{
  "success": true,
  "data": {
    "id": 1,
    "field_name": "value"
  }
}
```

**Response – Thất bại:**

HTTP Status: `400` / `401` / `404` / `409` / `500`

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Mô tả lỗi rõ ràng.",
    "details": null
  }
}
```

---

## Checklist Tự Review (Nhóm Tác Giả)

Trước khi trình bày, hãy tự kiểm tra:

- [ ] URL dùng **danh từ số nhiều**, không có động từ
- [ ] URL dùng **kebab-case** (chữ thường + gạch ngang)
- [ ] Có **versioning** (`/v1/`, `/v2/`, ...)
- [ ] Resource ID là **path parameter**, không phải query string
- [ ] **HTTP Method** phù hợp với hành động (GET/POST/PUT/PATCH/DELETE)
- [ ] **Request body fields** nhất quán (toàn snake_case hoặc toàn camelCase)
- [ ] **Response fields** nhất quán với request body
- [ ] Response dùng **envelope pattern** (`success`, `data`, `error`)
- [ ] Response danh sách có **pagination**
- [ ] **HTTP Status Code** chính xác
- [ ] Error response có `code` (machine-readable) và `message` (human-readable)
- [ ] Date/time dùng **ISO 8601** (`2024-01-15T10:30:00Z`)

---

## Phiếu Review (Nhóm Review Điền)

**Nhóm reviewer:** _______________  
**Nhóm được review:** _______________

| Tiêu chí | Điểm (1–5) | Nhận xét |
|----------|-----------|---------|
| **Naming Conventions** | /5 | |
| **Consistency** (nhất quán) | /5 | |
| **Extensibility** (dễ mở rộng) | /5 | |
| **HTTP Methods** | /5 | |
| **Status Codes** | /5 | |
| **Tổng** | /25 | |

**Điểm mạnh:** 

**Cần cải thiện:**

**Câu hỏi cho nhóm:**
