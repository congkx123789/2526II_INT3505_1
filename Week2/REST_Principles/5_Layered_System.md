# 5. Layered System (Hệ thống phân lớp)

## 📖 Khái niệm
Client thường không thể (hoặc không cần thiết) phân biệt được nó đang giao tiếp trực tiếp với Server thực thi cuối cùng (End-Server) hay là đang giao tiếp thông qua một máy chủ trung gian qua nhiều lớp (Load Balancer, API Gateway, Firewall, Proxy, Cache Server).
Bằng cách phân lớp, chúng ta đóng gói và ẩn đi độ phức tạp của Server bên trong mạng nội bộ, đồng thời thực thi được các tính năng bảo mật độc lập trong từng lớp.

## 🚀 Lợi ích
- **Tính bảo mật:** Lớp ngoài cùng (Gateway/Proxy) có thể cản phá tấn công DDoS hoặc chặn các IP xấu trước khi Request chạm tới Server chính mang mã nguồn và Database.
- **Cân bằng tải (Load Balancing):** Một Proxy trung gian nhận request và phân chia cho 10 máy chủ NodeJS đằng sau.
- **Microservices Routing:** API Gateway nhận `api.domain.com/users` chuyển vào cụm máy chủ User, nhận khoảng `/orders` chuyển về cụm máy chủ Order.

---

## 💻 Ví dụ chi tiết biểu diễn Hệ thống phân lớp

Không có một "đoạn code chuẩn" cho nguyên tắc này vì bản chất của Layered System nằm ở việc **triển khai hạ tầng (Infrastructure) & Web Server** chứ không phải ở App code. 

### Mô hình Layered System thực tế:
```text
(1) User Browsers (React App)
        |
    [HTTP Request]
        |
(2) NGINX/Cloudflare (Lớp 1: Reverse Proxy & Firewall, CDN Cache)
        | Chặn IP xấu, Check chứng chỉ SSL/HTTPS
        |
(3) API Gateway / Load Balancer (Lớp 2: Routing & Điều phối)
        | Tách /api/users và /api/orders
       / \
      /   \
(4) Server Node.js X (REST Service Users)   (4) Server Node.js Y (REST Service Orders)
      |
(5) Data Access Layer (Redis Cache + DB Slave)
```

### Ví dụ NGINX cấu hình làm Load Balancer (Đóng vai trò phân lớp che giấu Backend thật):

Lúc này Client (Browser) gọi HTTP đến cổng 80 của IP `192.168.1.10` (NGINX Proxy). 
Browser không hề biết đằng sau NGINX đang giấu 3 con Backend Node.js chạy port 3000, 3001, 3002.

```nginx
# Cấu hình Layer 1 - proxy ẩn danh backend
upstream my_nodejs_cluster {
    # Định nghĩa các Server thật đang trốn đằng sau proxy (Layer cuối)
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name my-rest-api.com;

    location / {
        # Client giao tiếp với proxy, không giao tiếp với layer backend
        proxy_pass http://my_nodejs_cluster;
        
        # Thiết lập header để Node.js biết ai gọi proxy thực sự
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
    }
}
```

Từ góc độ của Client đoạn code React:
```javascript
// CLient KHÔNG HỀ quan tâm gọi vào Server 3000 hay 3001, nó chỉ biết gọi Layer bên ngoài
fetch("http://my-rest-api.com/api/products");
```
