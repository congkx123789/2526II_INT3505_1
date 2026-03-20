# Demo RAML (RESTful API Modeling Language)

RAML có định dạng tương đồng với YAML như OpenAPI, thế mạnh lớn nhất là hệ thống `Traits` và `ResourceTypes` cho phép tính **tái sử dụng cao**, giảm việc phải copy paste lặp code khi có chung 1 chuẩn Response Error hay Pagination.

## 1. File RAML
- Định dạng tại: `api.raml`. Khai báo rất mạch lạc và có sử dụng TypeScript-like type definition (ví dụ `Book[]` hay `id?: string`).

## 2. Công cụ phổ biến: Sinh HTML tự động

Công cụ mạnh nhất của RAML là **raml2html**. 

### Cách cài và chạy
```bash
npm install -g raml2html

# Biên dịch RAML thành trang tài liệu chuẩn Bootstrap đẹp
raml2html api.raml > index.html
```

### Mock API Server bằng Osprey
Nếu bạn đang viết RAML, bạn có thể biến file này giả lập thành API sống (Mock) bằng Osprey (Mulesoft):
```bash
npx osprey-mock-service -f api.raml -p 3000
# Server sẽ auto trả về thông tin Book
```
