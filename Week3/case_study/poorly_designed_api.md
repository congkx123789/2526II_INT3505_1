# 🔍 Case Study: Phát Hiện Lỗi trong Poorly Designed API

> **Hình thức:** Bài tập nhóm (3-4 sinh viên/nhóm)  
> **Thời gian:** 30 phút làm bài + 15 phút trình bày  
> **Mục tiêu:** Nhận diện, phân tích và đề xuất cải thiện thiết kế API kém

---

## 📋 Bối cảnh

Công ty Startup XYZ vừa ra mắt v1 của hệ thống quản lý thương mại điện tử. Junior developer vừa thiết kế bộ API sau đây. **Team của bạn được thuê để review và cải thiện toàn bộ API này.**

---

## 🚨 Bộ API Cần Review

Dưới đây là **10 endpoint** của hệ thống. Mỗi endpoint có thể chứa **một hoặc nhiều lỗi** về Naming, Consistency, Extensibility hoặc HTTP Method.

---

### Nhóm 1: Quản lý Người Dùng (Users)

**API #1**
```
GET /getAllUsers
```
Response:
```json
[
  {"UserID": 1, "UserName": "john", "EmailAddress": "john@gmail.com"},
  {"UserID": 2, "UserName": "jane", "EmailAddress": "jane@gmail.com"}
]
```

---

**API #2**
```
POST /createNewUser
```
Request Body:
```json
{
  "UserName": "nguyenvana",
  "Email": "vana@gmail.com",
  "phone": "0912345678"
}
```
Response (khi thành công):
```json
{"message": "User created", "id": 5}
```

---

**API #3**
```
GET /User_Profile?UserID=3
```
Response:
```json
{
  "id": 3,
  "username": "tranthib",
  "EmailAddr": "b@gmail.com",
  "PhoneNum": "0987654321",
  "Created": "15-01-2024"
}
```

---

**API #4**
```
POST /users/3/doUpdateProfile
```
Request Body:
```json
{"newEmail": "newemail@gmail.com"}
```

---

### Nhóm 2: Quản lý Đơn Hàng (Orders)

**API #5**
```
GET /getOrdersByUserID/5
```
Response:
```json
[
  {"order_id": "o001", "Status": "Done", "Amt": 150000},
  {"order_id": "o002", "Status": "Waiting", "Amt": 89000}
]
```

---

**API #6**
```
DELETE /orders/cancelOrder/o001
```

---

**API #7**
```
GET /Orders?page=1&pageSize=10
```
Response:
```json
{
  "orders": [
    {"id": "o001", "status": "completed"},
    {"id": "o002", "status": "pending"}
  ],
  "totalCount": 50
}
```

---

### Nhóm 3: Quản lý Sản Phẩm (Products)

**API #8**
```
GET /product-list
```
Response:
```json
{
  "ProductList": [
    {"ProductID": "p001", "ProductName": "Laptop", "UnitPrice": 15000000},
    {"ProductID": "p002", "ProductName": "Mouse", "UnitPrice": 250000}
  ]
}
```

---

**API #9**
```
PUT /products/p001/updateStock
```
Request Body:
```json
{"new_stock_quantity": 50}
```

---

**API #10**
```
GET /api/V2/searchProduct?keyword=laptop&sortBy=Price_DESC
```

---

## 📝 Bài Làm

Điền vào bảng sau cho **từng API** mà nhóm bạn được phân công review:

| API # | Lỗi phát hiện được | Loại lỗi | Đề xuất sửa |
|-------|-------------------|-----------|-------------|
| | | | |

> **Loại lỗi gợi ý:** Naming (N), Consistency (C), Extensibility (E), HTTP Method (M), Status Code (S)

---

## 🎯 Câu hỏi Bonus (cho nhóm hoàn thành sớm)

1. Nếu API #7 cần thêm thông tin `total_revenue` vào response mà **không làm hỏng client cũ**, bạn sẽ thêm vào đâu?

2. Thiết kế một endpoint cho phép **cập nhật chỉ trạng thái** (status) của đơn hàng. Nên dùng `PUT` hay `PATCH`? Tại sao?

3. API của hệ thống hiện không có versioning. Nếu cần ra v2 với một số thay đổi breaking, bạn sẽ migrate như thế nào?
