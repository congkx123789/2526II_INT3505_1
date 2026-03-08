# 3. Stateless (Phi trạng thái)

## 📖 Khái niệm
Trong mô hình Stateless, **Server không tự ghi nhớ bất kỳ thông tin gì về trạng thái (state) của Client** giữa các lần gửi request liên tiếp.
Điều này có nghĩa là mỗi HTTP Request từ Client gửi lên Server phải KHÉP KÍN: Nó phải chứa **đầy đủ tất cả thông tin (Token, ID, Session, Data...)** cần thiết để Server có thể hiểu và xử lý yêu cầu đó, mà không cần dựa vào bất kỳ ngữ cảnh nào được lưu trong bộ nhớ máy chủ ở các request trước.

## 🚀 Lợi ích & ⚠️ Hạn chế
- **Lợi ích lớn nhất - Scale-out (Mở rộng ngang):** Quản lý trạng thái trên Server gây tốn RAM. Bằng Stateless, bạn có thể triển khai hệ thống lên 100 Server. Request 1 rơi vào Server A, Request 2 rơi vào Server B hoàn toàn bình thường (vì Server B không cần nhớ Request 1). Hợp với Cloud computing.
- **Hạn chế:** Tốn băng thông mạng hơn vì mỗi requset phải đính kèm đầy đủ thông tin xác thực.

---

## 💻 Ví dụ chi tiết

### ❌ Cách làm sai: Stateful (Sử dụng Session trên Server)
```javascript
let currentUserId = null; // Server nhớ tạm biến ở bộ nhớ tĩnh hoặc Session Server

app.post('/login', (req, res) => {
    currentUserId = req.body.id; // Lưu trạng thái
    res.send('Login OK');
});

// Nếu Request thứ 2 gửi đến (Không truyền ID nữa), Server vẫn lấy currentUserId
app.get('/myOrder', (req, res) => {
    // 💥 NẾU Request này rơi vào instance SERVER SỐ 2 (load balancer điều phối),
    // biến currentUserId trên Server 2 sẽ là NULL -> Lỗi!
    const orders = database.find(userId: currentUserId); 
    res.json(orders);
});
```

### ✅ Cách làm chuẩn REST: Stateless (Gửi Token kèm mọi Request)
Sử dụng JWT (JSON Web Token) để chứng minh trạng thái stateless. Server không lưu 'ai đang đăng nhập'.

```javascript
// 1. Sinh ra Token chứa thông tin Client (để Client tự giữ)
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    if (authSuccess) {
        // Sinh jwt token: chứa { userId: 123 }
        const token = jwt.sign({ userId: 123 }, 'secret_key');
        res.json({ token: token }); // Client sẽ lưu token này ở localStorage
    }
});

// 2. Các Request yêu cầu lấy dữ liệu -> Server không nhớ Client là ai
app.get('/api/myOrder', (req, res) => {
    // Client BẮT BUỘC phải gửi kèm theo Token ở Header mọi lúc
    const token = req.headers['authorization']; 
    if (!token) return res.status(401).send('Unauthorized');

    // Server giải mã Token để biết đấy là User nào (Server không cần tra bảng Session ở DB nhớ)
    const decodedPayload = jwt.verify(token, 'secret_key');
    
    // Tìm order bằng chính dữ liệu mang theo trên token
    const orders = database.find(userId: decodedPayload.userId); 
    res.json(orders);
});
```
