# 📚 Đáp Án Case Study – Poorly Designed API

> **⚠️ DÀNH CHO GIẢNG VIÊN – Không phát cho sinh viên trước buổi học**

---

## API #1: `GET /getAllUsers`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ trong URL:** `/getAllUsers` dùng động từ `get`. HTTP Method `GET` đã thể hiện hành động này.
2. **(N) Naming – Singular/Plural:** Nên dùng danh từ số nhiều.
3. **(E) Extensibility:** Response trả về mảng trực tiếp `[...]` → không thể thêm pagination.
4. **(C) Consistency – PascalCase:** `UserID`, `UserName`, `EmailAddress` → không nhất quán với chuẩn REST.

**Sửa thành:**
```
GET /v1/users
```
```json
{
  "success": true,
  "data": [
    {"id": 1, "username": "john", "email_address": "john@gmail.com"},
    {"id": 2, "username": "jane", "email_address": "jane@gmail.com"}
  ],
  "pagination": {"page": 1, "limit": 10, "total_records": 2, "total_pages": 1, "has_next": false, "has_prev": false}
}
```

---

## API #2: `POST /createNewUser`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ:** `/createNewUser` vi phạm nguyên tắc danh từ.
2. **(C) Consistency – Request Body:** `UserName` (PascalCase), `Email` (Capitalized), `phone` (lowercase) → trộn lẫn 3 style.
3. **(E) Extensibility – Response:** Khi thành công chỉ trả `{"message": "...", "id": 5}` → thiếu data đầy đủ, thiếu envelope.
4. **(S) Status Code:** Nên trả `201 Created` thay vì `200 OK` khi tạo resource mới.

**Sửa thành:**
```
POST /v1/users   →  201 Created
```
Request Body:
```json
{"username": "nguyenvana", "email_address": "vana@gmail.com", "phone_number": "0912345678"}
```
Response:
```json
{
  "success": true,
  "data": {"id": 5, "username": "nguyenvana", "email_address": "vana@gmail.com", "phone_number": "0912345678", "is_active": true, "created_at": "2024-01-15T10:00:00Z"}
}
```

---

## API #3: `GET /User_Profile?UserID=3`

**Lỗi tìm thấy:**
1. **(N) Naming – PascalCase + Underscore:** `/User_Profile` vi phạm kebab-case & lowercase.
2. **(N) Naming – ID trong query string:** Resource ID nên là path param: `/users/3`.
3. **(C) Consistency – Response fields:** `id`, `username`, `EmailAddr`, `PhoneNum`, `Created` → trộn lẫn nhiều convention.
4. **(C) Consistency – Date format:** `"15-01-2024"` nên dùng ISO 8601: `"2024-01-15T00:00:00Z"`.

**Sửa thành:**
```
GET /v1/users/3
```
```json
{
  "success": true,
  "data": {"id": 3, "username": "tranthib", "email_address": "b@gmail.com", "phone_number": "0987654321", "created_at": "2024-01-15T00:00:00Z"}
}
```

---

## API #4: `POST /users/3/doUpdateProfile`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ:** `doUpdateProfile` vi phạm nguyên tắc.
2. **(M) HTTP Method:** Cập nhật một phần (chỉ email) → nên dùng `PATCH`, không phải `POST`.
3. **(N) Naming – Thiếu versioning.**
4. **(C) Consistency – Request field:** `newEmail` (camelCase) không nhất quán với snake_case.

**Sửa thành:**
```
PATCH /v1/users/3   →  200 OK
```
```json
{"email_address": "newemail@gmail.com"}
```

---

## API #5: `GET /getOrdersByUserID/5`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ + không có hierarchy rõ ràng:** Nên thể hiện quan hệ user → orders.
2. **(E) Extensibility:** Trả mảng trực tiếp, thiếu pagination.
3. **(C) Consistency – Response:** `order_id`, `Status` (PascalCase), `Amt` (viết tắt) → không nhất quán.

**Sửa thành:**
```
GET /v1/users/5/orders
```
```json
{
  "success": true,
  "data": [
    {"id": "o001", "status": "completed", "total_amount": 150000},
    {"id": "o002", "status": "pending", "total_amount": 89000}
  ],
  "pagination": {"page": 1, "limit": 10, "total_records": 2, "total_pages": 1, "has_next": false, "has_prev": false}
}
```

---

## API #6: `DELETE /orders/cancelOrder/o001`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ trong URL:** `cancelOrder` là hành động, không phải tài nguyên.
2. **(M) HTTP Method:** `DELETE` xóa tài nguyên; "cancel" là thay đổi *trạng thái* → nên dùng `PATCH`.

**Sửa thành:**
```
PATCH /v1/orders/o001   →  200 OK
```
```json
{"status": "cancelled"}
```

---

## API #7: `GET /Orders?page=1&pageSize=10`

**Lỗi tìm thấy:**
1. **(N) Naming – PascalCase URL:** `/Orders` → phải là `/orders`.
2. **(C) Consistency – Query params:** `pageSize` (camelCase) → nên là `limit` (snake_case, cũng là convention phổ biến hơn).
3. **(E) Extensibility – Response:** Có `orders` và `totalCount` nhưng thiếu chuẩn envelope, thiếu các pagination field hữu ích.
4. **(N) Naming – Thiếu versioning.**

**Sửa thành:**
```
GET /v1/orders?page=1&limit=10
```
```json
{
  "success": true,
  "data": [{"id": "o001", "status": "completed"}, {"id": "o002", "status": "pending"}],
  "pagination": {"page": 1, "limit": 10, "total_records": 50, "total_pages": 5, "has_next": true, "has_prev": false}
}
```

---

## API #8: `GET /product-list`

**Lỗi tìm thấy:**
1. **(N) Naming – "list" thừa:** `/product-list` → danh từ số nhiều đã đủ: `/products`.
2. **(E) Extensibility:** Bọc trong key `ProductList` (PascalCase) nhưng không có envelope chuẩn.
3. **(C) Consistency:** `ProductID`, `ProductName`, `UnitPrice` → PascalCase trong response JSON.
4. **(N) Naming – Thiếu versioning.**

**Sửa thành:**
```
GET /v1/products
```
```json
{
  "success": true,
  "data": [
    {"id": "p001", "name": "Laptop", "unit_price": 15000000},
    {"id": "p002", "name": "Mouse", "unit_price": 250000}
  ],
  "pagination": {"page": 1, "limit": 10, "total_records": 2, "total_pages": 1, "has_next": false, "has_prev": false}
}
```

---

## API #9: `PUT /products/p001/updateStock`

**Lỗi tìm thấy:**
1. **(N) Naming – Động từ:** `updateStock` là action.
2. **(M) HTTP Method:** Chỉ cập nhật một field → `PATCH` phù hợp hơn `PUT`. `PUT` thay thế *toàn bộ* resource.
3. **(C) Consistency – Request field:** `new_stock_quantity` có prefix `new_` không cần thiết.

**Sửa thành:**
```
PATCH /v1/products/p001   →  200 OK
```
```json
{"stock_quantity": 50}
```

---

## API #10: `GET /api/V2/searchProduct?keyword=laptop&sortBy=Price_DESC`

**Lỗi tìm thấy:**
1. **(N) Naming – Uppercase versioning:** `/V2` → nên là `/v2`.
2. **(N) Naming – Động từ:** `searchProduct` → dùng query string trên `/products`.
3. **(N) Naming – Prefix `/api/`:** Thường không cần thiết, base URL đã là API.
4. **(C) Consistency – Query params:** `sortBy` (camelCase) và `Price_DESC` (PascalCase + underscore) → không nhất quán.

**Sửa thành:**
```
GET /v2/products?keyword=laptop&sort_by=price&order=desc
```

---

## 🎯 Đáp Án Câu Hỏi Bonus

**Bonus 1:** Thêm `total_revenue` vào key `meta` hoặc tạo key mới cạnh `data` trong envelope → không đụng đến `data` array → client cũ không bị ảnh hưởng.

**Bonus 2:** Dùng `PATCH /v1/orders/{id}` với body `{"status": "completed"}`. Dùng `PATCH` vì chỉ cập nhật *một phần* resource. `PUT` đòi hỏi gửi toàn bộ representation của resource.

**Bonus 3:** Chiến lược migrate: (1) Ra mắt `/v2/...` song song `/v1/...`; (2) Thông báo deprecation cho `/v1`; (3) Hỗ trợ `/v1` thêm 6-12 tháng; (4) Tắt `/v1` sau sunset date đã thông báo.
