# Hướng Dẫn Thuyết Trình & Chạy Demo - Week 6: JWT & Security Audit

Tài liệu này hướng dẫn chi tiết cách vận hành demo và kịch bản thuyết trình cho bài thực hành về JWT Authentication và Security Audit.

---

## 1. Hướng Dẫn Chạy Demo (Quick Start)

Bạn có thể chạy Demo bằng **Node.js** (Khuyên dùng) hoặc **Flask (Python)**.

### Tùy chọn 1: Chạy bằng Node.js (Express)
1.  **Mở Terminal** tại thư mục `Week6`.
2.  **Cài đặt thư viện**: `npm install`
3.  **Khởi động Server**: `node server.js`
4.  **Truy cập Giao diện**: `http://localhost:5000/index.html`

### Tùy chọn 2: Chạy bằng Flask (Python)
1.  **Mở Terminal** tại thư mục `Week6`.
2.  **Cài đặt thư viện**: `pip install -r requirements.txt`
3.  **Khởi động Server**: `python3 app.py`
4.  **Truy cập Giao diện**: `http://localhost:5000/` (Flask tự động map root vào index.html)

---

## 2. Kịch Bản Thuyết Trình (Presentation Script)

### Bước 1: Giới thiệu (Introduction)
*   **Lời dẫn:** "Hôm nay tôi sẽ trình bày về cơ chế xác thực JWT và các rủi ro bảo mật đi kèm khi lưu trữ Token trên trình duyệt."
*   **Thao tác:** Mở giao diện demo trên trình duyệt. Chỉ vào các nút `Login`.

### Bước 2: Demo Đăng nhập không an toàn (Insecure Login)
*   **Lời dẫn:** "Đầu tiên, chúng ta sẽ thử nghiệm cách làm phổ biến nhưng **kém an toàn**: Lưu JWT vào `localStorage`."
*   **Thao tác:**
    1.  Nhập `username: admin`, `password: password123`.
    2.  Click **"Login (Insecure - LocalStorage)"**.
    3.  Giải thích: "Lúc này, Server trả về Token và Frontend lưu nó vào LocalStorage. Bạn có thể thấy Token hiện ra ở mục 'Current Access Token'."

### Bước 3: Mô phỏng tấn công XSS (Audit - Token Leakage)
*   **Lời dẫn:** "Giả sử trang web bị tấn công XSS, hacker có thể dễ dàng lấy cắp token này."
*   **Thao tác:**
    1.  Click nút **"Steal from LocalStorage"**.
    2.  Giải thích: "Chỉ với 1 dòng lệnh Javascript (`localStorage.getItem`), hacker đã lấy được toàn bộ mã xác thực của bạn. Từ đây, họ có quyền mạo danh bạn để gọi các API nhạy cảm."
    3.  Click **"Test Admin Access"** để chứng minh hacker vẫn có thể truy cập dữ liệu admin.

### Bước 4: Demo Đăng nhập an toàn (Secure Login)
*   **Lời dẫn:** "Để khắc phục, chúng ta sẽ sử dụng cơ chế **HttpOnly Cookie**."
*   **Thao tác:**
    1.  Click **"Logout"**.
    2.  Click **"Login (Secure - HttpOnly Cookie)"**.
    3.  Giải thích: "Lần này, Server không trả Token về qua body mà đặt trực tiếp vào Cookie với cờ `HttpOnly`. Hãy để ý mục 'Current Access Token' sẽ báo là 'Hidden in HttpOnly Cookie'."

### Bước 5: Kiểm chứng khả năng bảo vệ (Audit - Failure to Steal)
*   **Lời dẫn:** "Hãy xem hacker có làm gì được không."
*   **Thao tác:**
    1.  Click nút **"Steal from Cookie"**.
    2.  Giải thích: "Lần này hacker đã thất bại! Trình duyệt ngăn chặn mọi đoạn mã Javascript truy cập vào Cookie này. Đây là cách bảo vệ hiệu quả nhất chống lại lỗi rò rỉ token qua XSS."

---

## 3. Giải Thích Kỹ Thuật (Technical Deep Dive)

### Cơ chế JWT trong Code
- **`jwt.sign()`**: Dùng để tạo ra chuỗi mã hóa chứa thông tin người dùng (Payload) và chữ ký (Signature).
- **`jwt.verify()`**: Middleware ở backend kiểm tra tính hợp lệ của chữ ký trước khi cho phép truy cập tài nguyên.

### Tại sao HttpOnly Cookie lại an toàn?
| Đặc điểm | LocalStorage | HttpOnly Cookie |
| :--- | :--- | :--- |
| **Truy cập qua JS** | Có (Dễ bị XSS) | **Không** (An toàn trước XSS) |
| **Gửi kèm Request** | Phải code tay (`Authorization` Header) | Tự động gửi bởi trình duyệt |
| **Bảo vệ CSRF** | Tự nhiên an toàn | Cần cấu hình `SameSite` |

---

## 4. Bảng Kịch Bản Test (Test Cases)

Để bài thuyết trình thêm thuyết phục, bạn nên thực hiện các bài test biên sau:

| STT | Tình huống Test | Thao tác | Kết quả mong đợi | Giải thích |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Chưa đăng nhập | Click `Truy cập Profile` | Báo lỗi 401 | Hệ thống yêu cầu xác thực. |
| 2 | Sinh viên vào Admin | Đăng nhập tài khoản `user/password456`, click `Test Admin Access` | Báo lỗi 403 Forbidden | Đúng vai trò (student) nhưng không đủ quyền. |
| 3 | Admin vào Admin | Đăng nhập tài khoản `admin/password123`, click `Test Admin Access` | Thông báo thành công | Đúng vai trò và đủ quyền. |
| 4 | Kiểm tra XSS | Click `Steal from LocalStorage` (sau khi Login Insecure) | Lấy được Token | LocalStorage không an toàn. |
| 5 | Kiểm tra Security | Click `Steal from Cookie` (sau khi Login Secure) | Trả về `undefined` hoặc `null` | HttpOnly bảo vệ token hoàn hảo. |

---
*Người soạn thảo: Hà Vũ Công - 23020014*
