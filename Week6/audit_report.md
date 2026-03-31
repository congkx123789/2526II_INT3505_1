# Báo Cáo Security Audit: Kiểm Tra Lộ Token (JWT)

Dự án này thực hiện Audit (Kiểm tra an ninh) cho việc lưu trữ JWT trên Browser.

## 1. Đối Tượng Kiểm Tra
- **Phương pháp 1:** Lưu JWT vào `localStorage` (Phản hồi JSON từ `/api/login-insecure`).
- **Phương pháp 2:** Lưu JWT vào `HttpOnly Cookie` (Phản hồi từ `/api/login-secure`).

## 2. Kết Quả Audit (Thực Nghiệm)

### 2.1. Rủi ro Token Leakage (Rò rỉ qua LocalStorage)
- **Hành động:** Sử dụng script `localStorage.getItem('access_token')` mô phỏng cuộc tấn công XSS.
- **Kết quả:** **[THẤT BẠI]** - Hacker hoàn toàn có thể đọc được toàn bộ chuỗi Token.
- **Kết luận:** LocalStorage không an toàn để lưu trữ dữ liệu nhạy cảm như JWT vì bất kỳ script nào chạy trên trang web (bao gồm cả các thư viện bên thứ 3 độc hại) đều có thể truy cập được.

### 2.2. Kiểm tra Bảo mật Cookie (HttpOnly)
- **Hành động:** Sử dụng script `document.cookie` để cố gắng đọc Token được lưu trong Cookie.
- **Kết quả:** **[THÀNH CÔNG]** - Browser không trả về giá trị của `access_token` trong chuỗi `document.cookie`.
- **Kết luận:** Thuộc tính `HttpOnly` ngăn chặn Javascript truy cập vào Cookie. Ngay cả khi trang web bị lỗ hổng XSS, hacker cũng không thể đánh cắp Token theo cách thông thường.

## 3. Đánh Giá Khả Năng Replay Attack
- **Phát hiện:** Token Access có thời hạn sống (TTL) là 15 phút.
- **Rủi ro:** Nếu kẻ xấu bắt được request chứa token, chúng có 15 phút để thực hiện các hành động giả mạo.
- **Khắc phục đã triển khai trong mã nguồn:**
    - Sử dụng `SameSite: 'Strict'` để ngăn chặn tấn công CSRF (Cross-Site Request Forgery) khi dùng Cookie.
    - Thời hạn token ngắn giúp giảm thiểu cửa sổ tấn công của Replay Attack.

## 4. Khuyến Nghị Cuối Cùng
1.  **Tuyệt đối không lưu JWT vào LocalStorage** cho các ứng dụng yêu cầu bảo mật cao.
2.  **Sử dụng HttpOnly Cookies** kết hợp với `Secure: true` (trên môi trường HTTPS).
3.  **Áp dụng cơ chế Refresh Token** để giữ thời gian sống của Access Token thật ngắn (ví dụ 5 phút).
