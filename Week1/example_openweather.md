# 🌤️ Ví Dụ Mẫu: Phân Tích OpenWeatherMap API

> Đây là ví dụ mẫu thầy phân tích ngay trên lớp để học viên hình dung.
> Hãy làm tương tự cho 3 API bạn chọn trong bài tập!

---

## API: OpenWeatherMap

### 1. Thông tin cơ bản

| Hạng mục | Thông tin |
|---|---|
| **Tên API** | OpenWeatherMap API |
| **Link Docs** | https://openweathermap.org/api |
| **Mục đích cốt lõi** | Cung cấp dữ liệu thời tiết hiện tại, dự báo thời tiết và dữ liệu lịch sử cho bất kỳ tọa độ / thành phố nào trên thế giới. Phục vụ cho các ứng dụng thời tiết, logistics, nông nghiệp... |

### 2. Đặc điểm kỹ thuật

| Hạng mục | Thông tin |
|---|---|
| **Kiểu kiến trúc** | ✅ **RESTful API** |
| **Định dạng dữ liệu** | ✅ **JSON** (có hỗ trợ XML nhưng rất ít dùng) |
| **Cơ chế xác thực** | ✅ **API Key** — truyền qua query parameter `&appid=YOUR_KEY` |

---

### 3. Phân tích Endpoint tiêu biểu

**Endpoint được chọn: Lấy thời tiết hiện tại của một thành phố**

```
GET https://api.openweathermap.org/data/2.5/weather
```

#### 📤 Input (Dữ liệu gửi lên - Query Parameters)

| Tên tham số | Bắt buộc? | Mô tả |
|---|---|---|
| `q` | ✅ Có | Tên thành phố. Ví dụ: `q=Hanoi` |
| `appid` | ✅ Có | API Key của bạn (lấy sau khi đăng ký) |
| `units` | ⬜ Không | Đơn vị nhiệt độ: `metric` (Celsius), `imperial` (Fahrenheit). Mặc định là Kelvin |
| `lang` | ⬜ Không | Ngôn ngữ trả về. Ví dụ: `lang=vi` để nhận kết quả tiếng Việt |

**Ví dụ URL hoàn chỉnh:**
```
GET https://api.openweathermap.org/data/2.5/weather?q=Hanoi&appid=YOUR_API_KEY&units=metric
```

#### 📥 Output (Dữ liệu nhận về - HTTP 200)

```json
{
  "weather": [
    {
      "main": "Clouds",
      "description": "scattered clouds"
    }
  ],
  "main": {
    "temp": 28.5,
    "feels_like": 31.2,
    "humidity": 75
  },
  "wind": {
    "speed": 3.6
  },
  "name": "Hanoi"
}
```

**Giải thích các trường quan trọng:**

| Trường | Ý nghĩa |
|---|---|
| `weather[0].main` | Tình trạng thời tiết chính (Clear, Clouds, Rain...) |
| `weather[0].description` | Mô tả chi tiết hơn |
| `main.temp` | Nhiệt độ hiện tại (°C khi dùng `units=metric`) |
| `main.humidity` | Độ ẩm (%) |
| `name` | Tên thành phố Server xác nhận |

---

### 4. Nhận xét

- **Điểm tốt trong thiết kế:**
  > Endpoint đặt tên rõ ràng `/weather`. Dùng query parameter chuẩn để tìm kiếm theo tên thành phố (`q=...`) hoặc tọa độ (`lat=...&lon=...`). Dễ đọc và cực kỳ phổ biến.

- **Điểm có thể cải thiện:**
  > API Key truyền qua query parameter (`?appid=...`) trên URL — điều này kém an toàn hơn so với truyền qua HTTP Header `Authorization: Bearer ...` vì URL thường được lưu vào log máy chủ.

---
