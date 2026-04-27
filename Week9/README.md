# Buổi 9: API Versioning và Lifecycle Management (Payment Case Study)

Dự án thực hành này triển khai chính xác kịch bản 4 bước nâng cấp API Thanh toán từ v1 lên v2.

## 1. Cấu trúc mã nguồn
- **`app.py`**: Server FastAPI xử lý song song V1 và V2.
- **`case_study_lifecycle.md`**: Chi tiết chiến lược xác định Breaking Change và lộ trình nâng cấp.
- **`deprecation_announcement.md`**: Mẫu email thông báo cho developers.

## 2. Các kịch bản Lifecycle (Vòng đời)
Trong file `app.py`, bạn có thể thay đổi biến `CURRENT_STAGE` để thử nghiệm các giai đoạn:
- `"COEXIST"`: V1 & V2 cùng tồn tại bình thường.
- `"DEPRECATED"`: V1 bắt đầu có Header cảnh báo.
- `"BROWNOUT"`: V1 giả lập lỗi 503 (Dùng để nhắc nhở client nâng cấp).
- `"SUNSET"`: V1 bị khai tử hoàn toàn (410 Gone).

## 3. Cách chạy thử

```bash
# Cài đặt
pip install -r requirements.txt

# Chạy server
python app.py
```

### Test V1 (Legacy) - Trước Breaking Change
```bash
curl -i -X POST http://localhost:8000/api/v1/payments \
     -H "Content-Type: application/json" \
     -d '{"amount": 100000, "order_id": "ORD123"}'
```

### Test V2 (Modern) - Sau Breaking Change
```bash
curl -i -X POST http://localhost:8000/api/v2/payments \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 100000, 
       "currency": "VND", 
       "payment_method": "credit_card", 
       "order_id": "ORD123"
     }'
```
