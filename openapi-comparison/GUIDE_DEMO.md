# Hướng dẫn Chạy Demo: So sánh API Specs (OpenAPI, Blueprint, RAML, TypeSpec)

Tài liệu này hướng dẫn bạn cách thực hành (hands-on) để so sánh 4 định dạng đặc tả API phổ biến từ các file lý thuyết hiện có trong dự án.

## 1. Chuẩn bị (Prerequisites)

- **Node.js**: Đảm bảo máy bạn đã cài Node.js (phiên bản 18+).
- **Internet**: Cần để tải `npx` tools trong lần đầu.

## 2. Công cụ sử dụng

- **@redocly/cli**: Render OpenAPI sang HTML.
- **@typespec/compiler**: Biên dịch TypeSpec sang OpenAPI.
- **aglio**: Render API Blueprint.
- **raml2html**: Render RAML.

## 3. Các bước thực hiện Demo

Mở Terminal tại thư mục `openapi-comparison/` và chạy:

### Bước 3.1: Thử nghiệm OpenAPI

```bash
npx @redocly/cli build-docs openapi/openapi.yaml --output=outputs/openapi.html
```

### Bước 3.2: Thử nghiệm TypeSpec (Khuyên dùng)

TypeSpec giống như TypeScript cho API, sạch sẽ và mạnh mẽ.

```bash
# 1. Biên dịch sang JSON
npx @typespec/compiler compile typespec/main.tsp --output-dir=outputs/typespec

# 2. Render sang HTML
npx @redocly/cli build-docs outputs/typespec/openapi.json --output=outputs/typespec.html
```

### Bước 3.3: Thử nghiệm API Blueprint

Dành cho những ai thích Markdown.

```bash
npx aglio -i api-blueprint/api.apib -o outputs/blueprint.html
```

### Bước 3.4: Thử nghiệm RAML

Cấu trúc phân cấp YAML cực kỳ chặt chẽ.

```bash
npx raml2html raml/api.raml > outputs/raml.html
```

---


## 4. Cách xem kết quả

Sau khi chạy, hãy mở các file trong thư mục `outputs/` bằng trình duyệt. Bạn sẽ thấy sự khác biệt về giao diện và cách trình bày của từng công cụ.

- `outputs/openapi.html`: Giao diện Redoc chuẩn.
- `outputs/typespec.html`: Giao diện render từ mã TypeSpec.
- `outputs/blueprint.html`: Giao diện phong cách Markdown (Aglio).
- `outputs/raml.html`: Giao diện RAML truyền thống.

> [!TIP]
> Bạn có thể chạy nhanh tất cả bằng: `npm run demo:all` (nếu môi trường mạng của bạn cho phép tải npx nhanh).

## 5. So sánh thực tế (Key Takeaways)

| Tiêu chuẩn | Cảm nhận khi demo | Phù hợp cho |
| --- | --- | --- |
| **OpenAPI** | Đầy đủ nhất, nhiều công cụ nhất. | Mọi dự án thực tế. |
| **TypeSpec** | Viết nhanh nhất, ít lỗi cú pháp nhất (như code). | Các hệ thống lớn, phức tạp. |
| **Blueprint** | Dễ đọc nhất (Markdown), thân thiện với BA/PM. | Thiết kế API giai đoạn đầu. |
| **RAML** | Cấu trúc phân cấp rõ ràng, dễ tái sử dụng. | Các hệ thống hướng tới Design-First. |

---

> [!TIP]
> Bạn có thể chạy tất cả cùng lúc bằng lệnh: `npm run demo:all` (nếu đã cài đặt scripts trong package.json).
