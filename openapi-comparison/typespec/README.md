# Demo TypeSpec (Trước đây là CADL)

**TypeSpec** là một ngôn ngữ do **Microsoft** phát triển. Triết lý của nó là thay vì bắt Lập trình viên thiết kế API bằng YAML dài ngoằng (OpenAPI rất dễ sai thụt dòng, không có IDE autocompletion tốt), lập trình viên có thể viết API như viết code TypeScript.

Lợi ích: Tái sử dụng cực cao, có kế thừa, Decorator siêu mạnh mà không thể tìm thấy ở YAML/JSON thông thường. Nó tự sinh ngược lại OpenAPI cực chuẩn.

## 1. File TypeSpec
- Tên file: `main.tsp`. Rất giống TypeScript. Mọi thứ được define logic Model và Route.

## 2. Hướng dẫn Biên dịch ra OpenAPI (Swagger)

TypeSpec không đứng độc lập mà là **Công cụ cấp cao hơn để sinh ra OpenAPI**. Chúng ta biên dịch nó để ra OpenAPI.yaml.

### Cách cài đặt và chạy
1. Khởi tạo một dự án nếu chưa có:
```bash
npm install -g @typespec/compiler
```

2. Cài dependency cho thư mục TypeSpec này:
```bash
npm install @typespec/http @typespec/openapi3
```

3. Biên dịch file `main.tsp` sang OpenAPI:
```bash
# Sau khi chạy lệnh này, thư mục tsp-output sẽ hiện ra chứa file openapi.yaml
tsp compile main.tsp --emit @typespec/openapi3
```

Từ file `openapi.yaml` sinh ra, bạn xài lại mọi công cụ mạnh mẽ của Swagger như `openapi-generator-cli` tương tự thư mục `/openapi` nhé. TypeSpec chính là giải pháp dọn sạch mớ YAML bùi nhùi, giải quyết nhược điểm khó nhìn của OpenAPI.
