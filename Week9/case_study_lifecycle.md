# Case Study: Nâng cấp Payment API từ v1 sang v2

## Bước 1: Xác định "Breaking Change"
Vấn đề ở v1: API `POST /api/v1/payments` chỉ nhận `amount` và mặc định hiểu là VND.
Nếu sửa trực tiếp để thêm `currency` và `payment_method`, các client cũ sẽ bị crash.

**JSON v1:**
```json
{ "amount": 100000, "order_id": "ORD123" }
```

**JSON v2 (Breaking Change):**
```json
{ 
  "amount": 100000, 
  "currency": "VND", 
  "payment_method": "credit_card", 
  "order_id": "ORD123" 
}
```

## Bước 2: Chọn chiến lược Versioning
Dự án chốt sử dụng **URL Versioning**: `/api/v2/payments`.
- **Lý do**: Rõ ràng nhất, dễ chia routing trên API Gateway, developer nhìn vào URL là biết ngay đang dùng bản nào.

## Bước 3: Lập kế hoạch nâng cấp (Lifecycle)

| Giai đoạn | Thời gian | Mô tả |
| :--- | :--- | :--- |
| **Giai đoạn 1: Co-existence** | Tháng 1 | v1 và v2 chạy song song. v2 là bản chính thức trong docs. |
| **Giai đoạn 2: Deprecation** | Tháng 2 | Thông báo v1 là Deprecated. Thêm Header `Deprecation: true`. |
| **Giai đoạn 3: Brownout** | Tháng 5 | Tắt v1 thử nghiệm trong thời gian ngắn (trả về lỗi 503). |
| **Giai đoạn 4: Sunset** | Tháng 6 | Xóa bỏ v1 hoàn toàn. Trả về `410 Gone`. |
