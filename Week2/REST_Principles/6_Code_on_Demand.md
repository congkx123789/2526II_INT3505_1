# 6. Code on Demand (Mã linh hoạt - Tùy chọn)

## 📖 Khái niệm
Đây là nguyên tắc **DUY NHẤT LÀ TÙY CHỌN (Optional)** trong 6 nguyên tắc của REST. 
Nó cho phép Server mở rộng, bổ sung hoặc tuỳ chỉnh các tính năng của Client ngay thời gian chạy (runtime) bằng cách tải xuống (download) và thực thi một đoạn mã lập trình (code snippets/scripts) như là JavaScript hoặc Java Applets cho Client.

## 🚀 Tại sao nó là tùy chọn & Ít dùng?
- **Khó đoán trước:** Client hiện đại (như App iOS, Android) sử dụng Swift, Java khó lòng chạy được các Code (như Javascript) truyền từ server xuống một cách trực tiếp mà không cần công cụ trung gian (WebView).
- **Nguy cơ Bảo mật:** Việc Client mù quáng thực thi mã do Server truyền xuống chứa đựng rất nhiều lỗ hổng rủi ro bảo mật tàng hình (tấn công XSS).
- Do vậy, trong lập trình API Microservices/Mobile thông thường hiện nay, các kỹ sư thường **BỎ QUA** nguyên tắc này và chỉ trao đổi dữ liệu tinh khiết thông qua JSON/XML thay vì trả mã thực thi.

---

## 💻 Ví dụ chi tiết

Mọi người thường dùng nó trong các hệ thống Web Application Browser truyền thống, nơi mà JS được load lười (Lazy-loading) hoặc API trả về mã để biểu diễn UI.

### 6.1 Server trả về Script (Node.js/Express)
Thay vì API REST `/api/calculator` trả về JSON (`{ a: 1, b: 2 }`), nó trả về một đoạn Mã (Code) tính toán.

```javascript
const express = require('express');
const app = express();

app.get('/api/get-widget-logic', (req, res) => {
    // Không trả về JSON theo cách Uniform thông thường
    // Trực tiếp trả về mã Javascript (Code on demand)
    const javascriptCode = `
        function drawChart(data) {
            console.log("Đang vẽ biểu đồ bằng logic từ Server cấp...", data);
            alert("Chart Generated from Server-provided Logic!");
        }
        window.drawChart = drawChart;
    `;
    
    // Khai báo là file Javascript script cho Client
    res.set('Content-Type', 'application/javascript');
    res.send(javascriptCode);
});
app.listen(3000);
```

### 6.2 Client thực thi mã (Trình duyệt Web)
Trình duyệt xin logic UI từ API, inject trực tiếp Code đó vào HTML để thực thi.

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Code on Demand Example</h1>
    <button onclick="requestServerLogic()">Lấy Logic tính toán từ Server</button>
    <button onclick="if(window.drawChart) drawChart([1,2,3])">Chạy thử Logic</button>

    <script>
        function requestServerLogic() {
            // Fetch Code from Server
            fetch('http://localhost:3000/api/get-widget-logic')
                .then(res => res.text()) // Nhận mã Script dạng text (string)
                .then(code => {
                    // Inject "Mã On Demand" vào hệ thống trình duyệt (Nguy hiểm, nhưng đúng spec)
                    const scriptTag = document.createElement('script');
                    scriptTag.textContent = code;
                    document.body.appendChild(scriptTag);
                    console.log("Tải thành công Code On Demand.");
                });
        }
    </script>
</body>
</html>
```
