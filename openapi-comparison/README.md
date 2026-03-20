# So sánh các định dạng tài liệu hóa API: OpenAPI, API Blueprint, RAML và TypeSpec

Dưới đây là bảng phân tích và so sánh 4 định dạng tài liệu API phổ biến hiện nay:

| Tiêu chí | OpenAPI (Swagger) | API Blueprint | RAML | TypeSpec (Microsoft) |
| --- | --- | --- | --- | --- |
| **Định dạng** | YAML hoặc JSON | Markdown (hiệu chỉnh) | YAML | Ngôn ngữ riêng (giống TypeScript) |
| **Mức độ phổ biến** | Cực kỳ cao, tiêu chuẩn công nghiệp hiện tại | Trung bình, đang giảm dần | Trung bình | Đang phát triển (được Microsoft hậu thuẫn) |
| **Tính dễ đọc (Người)** | Khá rườm rà nếu API lớn, cấu trúc phức tạp | Rất tốt (vì viết bằng Markdown) | Khá tốt, tái sử dụng cao | Rất xuất sắc cho lập trình viên |
| **Công cụ hỗ trợ** | Hệ sinh thái khổng lồ (Swagger UI, Generator,...) | Dredd, Aglio, Snowboard | RAML2HTML, Osprey | Trình biên dịch mạnh mẽ, xuất ra OpenAPI |
| **Tái sử dụng code** | Có (dùng `$ref`) | Hạn chế | Rất tốt (Traits, Resource Types) | Tuyệt vời (Kế thừa, Models, Decorators) |
| **Thế mạnh** | Hệ sinh thái công cụ số 1, dễ dàng sinh code/test tự động cho mọi ngôn ngữ. | Viết tài liệu thân thiện với người đọc phi kỹ thuật (BA, PM). | Định nghĩa API theo tư duy Design-First rất chặt chẽ. | Viết API nhanh, sạch, cấu trúc giống code thật, Dễ bảo trì hơn OpenAPI. |

---

## Cấu trúc thư mục thư viện demo

Ví dụ ứng dụng **Quản lý Thư viện** được thiết kế lại bằng cả 4 ngôn ngữ trên. Bạn có thể chui vào từng thư mục để xem cấu trúc và cách chạy lệnh sinh code/test:

1. [openapi/](./openapi) - Định dạng OpenAPI (YAML)
2. [api-blueprint/](./api-blueprint) - Định dạng API Blueprint (Markdown)
3. [raml/](./raml) - Định dạng RAML (YAML)
4. [typespec/](./typespec) - Định dạng TypeSpec (.tsp)
