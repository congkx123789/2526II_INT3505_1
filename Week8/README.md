# Buổi 8: API Testing và Quality Assurance

Trong buổi học này, chúng ta sẽ tìm hiểu về kiểm thử API và đảm bảo chất lượng phần mềm, bao gồm các loại test (unit, integration, performance) và cách đo hiệu năng.

## Kiến thức cần đạt
- **Các loại test**: unit test, integration test, và performance test.
- **Công cụ**: Postman, Newman (để chạy Postman tự động CLI), và load testing tools (Locust).
- **Kỹ năng**:
  - Viết bộ test tự động cho các endpoint.
  - Đo hiệu năng API (response time, error rate).

## Tài liệu đọc trước
- **JJ Geewax** – Chương 6: API Testing.

---

## Thực hành: Xây dựng và kiểm thử API

Thư mục này chứa sẵn một API Server giả lập (viết bằng Python & Flask) cung cấp 5 endpoint để bạn có thể thực hành.

### 1. Chuẩn bị

Mở Terminal tại thư mục `Week8/` và cài đặt các thư viện cần thiết:

Tạo môi trường ảo (Virtual Environment) và cài đặt dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Khởi động API Server:
```bash
python app.py
```
Server sẽ chạy ở địa chỉ: `http://localhost:3000`

### 2. Tạo test suite trong Postman cho 5 endpoints

Trong thư mục đã có file `postman_collection.json`. Đây là bộ test mẫu cho 5 endpoint mô phỏng thao tác CRUD trên tài nguyên `tasks` (Công việc). Bạn có thể import file `postman_collection.json` vào phần mềm Postman để xem chi tiết.

Các endpoint bao gồm:
1. `GET /api/tasks` - Lấy danh sách task (Kỳ vọng Status: 200)
2. `POST /api/tasks` - Tạo mới task (Kỳ vọng Status: 201)
3. `GET /api/tasks/:id` - Lấy thông tin 1 task (Kỳ vọng Status: 200)
4. `PUT /api/tasks/:id` - Cập nhật task (Kỳ vọng Status: 200)
5. `DELETE /api/tasks/:id` - Xóa task (Kỳ vọng Status: 204)

### 3. Chạy test tự động bằng Newman

Khi dự án đưa lên CI/CD, chúng ta cần chạy Postman Tests tự động thông qua giao diện dòng lệnh (CLI). Postman cung cấp công cụ có tên là `newman`.

Biên dịch script chạy newman (không cần package.json) thông qua `npx`:
Mở một cửa sổ Terminal mới và chạy:
```bash
npx newman run postman_collection.json
```

Kết quả in ra màn hình sẽ hiển thị số lượng requests đã chạy cùng các test (assertions), thông báo tình trạng passed/failed.

### 4. Đo hiệu năng API bằng load testing tool (Locust)

Thử nghiệm tải (Load Test) sẽ gửi một lượng lớn request đồng thời vào API để đo được `response time`, `throughput`, và `error rate`.

Với Python, chúng ta sử dụng `locust` (đã cài chung trong requirements.txt).
Khởi động Locust:
```bash
locust -f locustfile.py
```

Truy cập vào giao diện Locust tại `http://localhost:8089/`, điền `Number of users` là 100, `Hatch rate` là 10. Điền Host là `http://localhost:3000` và nhấn **Start swarming**.

Bạn có thể theo dõi biểu đồ Response Time, Errors, RPS (Requests Per Second) theo thời gian thực để từ đó đánh giá hiệu năng chịu tải của API.
