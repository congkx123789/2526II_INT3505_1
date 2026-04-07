# Hướng Dẫn Chạy Demo Week 5: Library Management API

Tài liệu này hướng dẫn cách cài đặt và chạy hệ thống API Quản lý Thư viện bằng cả hai ngôn ngữ: **Node.js (Express)** và **Python (Flask)**.

---

## 1. Tổng quan Dự án

Hệ thống này mô phỏng một API RESTful để quản lý Sách, Độc giả và Phiếu mượn. Mục tiêu chính là trình bày các kỹ thuật API nâng cao:
- **Search (Tìm kiếm)**: Tìm theo tiêu đề.
- **Filtering (Lọc)**: Lọc theo thể loại, tác giả.
- **Sorting (Sắp xếp)**: Sắp xếp theo năm xuất bản (tăng/giảm).
- **Pagination (Phân trang)**: Hỗ trợ hai chiến lược là `Page-based` và `Offset/Limit`.

---

## 2. Tại sao lại có cả Node.js và Python?

Dự án cung cấp hai phiên bản mã nguồn tương đương nhau:
1.  **Node.js (Express) - `server.js`**: Chạy trên cổng **3001**. Phổ biến trong phát triển Web Backend tốc độ cao.
2.  **Python (Flask) - `app.py`**: Chạy trên cổng **5001**. Phổ biến trong khoa học dữ liệu và các dịch vụ API đơn giản, dễ đọc.

Việc có cả hai phiên bản giúp bạn so sánh cách triển khai cùng một logic nghiệp vụ (Business Logic) trên hai hệ sinh thái khác nhau, nhưng vẫn đảm bảo cấu trúc API đồng nhất (cùng Endpoint, cùng định dạng JSON).

---

## 3. Cách chạy bản Node.js (Express)

### Bước 1: Cài đặt dependencies
Mở terminal tại thư mục `Week5` và chạy:
```bash
npm install
```

### Bước 2: Khởi chạy Server
```bash
npm start
```
*Server sẽ chạy tại: `http://localhost:3001`*

### Bước 3: Kiểm tra API
Bạn có thể mở trình duyệt hoặc dùng Postman truy cập:
- Danh sách sách: [http://localhost:3001/books](http://localhost:3001/books)
- Tìm kiếm & Phân trang: [http://localhost:3001/books?title=Harry&page=1&size=2&sort=-published_year](http://localhost:3001/books?title=Harry&page=1&size=2&sort=-published_year)

---

## 4. Cách chạy bản Python (Flask)

### Bước 1: Cài đặt dependencies
Đảm bảo bạn đã cài Python, sau đó chạy:
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi chạy Server
```bash
python app.py
```
*Server sẽ chạy tại: `http://localhost:5000`*

### Bước 3: Kiểm tra API
- Danh sách sách: [http://localhost:5000/books](http://localhost:5000/books)
- Thử nghiệm các tham số tương tự như bản Node.js để thấy sự đồng nhất.

---

## 5. Chạy Unit Test (Kiểm thử tự động)

Dự án đi kèm file `test_api.py` để kiểm tra tính đúng đắn của logic (đặc biệt là phân trang và tìm kiếm).
Chạy lệnh sau:
```bash
python test_api.py
```
Nếu kết quả hiện `OK`, nghĩa là logic API của bạn đã chuẩn xác.

---

## 💡 Lưu ý quan trọng
- **Xung đột cổng**: Server đã được đổi sang cổng **3001** để tránh xung đột với các dịch vụ khác đang chạy trên cổng 3000.
- **Mock Data**: Cả hai phiên bản đều dùng dữ liệu giả lập (in-memory). Nếu bạn tắt server, các dữ liệu `POST` thêm mới sẽ bị mất.
