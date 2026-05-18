# Bài tập môn Kiến trúc Hướng Dịch vụ (INT3505)

Đây là repository lưu trữ bài tập cá nhân và các demo thực hành của môn học **Kiến trúc hướng dịch vụ** (Service-Oriented Architecture).

## Thông tin sinh viên
- **Họ và tên:** Hà Vũ Công
- **Mã sinh viên:** 23020014

## Nội dung thực hành (Course Content)

### Week 1: Introduction to APIs
- Tìm và phân tích các API công khai (Public REST APIs analysis).
- Demo trực quan với PokéAPI, REST Countries, và JSONPlaceholder.

### Week 2: Mocking & REST Basics
  - Giả lập cơ sở dữ liệu RESTful.
  - Tự động tạo các Error HTTP Codes phổ biến (400, 401, 403, 404, 500) thông qua Middleware.
  - Minh họa trực quan vấn đề **N+1 Query** và giải pháp **Eager Loading** (`?_expand=...`).

### Week 3: API Design Best Practices

- So sánh thiết kế API: "Bad" vs "Good" design.
- Áp dụng Versioning, Envelope patterns, và Pagination logic.
- Quản lý resource hierarchy và partial updates (PATCH).

### Week 4: API Specification & OpenAPI
- Tài liệu hóa API theo chuẩn **OpenAPI Specification (OAS)**.
- Demo tự động sinh Swagger UI từ Python Flask (sử dụng Flasgger).
- Xây dựng Schema chi tiết cho đối tượng `Book` (bao gồm trường `genre`).
- Kiểm thử tự động (Automated Testing) với bộ test case cho các CRUD operations.
- **Live Demo (Express API):** [https://expressdemo.vercel.app/api-docs/](https://expressdemo.vercel.app/api-docs/)

### Week 5: API Design & Resource Modeling
- Thiết kế Data Model (Entities & Attributes) cho hệ thống Quản lý Thư viện.
- Xây dựng Resource Tree và RESTful Endpoints (Nested resources).
- Phân tích và so sánh lý thuyết 3 chiến lược phân trang: Page-based, Offset-limit, và Cursor-based.

### Week 6: JWT Authentication & Security Audit
- Triển khai Xác thực (Authentication) và Phân quyền (Authorization - RBAC) bằng JWT.
- So sánh Access Token và Refresh Token.
- **Security Audit:** Demo thực tế rủi ro rò rỉ Token (XSS) khi lưu vào `localStorage` và giải pháp bảo mật với `HttpOnly Cookie`.

### Week 7: OpenAPI Server Generation
- Tự động sinh mã nguồn Server Stub (Python Flask & Connexion) từ định dạng OpenAPI Specification.
- Hỗ trợ chạy dịch vụ qua Docker và kiểm thử tích hợp tự động với `tox`.

### Week 8: API Testing & Quality Assurance
- Xây dựng bộ kiểm thử API tự động (Postman Collection & Newman CLI) cho các endpoint CRUD.
- Đo kiểm hiệu năng chịu tải (Load Testing) và phân tích Response Time, Error Rate với Locust.

### Week 9: API Versioning & Lifecycle Management
- Triển khai kịch bản thực tế 4 bước quản lý vòng đời API thanh toán (Coexist -> Deprecated -> Brownout -> Sunset).
- Xử lý Breaking Changes và thông báo cho nhà phát triển khi chuyển từ v1 sang v2.

### Week 10: Service Operation – Security & Monitoring
- Tích hợp các giải pháp bảo mật và giám sát hệ thống (Rate Limiting, Winston Logging, Prometheus Metrics).
- Triển khai mẫu thiết kế Circuit Breaker (Opossum) bảo vệ ứng dụng trước sự cố Cascading Failure từ các API bên ngoài.

### Week 11-12: API Design Patterns (Python Flask API)
- Triển khai và kết hợp nhiều mẫu thiết kế API hiện đại: CRUD, Query (Filtering/Sorting/Pagination), HATEOAS, Webhook và Event-driven bằng Python Flask.
- So sánh chi tiết các giao thức REST, gRPC, và GraphQL; phân tích thiết kế API thực tế của Stripe và GitHub.
- Xây dựng hệ thống gửi/nhận Webhook bảo mật với chữ ký xác thực HMAC SHA256 và tích hợp vào hệ thống thông báo.

### Comparative Studies & Benchmarks

#### [OpenAPI Comparison](./openapi-comparison)
- Phân tích và so sánh các định dạng tài liệu hóa API phổ biến: **OpenAPI (Swagger)**, **API Blueprint**, **RAML**, và **TypeSpec**.
- Minh họa cách thiết kế cùng một hệ thống trên 4 định dạng khác nhau.

#### [Pagination Benchmark](./Pagination_Benchmark)
- Thử nghiệm hiệu năng thực tế (Empirical Benchmarking) trên tập dữ liệu 1 triệu bản ghi.
- Chứng minh lợi thế vượt trội của **Cursor-based Pagination** (~200x lần) so với Offset-based khi xử lý dữ liệu lớn (Deep Paging).
