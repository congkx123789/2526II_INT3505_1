# Naming Conventions trong RESTful API

> **Nguyên tắc cốt lõi:** URL là định danh *tài nguyên* (resource), không phải hành động.  
> HTTP Method (GET, POST, PUT, DELETE) đã đảm nhận vai trò hành động.

---

## 1. Bảng So Sánh – Bad vs Good

| Tiêu chí | Thiết kế kém (Poor) ❌ | Chuẩn mực (Best Practice) ✅ | Giải thích |
|---|---|---|---|
| **Plural Nouns** | `GET /user/1` `POST /createOrder` | `GET /users/1` `POST /orders` | Dùng **danh từ số nhiều**, tuyệt đối không dùng động từ trên URL |
| **Lowercase & Hyphens** | `GET /User-Profiles` `GET /user_profiles` | `GET /user-profiles` | Dùng **chữ thường + kebab-case** (gạch ngang) – dễ đọc & chuẩn SEO |
| **Hierarchy (Cấp bậc)** | `GET /users/1/getOrders` | `GET /users/1/orders` | Thể hiện **quan hệ tài nguyên** rõ ràng: orders thuộc user 1 |
| **Versioning** | `GET /users?version=1` | `GET /v1/users` | Đặt **phiên bản ở đầu path** để dễ quản lý vòng đời API |
| **Filtering/Search** | `GET /searchUsers?n=john` | `GET /v1/users?name=john` | Dùng **query string** cho filter, search, sort – không tạo endpoint riêng |
| **Actions đặc biệt** | `POST /users/1/doActivate` | `POST /v1/users/1/activate` | Nếu bắt buộc dùng action, dùng **danh từ hóa**, không có chữ "do/get" |

---

## 2. HTTP Methods – Quy ước

| Method | Mục đích | Ví dụ |
|--------|----------|-------|
| `GET` | Lấy tài nguyên (read-only, idempotent) | `GET /v1/users/1` |
| `POST` | Tạo tài nguyên mới | `POST /v1/users` |
| `PUT` | Cập nhật toàn bộ tài nguyên | `PUT /v1/users/1` |
| `PATCH` | Cập nhật một phần tài nguyên | `PATCH /v1/users/1` |
| `DELETE` | Xóa tài nguyên | `DELETE /v1/users/1` |

---

## 3. HTTP Status Codes Thường Gặp

| Code | Ý nghĩa | Khi nào dùng |
|------|---------|--------------|
| `200 OK` | Thành công | GET, PUT, PATCH thành công |
| `201 Created` | Tạo thành công | POST tạo resource mới |
| `204 No Content` | Thành công, không có body | DELETE thành công |
| `400 Bad Request` | Request sai | Validation lỗi, thiếu field |
| `401 Unauthorized` | Chưa xác thực | Thiếu/sai token |
| `403 Forbidden` | Không có quyền | Đúng token nhưng không có phép |
| `404 Not Found` | Không tìm thấy | Resource không tồn tại |
| `409 Conflict` | Xung đột | Duplicate email/username |
| `500 Internal Server Error` | Lỗi server | Bug backend |

---

## 4. Cấu trúc URL Đúng – Quick Reference

```
https://api.example.com/v1/users/42/orders?status=pending&page=1&limit=10
│                        │  │      │  │      └─────────────────────────────── Query string: filter/sort/paginate
│                        │  │      │  └───────────────────────────────────── Sub-resource: orders của user 42
│                        │  │      └──────────────────────────────────────── Resource ID: 42
│                        │  └─────────────────────────────────────────────── Resource: users (plural)
│                        └────────────────────────────────────────────────── Version: v1
└─────────────────────────────────────────────────────────────────────────── Base URL
```

---

## 5. Anti-patterns Cần Tránh

```
❌ /getUsers          → ✅ GET /v1/users
❌ /deleteUser/1      → ✅ DELETE /v1/users/1
❌ /users/create      → ✅ POST /v1/users
❌ /API/V1/GetOrders  → ✅ GET /v1/orders
❌ /user_orders/1     → ✅ GET /v1/users/1/orders
❌ /users?ver=2       → ✅ GET /v2/users
```
