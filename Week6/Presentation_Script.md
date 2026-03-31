# Kịch Bản Thuyết Trình: Cấu Trúc 20 Slide (Buổi 6)
**Chủ đề: Authentication & Authorization (JWT vs OAuth 2.0 & Thực hành Node.js)**

Đây là kịch bản chi tiết cho 20 slide. Dưới mỗi slide đều có Text giải thích, Text rải trên slide (Bullet points) và **hướng dẫn đoạn code cần chụp** từ project thực tế của bạn.

---

## PHẦN 1: GIỚI THIỆU & LÝ THUYẾT NỀN TẢNG

### Slide 1: Trang bìa (Title Slide)
*   **Tiêu đề lớn:** Buổi 6: Authentication và Authorization
*   **Tiêu đề phụ:** Quản lý danh tính và Phân quyền trong kiến trúc ứng dụng hiện đại (Microservices)
*   **Người trình bày:** [Tên của bạn]

### Slide 2: Mục tiêu bài học (Agenda)
*   **Nội dung trên slide (Bullet points):**
    *   Sự khác biệt giữa Xác thực (Authentication) & Phân quyền (Authorization).
    *   So sánh JWT và OAuth 2.0.
    *   Các khái niệm cốt lõi: Bearer token, Refresh token, Scopes, Roles.
    *   Thực hành: Triển khai JWT trên Node.js.
    *   Security Audit: Rủi ro Token Leakage & Replay Attack.
*   **Giải thích (Khi thuyết trình):** "Hôm nay chúng ta sẽ đi từ định nghĩa cơ bản nhất, đến cách triển khai thực tế bằng mã nguồn Node.js, và cuối cùng là đóng vai một hacker để xem hệ thống của chúng ta dễ bị tấn công như thế nào nếu không làm đúng chuẩn."

### Slide 3: Authentication vs. Authorization
*   **Nội dung trên slide:**
    *   **Authentication (Ai?):** Xác minh danh tính người dùng (VD: Login bằng Username/Password). Hỏi: "Bạn là ai?"
    *   **Authorization (Được làm gì?):** Kiểm tra quyền hạn truy cập tài nguyên (VD: Quyền Admin, Quyền User). Hỏi: "Bạn có quyền làm việc này không?"
*   **Giải thích:** "Xác thực là cái vé vào cổng khu vui chơi. Còn Phân quyền là việc cái vé đó có cho phép bạn chơi tàu lượn siêu tốc hay chỉ được bơi ở hồ bơi trẻ em. Chúng là 2 bước tách biệt nhưng luôn đi liền với nhau."

### Slide 4: Tại sao cần Token-based Auth trong Microservices?
*   **Nội dung trên slide:**
    *   **Session-based (Truyền thống):** Server lưu trạng thái (Stateful), khó mở rộng (Scale).
    *   **Token-based (Hiện đại):** Server không lưu trạng thái (Stateless). Khách hàng giữ Token.
*   **Giải thích:** "Trong hệ thống Microservice có hàng chục backend con, nếu dùng Session lưu ở RAM server, khi request bay sang server khác sẽ bị mất session. Token giải quyết bài toán này vì nó tự chứa thông tin, các server chỉ cần xác minh chữ ký."

### Slide 5: JWT (JSON Web Token) là gì?
*   **Nội dung trên slide:**
    *   Bản chất: Một định dạng chuỗi mã hóa nhỏ gọn để truyền dữ liệu an toàn.
    *   Cấu trúc 3 phần: `Header` (Thuật toán) . `Payload` (Dữ liệu/Claims) . `Signature` (Chữ ký điện tử).
*   **Giải thích:** "JWT giống như một chứng minh thư số. Payload chứa tên, role của user. Việc làm giả dữ liệu trong Payload là bất khả thi nếu không có Secret Key của backend nhờ vào phần Signature."

### Slide 6: So sánh JWT vs OAuth 2.0
*   **Nội dung trên slide:**
    *   **JWT:** Là một **định dạng** (Format) của token. Dùng để truyền tin an toàn.
    *   **OAuth 2.0:** Là một **tiêu chuẩn/giao thức** (Protocol). Cung cấp luồng (Flow) để cấp quyền cho bên thứ 3 (VD: "Login with Google").
*   **Giải thích:** "Nhiều người hay nhầm chúng là đối thủ của nhau. Thực chất, OAuth 2.0 quy định cách bạn 'đăng nhập qua Google', còn cái rốt cuộc mà Google trả về cho server của bạn thường chính là một cái JWT. Một bên là quy trình, một bên là kết quả."

---

## PHẦN 2: CÁC KHÁI NIỆM CỐT LÕI

### Slide 7: Bearer Token
*   **Nội dung trên slide:**
    *   Định nghĩa: "Token của người mang nó". (Whoever holds it can use it).
    *   Header HTTP: `Authorization: Bearer <token_string>`
*   **Giải thích:** "Bearer có nghĩa là 'người mang'. Nếu bạn mất thẻ Bearer này vào tay người khác, họ sẽ có toàn quyền như bạn. Server không quan tâm ai gửi request, cứ có thẻ là cho vào."

### Slide 8: Nỗi lo lộ Token và giải pháp Refresh Token
*   **Nội dung trên slide:**
    *   **Access Token:** Tuổi thọ ngắn (5-15 phút). Dùng để gọi API.
    *   **Refresh Token:** Tuổi thọ dài (Ví dụ: 7 ngày, 30 ngày). Dùng để đổi lấy Access Token mới khi thẻ cũ hết hạn.
*   **Giải thích:** "Vì Bearer Token nguy hiểm nếu lộ, ta ép Access Token sống cực ngắn (15p). Lỡ trộm lấy được, 15p sau token cũng vô dụng. Nhưng bắt User đăng nhập lại mỗi 15p thì quá tệ, ta sinh ra Refresh Token (lưu an toàn) để tự động xin lại thẻ Access ngầm bên dưới."

### Slide 9: Luồng hoạt động Access & Refresh Token
*   **Nội dung trên slide:**
    *   Sơ đồ step-by-step:
        1. Login -> Trả về Access + Refresh.
        2. Dùng Access gọi API -> OK.
        3. 15 phút sau -> Access hết hạn, Server báo 401.
        4. Gửi Refresh Token -> Trả về Access Token mới.
*   **Giải thích:** "Đây là flow chuẩn của mọi ứng dụng lớn hiện tại như Facebook, Google."

### Slide 10: Phân Quyền: Scopes vs Roles
*   **Nội dung trên slide:**
    *   **Role (Vai trò của người dùng):** VD: `admin`, `student`. (Ai được làm gì trong tổ chức).
    *   **Scope (Phạm vi của ứng dụng):** VD: `read:profile`, `write:email`. (Ứng dụng client được uỷ quyền làm gì thay bạn).
*   **Giải thích:** "Role thiên về hệ thống nội bộ, Scope thường thấy trong OAuth2 khi ứng dụng bên thứ 3 xin quyền truy cập vào tài khoản của bạn (VD muốn đăng bài thay bạn hay chỉ muốn xem avatar)."

---

## PHẦN 3: TRIỂN KHAI BACKEND (THỰC HÀNH NODE.JS)

### Slide 11: Tổng quan dự án kiến trúc Auth
*   **Nội dung trên slide:**
    *   Ngôn ngữ: Node.js (Express Framework).
    *   Thư viện: `jsonwebtoken` (Xử lý JWT), `cookie-parser` (Xử lý Cookie bảo mật).
    *   Frontend: Giao diện test audit (Hacker Simulator).
*   **Giải thích:** "Chúng ta sẽ xem xét cách viết code trên Node.js để quản lý JWT, đồng thời mình có viết một cái file HTML đóng vai trò cả người dùng bình thường và Hacker để test hệ thống."

### Slide 12: Bước 1 - Database và Secret Key
*   **Nội dung trên slide:** Giả lập dữ liệu người dùng có các Roles và Scopes khác nhau. Quy định key bí mật.
*   **📷 Chụp ảnh code `server.js`:** Chụp đoạn từ dòng `const SECRET_KEY = ...` đến hết biến `const users = {...};` (Khoảng dòng 8 đến 31).
*   **Giải thích:** "Đây là Mock database. Admin sẽ có role 'admin' và nhiều scopes. Chúng ta cũng cấu hình SECRET_KEY, là chìa khóa duy nhất dùng để ký và giải mã Token."

### Slide 13: Bước 2 - Thiết kế Endpoint Login tạo JWT
*   **Nội dung trên slide:** Sử dụng hàm `jwt.sign()` để tạo Access Token (15p) và Refresh Token (7 ngày).
*   **📷 Chụp ảnh code `server.js`:** Chụp đoạn `app.post('/api/login-insecure', ...)` (Khoảng dòng 65 đến 78).
*   **Giải thích:** "Sau khi check đúng username pass, server đóng gói id, role vào payload và dùng SECRET_KEY để ký token. Ở endpoint này, mình cố tình trả Token dưới dạng JSON text thẳng về Client."

### Slide 14: Bước 3 - Middleware Xác Thực (Authentication)
*   **Nội dung trên slide:** Kiểm tra xem request có mang theo Bearer Token hợp lệ hay không.
*   **📷 Chụp ảnh code `server.js`:** Chụp hàm `const verifyToken = ...` (Khoảng dòng 33 đến 51).
*   **Giải thích:** "Đây là cái chốt bảo vệ ở cửa. Request đi vào phải qua middleware này. Hàm `jwt.verify` kiểm tra chữ ký. Nếu chữ ký sai hoặc token đã hết hạn, chặn ngay lập tức."

### Slide 15: Bước 4 - Middleware Phân Quyền (RBAC - Roles)
*   **Nội dung trên slide:** Kiểm tra sau khi lọt qua cửa, Role của người dùng có đủ thẩm quyền vào phòng VIP hay không.
*   **📷 Chụp ảnh code `server.js`:** Chụp hàm `const authorizeRoles = ...` (Khoảng dòng 53 đến 61). VÀ đoạn tạo route `app.get('/api/admin-only'...)` (khoảng dòng 112).
*   **Giải thích:** "Khi verify thành công, giải mã JWT ta biết đây là 'admin' hay 'student'. Middleware `authorizeRoles('admin')` đảm bảo nếu mạo danh, request sẽ bị đá ra với mã lỗi 403 Forbidden."

---

## PHẦN 4: SECURITY AUDIT & KHẮC PHỤC RỦI RO

### Slide 16: Security Audit (Kiểm tra An Ninh) là gì?
*   **Nội dung trên slide:**
    *   Rủi ro 1: Token Leakage (Lộ/Đánh cắp token từ Browser).
    *   Rủi ro 2: Replay Attack (Tấn công phát lại trên đường truyền).
*   **Giải thích:** "Viết code chạy được là 1 chuyện. Code an toàn hay không là chuyện khác. Với tư cách kỹ sư bảo mật bài học này, chúng ta sẽ bắt bệnh phần code vừa rồi."

### Slide 17: Rủi ro 1 - Token Leakage (Tấn công XSS)
*   **Nội dung trên slide:**
    *   Thói quen xấu: Frontend dev hay lưu token vào `localStorage`.
    *   Tấn công: Cross-Site Scripting (XSS). Kẻ xấu chèn script độc JS vào web và đọc localStorage.
*   **📷 Chụp ảnh code `index.html`:** Chụp phần hàm hacker: `function stealFromLocalStorage()` (Khoảng dòng 130 đến 141).
*   **Giải thích:** "Đây là hàm mô phỏng chiêu của hacker. Chỉ một dòng lệnh `localStorage.getItem('access_token')`, mọi bí mật của bạn đã bị gửi đi nơi khác."

### Slide 18: Giải pháp - Đăng nhập An Toàn với HttpOnly Cookie
*   **Nội dung trên slide:** Cất token vào ngăn kéo mà Javascript không thể chạm tới.
*   **📷 Chụp ảnh code `server.js`:** Chụp đoạn `app.post('/api/login-secure', ...)` (Khoảng dòng 80 đến 99), đặc biệt focus vào `res.cookie(..., { httpOnly: true })`.
*   **Giải thích:** "Sửa sai! Đừng trả token qua payload rồi bắt client lưu. Backend có quyền ép trình duyệt lưu thành cục Cookie với cờ `HttpOnly: true`. Cờ này có nghĩa là cọc chết, cấm Javascript đọc nó."

### Slide 19: Kết quả Audit HttpOnly Cookie (Demo)
*   **Nội dung trên slide:** Javascript của Hacker trở nên mù lòa trước `HttpOnly`.
*   **📷 Chụp ảnh code `index.html`:** Chụp phần hàm `function stealFromCookie()` (Khỏang dòng 143 đến 153).
*   **Giải thích:** "Lúc này, hacker dùng lệnh `document.cookie` để mò mẫm, nhưng trình duyệt đã giấu Token đi. Mã độc thất bại, hệ thống của ta an toàn trước XSS."

### Slide 20: Rủi ro 2 - Replay Attack & Best Practices
*   **Nội dung trên slide:** Kẻ xấu nghe lén wifi quán cafe (Man-in-The-Middle), túm được cái gói tin chứa token và gửi lại y chang.
*   **Khắc phục (Best Practices):**
    1.  Bắt buộc triển khai cấu hình **HTTPS/TLS** (mã hóa toàn bộ đường truyền, kẻ gian lấy được rác).
    2.  Token TTL: Access Token tuổi thọ thật ngắn (Ví dụ 5 phút).
    3.  Thêm Unique ID (JTI) vào payload JWT để tra soát xem token đã xài chưa.
*   **Giải thích:** "Qua case audit này, bài học rút ra là: JWT rất mạnh, nhưng nếu lưu trữ sai trên Client (để vào LocalStorage) và không cấu hình HTTPS, nó giống như đi xe xịn mà cắm sẵn chìa khóa vậy. Xin cảm ơn thầy cô và các bạn."
