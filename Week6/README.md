# Week 6: JWT Authentication & Security Audit (Node.js)

Dự án này là bài Lab thực hành chuyên sâu về **Xác thực (Authentication)** và **Phân quyền (Authorization)** bằng JWT trong kiến trúc Node.js, đi kèm với thử nghiệm **Security Audit (Kiểm tra an ninh)**.

## 1. Nội Dung Thực Hành
- **Triển khai JWT:** Sử dụng `jsonwebtoken` để cấp phát Access/Refresh tokens.
- **Roles & Scopes:** Middleware kiểm tra quyền truy cập tài nguyên (RBAC).
- **Security Audit:** So sánh thực tế giữa `localStorage` và `HttpOnly Cookie`.

## 2. Hướng Dẫn Cài Đặt và Chạy

### Bước 1: Cài đặt Dependencies
Mở terminal tại thư mục `Week6` và chạy:
```bash
npm install
```

### Bước 2: Chạy Backend Server
```bash
node server.js
```
Server sẽ chạy tại `http://localhost:5000`.

### Bước 3: Mở Frontend
Bạn có thể mở file `index.html` trực tiếp bằng trình duyệt hoặc sử dụng Live Server.
- **URL gợi ý:** `http://localhost:5000/index.html` (Nếu bạn cấu hình static file - hiện tại hãy mở trực tiếp file `index.html`).

## 3. Các Bước Thực Hiện Security Audit (Audit Steps)

1.  **Thực hiện Đăng nhập Insecure:** Click `Login (Insecure - LocalStorage)`.
2.  **Kiểm tra Rò rỉ Token:** Click `Steal from LocalStorage`. Bạn sẽ thấy Hacker lấy được mã JWT dễ dàng.
3.  **Đăng nhập Secure:** Click `Login (Secure - HttpOnly Cookie)`.
4.  **Kiểm tra Bảo vệ:** Click `Steal from Cookie`. Bạn sẽ thấy Hacker **thất bại** vì mã JWT đã được ẩn khỏi Javascript bằng cờ `HttpOnly`.

---
Chi tiết báo cáo kiểm tra an ninh có thể xem tại: [audit_report.md](file:///d:/Micro/2526II_INT3505_1/Week6/audit_report.md)
