# 4. Cacheable (Khả năng lưu trữ đệm)

## 📖 Khái niệm
Vì các truy vấn qua mạng đòi hỏi thời gian phản hồi (latency) và tiêu tốn băng thông, hệ thống REST yêu cầu mọi phản hồi (Response) từ Server phải định nghĩa rõ ràng nó "Có được phép Cache không?", và "Được cache trong bao lâu?".
Việc này được thực hiện thông qua HTTP Headers. Các bên trung gian nhận thông tin (Trình duyệt, CDN, Proxy) sẽ tự động lưu lại (cache) các response này để phục vụ lại siêu tốc cho các request tương tự tiếp theo thay vì phải gọi vào Back-end, Database.

## 🚀 Lợi ích
- **Tăng tốc độ (Performance):** Client load dữ liệu gần như ngay lập tức nếu đã cache.
- **Giảm tải cho Server (Scalability):** Giảm thiểu hàng triệu request vào Database và CPU máy chủ.

## Các Header Cache thông dụng:
- `Cache-Control`: Định nghĩa chiến lược (VD: `max-age=3600` // 1 giờ, `no-cache`, `public`, `private`).
- `ETag` (Entity Tag): Một mã băm (Hash) đại diện cho version hiện tại của Resource. Nếu Resource đổi -> ETag đổi.
- `Last-Modified`: Thời gian cuối cùng Resource bị thay đổi.

---

## 💻 Ví dụ chi tiết (Node.js/Express)

### 4.1 Sử dụng Cache-Control (Cache dựa trên thời gian)

Server thông báo cho Client: "Dữ liệu này mầy được phép lưu thẳng vào RAM/Ổ cứng và dùng lại trong 60 giây tiếp theo, cấm gọi lại Server trong vòng 60 giây đó!".

```javascript
app.get('/api/statistics/daily', (req, res) => {
    // Tính toán dữ liệu nặng nề tốn 5 giây
    const statsData = { views: 5000, money: 1000 };
    
    // Gắn Header: Báo trình duyệt cache này trong vòng 60 giây
    res.set('Cache-Control', 'public, max-age=60'); 
    
    res.json(statsData);
});
// Nếu trình duyệt gọi lại F5 trong vòng 59s đầu, API này KHÔNG HỀ được chạy vào server.
// Trình duyệt tự nhận lấy data từ bộ nhớ máy tính. (Status 200 - disk cache)
```

### 4.2 Sử dụng ETag (Cache dựa trên kiểm tra thay đổi)
Sử dụng trường hợp bạn muốn Cache dài nhưng vẫn muốn lấy Dữ liệu Mới ngay lập tức nếu server có sửa đổi.

```javascript
const crypto = require('crypto');

let product = { id: 1, name: "IPhone", price: 1000, version: 1 };

app.get('/api/product/1', (req, res) => {
    // 1. Tạo chuỗi Hash đại diện cho data hiện tại (ETag)
    const eTagHash = crypto.createHash('md5').update(JSON.stringify(product)).digest('hex');

    // 2. Client gửi lên header 'If-None-Match' t/c Etag cũ nó đang giữ
    const clientHeaderEtag = req.headers['if-none-match'];

    // 3. Nếu Data chưa sửa -> Hash bằng nhau -> Server ngắt kết nối luôn, đỡ tốn băng thông Data
    if (clientHeaderEtag === eTagHash) {
        return res.status(304).send(); // 304 Not Modified -> Trình duyệt TỰ HIỂU và dùng lại data cũ của nó
    }

    // 4. Nếu là lần đầu tiên, hoặc Data có sửa (ETag ko khớp) -> Phục vụ data kèm ETag mới
    res.setHeader('ETag', eTagHash);
    res.json(product);
});
```
