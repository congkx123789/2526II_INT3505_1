# Báo Cáo Thực Hành: Thiết Kế API Hệ Thống Quản Lý Thư Viện

Tài liệu này trình bày chi tiết phần thực hành thiết kế Data Model và RESTful API cho hệ thống quản lý thư viện, đồng thời so sánh các chiến lược phân trang (Pagination).

---

## Phần 1: Thiết Kế Data Model (Mô Hình Dữ Liệu)

Dưới đây là thiết kế các thực thể (Entities) và các trường dữ liệu (Attributes) cho Domain quản lý thư viện:

### 1. `books` (Sách)
*   **id** (UUID/String): Khóa chính.
*   **title** (String): Tên sách.
*   **isbn** (String): Mã số tiêu chuẩn quốc tế.
*   **published_year** (Integer): Năm xuất bản.
*   **quantity** (Integer): Số lượng sách có sẵn trong kho.
*   **author_id** (UUID/String): Khóa ngoại chỉ đến `authors`.
*   **category_id** (UUID/String): Khóa ngoại chỉ đến `categories`.

### 2. `users` (Độc giả)
*   **id** (UUID/String): Khóa chính.
*   **full_name** (String): Họ và tên độc giả.
*   **email** (String): Địa chỉ email.
*   **registered_at** (DateTime): Ngày đăng ký.

### 3. `loans` (Phiếu mượn)
*   **id** (UUID/String): Khóa chính.
*   **user_id** (UUID/String): Khóa ngoại chỉ đến `users`.
*   **book_id** (UUID/String): Khóa ngoại chỉ đến `books`.
*   **borrow_date** (DateTime): Ngày mượn.
*   **return_date** (DateTime): Ngày hạn trả.
*   **status** (Enum/String): `BORROWED` (Đang mượn), `RETURNED` (Đã trả), `OVERDUE` (Quá hạn).

**Mối quan hệ (Relationships):**
*   1 User có thể có N `loans` (1-N).
*   1 Book có thể nằm trong N `loans` (1-N).
*   (Loans chính là bảng trung gian trong quan hệ N-N giữa User và Book).

---

## Phần 2: Thiết Kế Resource Tree (RESTful Endpoints)

Ánh xạ mô hình dữ liệu thành các chuẩn REST API.

### Root Resources (Tài nguyên độc lập)
*   `GET /books`: Lấy danh sách sách (dùng cho tìm kiếm/phân trang).
*   `POST /books`: Thêm sách mới.
*   `GET /books/{id}`: Xem chi tiết sách.
*   `PUT /books/{id}`: Cập nhật thông tin sách.
*   `DELETE /books/{id}`: Xóa sách.
*   `GET /users`: Lấy danh sách độc giả.

### Sub-resources (Tài nguyên lồng nhau - Nested)
*   Thể hiện quan hệ **Độc giả có các phiếu mượn**:
    *   `GET /users/{id}/loans`: Lịch sử mượn sách của một độc giả cụ thể.
    *   `POST /users/{id}/loans`: Tạo yêu cầu mượn sách mới (Gắn liền với User).
*   Thể hiện quan hệ **Sách có các Tác giả**:
    *   `GET /books/{id}/authors`: Lấy thông tin tác giả của một quyển sách cụ thể.

---

## Phần 3: Thiết Kế Endpoint Tìm Kiếm và Phân Trang

### 3.1. Tìm kiếm (Search & Filter) & Sắp xếp (Sorting)
Đưa trực tiếp vào query parameters của endpoint danh sách:
*   **Tìm kiếm**: `GET /books?title=Harry&category=Fiction`
*   **Sắp xếp**: `GET /books?sort=-published_year` (Dấu `-` là sắp xếp giảm dần, không có dấu là tăng dần).

### 3.2. So Sánh và Phân Tích 3 Chiến Lược Phân Trang (Pagination)

Dưới đây là bảng so sánh các chiến lược phân trang áp dụng cho `GET /books`:

#### 1. Page-based (Dựa trên số trang)
*   **Cú pháp API**: `GET /books?page=1&size=20`
*   **Ưu điểm**:
    *   Cực kỳ thân thiện với UI truyền thống (hiển thị trang 1, 2, 3... Next, Prev).
    *   Dễ hiểu, dễ cài đặt cho Backend và Frontend.
    *   Người dùng có thể "nhảy" trực tiếp đến trang số 50 dễ dàng.
*   **Nhược điểm**:
    *   Hiệu năng giảm nghiêm trọng khi page rất lớn (Deep Pagination). DB phải tính toán và skip hàng triệu records trước khi lấy dữ liệu trang hiện tại.
    *   Lỗi lệch dữ liệu: Nếu có dữ liệu mới thêm/xóa khi đang chuyển trang, kết quả có thể bị trùng hoặc sót.

#### 2. Offset/Limit (Dựa trên độ lệch)
*   **Cú pháp API**: `GET /books?offset=0&limit=20`
*   **Ưu điểm**:
    *   Cú pháp gần giống với SQL nhất (`OFFSET x LIMIT y`), dễ code Backend.
    *   Cho phép "nhảy cóc" sang bất cứ block dữ liệu nào.
*   **Nhược điểm**:
    *   Hoàn toàn gặp phải 2 nhược điểm hệt như Page-based (Deep Pagination làm query chậm lại và lỗi lệch/trùng dữ liệu).

#### 3. Cursor-based (Dựa trên con trỏ)
*   **Cú pháp API**: `GET /books?cursor=eyJpZCI6MTIzfQ==&limit=20`
*   **Ưu điểm**:
    *   Hiệu suất truy vấn (Performance) cực kỳ xuất sắc và ổn định dù dữ liệu là trang 1 hay trang 1 triệu (vì sử dụng index để skip data).
    *   Ngăn chặn hoàn toàn lỗi trùng/sót dữ liệu khi DB bị thay đổi lúc đang cuộn.
    *   Đặc biệt hiệu quả cho tính năng "Infinite Scroll" (Cuộn vô hạn) trên App/Mobile.
*   **Nhược điểm**:
    *   Không cho phép "nhảy cóc" (Không thể nhảy 1 phát sang trang 50).
    *   Backend cài đặt phức tạp do phải sinh ra và giải mã token/cursor.

> **Kết luận cho dự án**: 
> Khuyến nghị sử dụng **Page-based** theo yêu cầu của đồ án học thuật thông thường, do nó trực quan và dễ trình bày trong báo cáo (Swagger/Postman). Tuy nhiên, nếu xây dựng hệ thống thật với hàng chục vạn cuốn sách (Deep dữ liệu), hệ thống sẽ cần nâng cấp sang **Cursor-based**.
