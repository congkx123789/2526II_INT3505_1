# 2. Client-Server (Kiến trúc Khách - Chủ)

## 📖 Khái niệm
Nguyên tắc này chia hệ thống thành 2 thành phần hoàn toàn độc lập với các trách nhiệm riêng biệt:
- **Client (Khách):** Chịu trách nhiệm về giao diện người dùng (UI), hiển thị dữ liệu và quản lý các tương tác của người dùng.
- **Server (Chủ/Máy chủ):** Chịu trách nhiệm về xử lý logic kinh doanh, tính toán, xác thực và lưu trữ/truy xuất dữ liệu vào Database.

## 🚀 Lợi ích
- **Tách biệt mối quan tâm (Separation of Concerns):** Giúp mã nguồn tách mạch lạc.
- **Phát triển độc lập:** Đội Frontend và Backend có thể làm việc song song, miễn là tuân thủ API Contract (JSON format thỏa thuận từ trước).
- **Đa nền tảng:** Một Server API duy nhất có thể phục vụ nhiều loại Client khác nhau (Web React, Mobile iOS/Android, Desktop app).
- **Khả năng mở rộng (Scalability):** Có thể nâng cấp phần cứng hoặc scale Server độc lập với Client.

---

## 💻 Ví dụ chi tiết

### 2.1 Backend (Node.js/Express) - Chỉ nhận Request và Trả về JSON
Backend không quan tâm việc dữ liệu này sẽ hiển thị lên trình duyệt ra sao. Nó chỉ làm đúng 1 việc: lấy dữ liệu từ DB và trả về dạng API.

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors()); // Cho phép Client ở Domain khác gọi tới

app.get('/api/products', (req, res) => {
    // Logic: Gọi tính toán/Query Database...
    const products = [
        { id: 1, name: 'Macbook Pro', price: 2000 },
        { id: 2, name: 'Dell XPS', price: 1500 }
    ];
    // Chỉ trả về Data thuần túy dưới dạng JSON
    res.json(products);
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### 2.2 Frontend Client (Ví dụ HTML/Vanilla JS) - Chỉ lo hiển thị
Client không biết làm sao lấy được dữ liệu trong DB. Nó chỉ gọi API của Server đã thỏa thuận, nhận JSON và render UI.

```html
<!-- index.html (Chạy trên port 5500 hoặc bất kỳ UI nào) -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Sản phẩm</title>
</head>
<body>
    <h1>Danh sách Sản phẩm</h1>
    <ul id="productList"></ul>

    <script>
        // Gọi lên Server
        fetch('http://localhost:3000/api/products')
            .then(res => res.json())
            .then(data => {
                const list = document.getElementById('productList');
                data.forEach(product => {
                    const li = document.createElement('li');
                    li.textContent = `${product.name} - $${product.price}`;
                    list.appendChild(li);
                });
            })
            .catch(err => console.error("Lỗi khi kết nối tới Server", err));
    </script>
</body>
</html>
```

*Trong cấu trúc này, cho dù Client có chuyển từ Giao diện HTML sang App Mobile Android (dùng Kotlin), Code của Server không cần phải sửa đổi bất kỳ dòng nào.*
