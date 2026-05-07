# Week 10: Service Operation – Security & Monitoring

Dự án này minh họa cách thiết lập Security (Rate Limiting), Monitoring (Logging, Metrics), và Resilience (Circuit Breaker) cho một ứng dụng Node.js/Express.

## 1. Cấu trúc thư mục
```text
Week10/
├── src/
│   ├── middlewares/
│   │   ├── rateLimiter.js     # Chặn spam request (express-rate-limit)
│   │   └── auditLog.js        # Ghi log mọi request (Winston + Prometheus)
│   ├── services/
│   │   └── dataService.js     # Circuit Breaker gọi API ngoài (Opossum)
│   ├── utils/
│   │   ├── logger.js          # Cấu hình Winston
│   │   └── metrics.js         # Cấu hình Prometheus (prom-client)
│   └── app.js                 # File chạy chính
└── package.json
```

## 2. Cách chạy
1. Cài đặt dependencies:
   ```bash
   npm install
   ```
2. Chạy server:
   ```bash
   node src/app.js
   ```

## 3. Cách test
- **Rate Limiting**: Truy cập `http://localhost:3000/api/ping`. Nếu reload quá 3 lần trong 10 giây, bạn sẽ nhận được thông báo lỗi bảo mật.
- **Logging**: Kiểm tra file `logs/audit.log` để xem lịch sử các request.
- **Metrics**: Truy cập `http://localhost:3000/metrics` để xem các thông số hệ thống và số lượng request.
- **Circuit Breaker**: Truy cập `http://localhost:3000/api/unstable`. Đây là endpoint giả lập lỗi. Nếu lỗi xảy ra quá nhiều (>50%), Circuit Breaker sẽ ngắt mạch và trả về dữ liệu Fallback ngay lập tức.

## 4. Kiến thức đạt được
- **Observability**: Logging (Winston) & Metrics (Prometheus).
- **Security**: Rate limiting để chống Brute-force/Spam.
- **Resilience**: Circuit Breaker để bảo vệ hệ thống khỏi các dịch vụ bên ngoài bị lỗi (Cascading failure).
