# Demo OpenAPI (Swagger)

Đây là chuẩn công nghiệp phổ biến nhất hiện nay, dựa trên JSON/YAML.

## 1. File OpenAPI
- Xem định nghĩa chi tiết tại: `openapi.yaml`. Format file sử dụng YAML. Cấu trúc chia thành Header (info, servers), Paths (danh sách api), và Components (Schemas dùng chung).

## 2. Hướng dẫn sinh Code / Test tự động

OpenAPI có bộ công cụ lớn nhất hành tinh. Để sinh code tự động, chúng ta thường dùng thư viện `openapi-generator-cli`.

### Công cụ cần thiết
- Node.js (dùng `npx`) hoặc Java (dùng file `.jar`).

### Các bước sinh thư viện Client (TypeScript) hoặc Server
```bash
# 1. Sinh code TypeScript Client để Frontend dùng
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./generated-client

# 2. Sinh khung sườn Server Node.js (Express)
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g nodejs-express-server -o ./generated-server
```

### Cách tạo bộ test (Postman / Newman)
Sử dụng công cụ `openapi-to-postmanv2`:
```bash
npx openapi-to-postmanv2 -s openapi.yaml -o postman_collection.json

# Chạy test tự động với Newman
npx newman run postman_collection.json
```
