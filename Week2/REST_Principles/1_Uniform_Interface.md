# 1. Uniform Interface (Giao diện đồng nhất)

## 📖 Khái niệm
Uniform Interface là nguyên tắc quan trọng nhất tạo nên "linh hồn" của REST. Nó đặt ra các tiêu chuẩn chuẩn hóa về cáchClient và Server giao tiếp. Bằng cách áp dụng một giao diện chung, toàn bộ hệ thống trở nên đơn giản, dễ hiểu và cho phép Client/Server phát triển độc lập.

## 🔑 4 Ràng buộc con (Sub-constraints)
1. **Identification of resources (Định danh tài nguyên bằng URI):** Mỗi tài nguyên (Resource) được định danh bằng một URL/URI duy nhất.
2. **Manipulation of resources through representations (Thao tác qua biểu diễn):** Khi Client có được biểu diễn (representation - ví dụ file JSON/XML) của tài nguyên, nó có đủ thông tin để thay đổi hoặc xóa tài nguyên đó.
3. **Self-descriptive messages (Thông điệp tự mô tả):** Mỗi yêu cầu chứa đủ thông tin để Server hiểu cách xử lý, bằng cách sử dụng đúng HTTP Methods (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) và Content-Type phù hợp (`application/json`).
4. **HATEOAS (Hypermedia As The Engine Of Application State):** Server trả về các liên kết (hyperlinks) đi kèm trong dữ liệu, giúp Client tự khám phá các hành động tiếp theo mà không cần hard-code (gắn cứng) logic trên Client.

---

## 💻 Ví dụ chi tiết (Node.js/Express)

### Thiết kế sai (Không Uniform)
```http
POST /getUser?id=1
POST /createNewUser
POST /deleteUser?id=1
```

### Thiết kế chuẩn RESTful (Uniform Interface)
Sử dụng URI để chỉ định tài nguyên (`/users`) và HTTP Method để diễn tả hành động:

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// 1. HTTP GET - Lấy danh sách (Định danh: /users)
app.get('/users', (req, res) => {
    res.json([{ id: 1, name: 'Công' }]);
});

// 2. HTTP GET - Lấy chi tiết 1 resource
app.get('/users/:id', (req, res) => {
    const userId = req.params.id;
    res.json({ id: userId, name: 'Công' });
});

// 3. HTTP POST - Tạo tài nguyên mới
app.post('/users', (req, res) => {
    // Thông điệp tự mô tả: body chứa JSON application/json
    const newUser = req.body; 
    res.status(201).json({ message: 'User created' });
});

// 4. HTTP DELETE - Xóa tài nguyên
app.delete('/users/:id', (req, res) => {
    res.status(204).send(); // 204 No Content
});

// 5. Kết hợp HATEOAS trong Response
app.get('/orders/:id', (req, res) => {
    res.json({
        id: req.params.id,
        item: 'Laptop',
        status: 'pending',
        links: [
            { rel: 'self', href: '/orders/123' },
            { rel: 'cancel', href: '/orders/123/cancel', method: 'PUT' }, // Client tự biết URL để hủy đơn hàng
            { rel: 'pay', href: '/orders/123/pay', method: 'POST' }
        ]
    });
});
```
