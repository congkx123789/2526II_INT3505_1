# [Mẫu Thông báo] Nâng cấp API Thanh toán v2 & Sunset v1

**Tiêu đề**: [Quan trọng] Nâng cấp API Thanh toán v2 & Kế hoạch ngừng hoạt động bản v1 (Sunset Notice)

**Kính gửi Quý Đối tác / Nhà phát triển,**

Nhằm hỗ trợ thanh toán đa tiền tệ và nâng cao bảo mật, chúng tôi đã chính thức ra mắt Payment API v2. Theo đó, hệ thống sẽ tiến hành quá trình ngừng hỗ trợ (Deprecation) đối với Payment API v1 (`/api/v1/payments`).

### Lịch trình chuyển đổi (Lifecycle Timeline):
- **Trạng thái hiện tại**: Bản v1 đang ở trạng thái Deprecated (Vẫn hoạt động nhưng không cập nhật tính năng).
- **Ngày 01/05/2026**: Brownout test (Gián đoạn thử nghiệm v1 trong 2 giờ).
- **Ngày 01/06/2026 (Sunset)**: Dừng hoạt động hoàn toàn v1. Các request gọi vào v1 sẽ nhận lỗi 410 Gone.

### Bạn cần làm gì?
Vui lòng di chuyển (migrate) hệ thống của bạn sang bản v2 trước ngày 01/06/2026 để không làm gián đoạn giao dịch của khách hàng.

### Sự thay đổi chính (Breaking Changes):
1. Endpoint thay đổi từ `/api/v1/payments` sang `/api/v2/payments`.
2. Payload bắt buộc bổ sung thêm trường `currency` và `payment_method`.

Xem chi tiết Hướng dẫn chuyển đổi (Migration Guide) tại: [Link_Document]

Nếu bạn cần bất kỳ sự hỗ trợ kỹ thuật nào, vui lòng phản hồi lại email này hoặc liên hệ qua kênh hỗ trợ nhà phát triển của chúng tôi.

Trân trọng,  
**Đội ngũ Phát triển API**
