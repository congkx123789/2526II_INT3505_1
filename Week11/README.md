# Buổi 11-12: API Design Patterns

Dự án này minh họa cách thiết kế và triển khai một hệ thống API hiện đại kết hợp nhiều mẫu thiết kế (Design Patterns) phổ biến trong thực tế: **CRUD**, **Query (Filtering/Sorting/Pagination)**, **HATEOAS**, **Event-driven**, và **Webhook**. 

---

## 1. Mục lục
1. [Cấu trúc thư mục](#1-cấu-trúc-thư-mục)
2. [Các API Design Patterns được triển khai](#2-các-api-design-patterns-được-triển-khai)
3. [So sánh: Khi nào dùng REST, gRPC, hay GraphQL?](#3-so-sánh-khi-nào-dùng-rest-grpc-hay-graphql)
4. [Phân tích Case Study: Stripe & GitHub API Patterns](#4-phân-tích-case-study-stripe--github-api-patterns)
5. [Hướng dẫn cài đặt & Chạy demo](#5-hướng-dẫn-cài-đặt--chạy-demo)
6. [Kịch bản kiểm thử (Test Scenarios)](#6-kịch-bản-kiểm-thử-test-scenarios)

---

## 1. Cấu trúc thư mục

```text
Week11/
├── routes/
│   ├── orders.py              # CRUD, Query, HATEOAS, Kích hoạt Event Webhook
│   └── webhooks.py            # Đăng ký Webhook, Nhận Webhook, Xử lý Thông báo
├── services/
│   ├── notification_service.py# Quản lý danh sách thông báo hệ thống
│   └── webhook_service.py     # Gửi Webhook bằng luồng riêng với chữ ký HMAC SHA256
├── database.py                # Mock DB lưu đơn hàng, Webhook URL, Thông báo
├── app.py                     # Cấu hình Flask API server chính
├── requirements.txt           # Danh sách thư viện Python
├── postman_collection.json    # Bộ Postman Collection kiểm thử tự động
└── README.md
```

---

## 2. Các API Design Patterns được triển khai

### 2.1. CRUD (Create - Read - Update - Delete)
- Các thao tác chuẩn hóa trên tài nguyên `Order` tuân thủ nguyên tắc HTTP methods và Status codes:
  - `POST /api/orders` (201 Created)
  - `GET /api/orders` (200 OK)
  - `GET /api/orders/:id` (200 OK hoặc 404 Not Found)
  - `PUT /api/orders/:id` (200 OK)
  - `DELETE /api/orders/:id` (200 OK)

### 2.2. Query Pattern (Filtering, Sorting, Pagination)
- Khi dữ liệu lớn, endpoint `GET /api/orders` hỗ trợ các tham số truy vấn nâng cao:
  - **Filtering**: `?status=PAID` (Lọc các đơn hàng đã thanh toán)
  - **Sorting**: `?sortBy=amount&order=DESC` (Sắp xếp theo số tiền giảm dần)
  - **Pagination**: `?page=1&limit=2` (Phân trang với kích thước trang là 2)
- Server trả về đầy đủ metadata phân trang (`totalItems`, `totalPages`, `currentPage`).

### 2.3. HATEOAS (Hypermedia As The Engine Of Application State)
- Mỗi phản hồi từ API đều kèm theo thuộc tính `_links` giúp client tự khám phá các hành động tiếp theo có thể thực hiện mà không cần hardcode URL:
```json
"_links": {
  "self": { "href": "http://localhost:3000/api/orders/ORD-001", "method": "GET" },
  "update": { "href": "http://localhost:3000/api/orders/ORD-001", "method": "PUT" },
  "delete": { "href": "http://localhost:3000/api/orders/ORD-001", "method": "DELETE" },
  "pay": { "href": "http://localhost:3000/api/orders/ORD-001/pay", "method": "POST" }
}
```

### 2.4. Event-Driven & Webhook Pattern
- **Bản chất**: Khi một sự kiện quan trọng xảy ra trong hệ thống (như tạo đơn hàng mới `order.created` hay thanh toán thành công `payment.success`), hệ thống tự động phát sự kiện (Event-driven).
- **Webhook Dispatcher (`webhookService.js`)**: Quét danh sách các URL đã đăng ký nhận sự kiện này và thực hiện HTTP POST bất đồng bộ tới các URL đó.
- **Bảo mật Webhook (HMAC SHA256 Signature)**:
  - Tương tự Stripe và GitHub, mỗi payload webhook gửi đi đều kèm theo một chữ ký mã hóa trong header `X-Webhook-Signature` được tạo từ `Secret Key`.
  - Bên nhận (Receiver) sử dụng cùng `Secret Key` để kiểm chứng tính xác thực của dữ liệu trước khi xử lý.

---

## 3. So sánh: Khi nào dùng REST, gRPC, hay GraphQL?

| Tiêu chí | REST API | GraphQL | gRPC |
| :--- | :--- | :--- | :--- |
| **Giao thức** | HTTP/1.1 hoặc HTTP/2 | HTTP/1.1 hoặc HTTP/2 | **HTTP/2 bắt buộc** |
| **Định dạng dữ liệu** | JSON / XML | JSON | **Protocol Buffers (Binary)** |
| **Tốc độ / Hiệu năng** | Trung bình | Trung bình (có thể bị N+1 query) | **Cực kỳ nhanh (x7-10 lần JSON)** |
| **Tính linh hoạt** | Server quyết định cấu trúc dữ liệu trả về | **Client yêu cầu chính xác các trường cần thiết** | Định nghĩa chặt chẽ qua file `.proto` |
| **Hỗ trợ Streaming** | Hạn chế (SSE/WebSockets) | Subscriptions (WebSockets) | **Hỗ trợ Native Bi-directional Streaming** |
| **Trường hợp sử dụng lý tưởng** | - API công cộng (Public API)<br>- Web/Mobile App thông thường<br>- Chuẩn hóa CRUD | - Hệ thống có nhiều quan hệ dữ liệu phức tạp<br>- Tránh Over-fetching / Under-fetching cho Mobile | - Giao tiếp nội bộ giữa các Microservices (Inter-service communication)<br>- Hệ thống IoT, Real-time |

---

## 4. Phân tích Case Study: Stripe & GitHub API Patterns

### 4.1. Phân tích API của Stripe (Payment Gateway)
1. **Idempotency (Tính lũy đẳng)**:
   - Thách thức: Trong thanh toán, nếu mạng bị lag và client gửi request `POST /charges` 2 lần, khách hàng có thể bị trừ tiền 2 lần.
   - Pattern của Stripe: Sử dụng header `Idempotency-Key: <UUID>`. Stripe lưu key này trong 24h. Nếu nhận lại request có cùng key, Stripe trả về ngay kết quả đã lưu trữ trước đó mà không thực hiện lại giao dịch.
2. **Cursor-based Pagination**:
   - Thay vì dùng `page` và `offset` (gây chậm khi offset lớn hoặc lặp/sót dữ liệu nếu DB thay đổi), Stripe sử dụng `starting_after` và `ending_before` dựa trên ID của object cuối cùng.
3. **Webhook Verification**:
   - Gửi header `Stripe-Signature: t=<timestamp>,v1=<hash>`. Client dùng secret key để băm HMAC SHA256 xác thực.

### 4.2. Phân tích API của GitHub
1. **HATEOAS / Link Header Pagination**:
   - GitHub trả về thông tin phân trang trong HTTP Header `Link: <https://api.github.com/...?page=2>; rel="next"`.
2. **REST & GraphQL Dual Support**:
   - GitHub cung cấp cả v3 REST API và v4 GraphQL API, cho phép các bên thứ ba tối ưu truy vấn dữ liệu theo nhu cầu.
3. **Event Payload & Webhook Delivery**:
   - Gửi webhook với header `X-Hub-Signature-256`. Hỗ trợ chức năng "Redeliver" (Gửi lại webhook nếu server client bị sập).

---

## 5. Hướng dẫn cài đặt & Chạy demo

### 5.1. Cài đặt
Di chuyển vào thư mục `Week11`, tạo môi trường ảo (Virtual Environment) và cài đặt các thư viện Python:
```bash
cd Week11
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5.2. Khởi động Server
```bash
source venv/bin/activate
python app.py
```
Server sẽ chạy tại địa chỉ: `http://localhost:3000`

---

## 6. Kịch bản kiểm thử (Test Scenarios)

> [!TIP]
> Trong thư mục `Week11` đã có sẵn tệp [postman_collection.json](./postman_collection.json) chứa 10 kịch bản kiểm thử chuẩn hóa. Bạn có thể import trực tiếp tệp này vào phần mềm Postman để thực hành và kiểm chứng toàn bộ luồng hoạt động ngay lập tức.

Bạn cũng có thể sử dụng cURL hoặc trình duyệt theo các bước sau:

### Bước 1: Khám phá API Root (HATEOAS)
- **Request**: `GET http://localhost:3000/`
- **Kết quả**: Bạn sẽ thấy danh sách các endpoint khả dụng trong thuộc tính `_links`.

### Bước 2: Thử nghiệm Query Pattern (Filter, Sort, Pagination)
- **Request**: `GET http://localhost:3000/api/orders?status=PAID&sortBy=amount&order=DESC&page=1&limit=2`
- **Kết quả**: Trả về 2 đơn hàng có trạng thái `PAID`, sắp xếp số tiền từ cao xuống thấp kèm metadata phân trang.

### Bước 3: Đăng ký Webhook (Subscribe)
Hệ thống đã cấu hình sẵn 1 subscriber trỏ về `http://localhost:3000/api/webhooks/receiver` để bạn dễ test. Bạn có thể đăng ký thêm:
- **Request**: `POST http://localhost:3000/api/webhooks/subscribe`
- **Body** (JSON):
```json
{
  "url": "http://localhost:3000/api/webhooks/receiver",
  "events": ["order.created", "payment.success"],
  "secret": "whsec_supersecretkey123"
}
```

### Bước 4: Tạo đơn hàng mới & Xem Webhook hoạt động (Event-Driven)
- **Request**: `POST http://localhost:3000/api/orders`
- **Body** (JSON):
```json
{
  "customer": "Hoàng Nam",
  "product": "Khóa học Kiến trúc Hệ thống Phân tán",
  "amount": 4500000
}
```
- **Trên Terminal Console của Server**:
  - Bạn sẽ thấy log `[Webhook Dispatcher]` tạo chữ ký HMAC SHA256 và gửi HTTP POST tới endpoint receiver.
  - Ngay sau đó, log `[Webhook Receiver]` xác thực chữ ký thành công và đưa vào hệ thống thông báo.

### Bước 5: Thực hiện Thanh toán & Kiểm tra Thông báo tích hợp
- Lấy `id` đơn hàng vừa tạo (ví dụ `ORD-123456789`).
- **Request**: `POST http://localhost:3000/api/orders/ORD-123456789/pay`
- Sự kiện `payment.success` sẽ được phát và gửi qua Webhook.

### Bước 6: Kiểm tra Hệ thống Thông báo (Notification Integration)
- **Request**: `GET http://localhost:3000/api/notifications`
- **Kết quả**: Trả về danh sách thông báo, trong đó ghi nhận rõ các sự kiện tạo đơn hàng, thanh toán, và các sự kiện được tiếp nhận qua Webhook.
