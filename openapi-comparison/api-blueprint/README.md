# Demo API Blueprint

API Blueprint là định dạng tiên phong chuyên tiếp cận theo hướng "Tài liệu đẹp dễ đọc" dành cho con người. Format viết hoàn toàn dựa trên Markdown.

## 1. File API Blueprint
- Xem định nghĩa chi tiết tại: `api.apib`. Markdown giúp các BA (Business Analyst) hoặc khách hàng cũng đọc hiểu tài liệu.

## 2. Hướng dẫn sinh HTML và Test tự động

Vì format là Markdown nên công việc chính của cộng đồng Blueprint là chuyển code này thành giao diện HTML tuyệt đẹp, hoặc Mock Data.

### Biên dịch ra HTML đẹp (Snowboard / Aglio)
```bash
# Dùng Snowboard (viết bằng Golang, nhanh) sinh HTML
npx snowboard html -i api.apib -o index.html
```

### Kiểm thử API tự động với Dredd
`Dredd` là công cụ huyền thoại gắn liền với Blueprint. Nó đọc tài liệu và tự động gọi API server để xem server có trả về code chuẩn với tài liệu không.
```bash
# Cài Dredd: 
npm instal -g dredd

# Chạy Dredd đối chiếu tài liệu với 1 con server thật
dredd api.apib http://localhost:3000
```
Dredd sẽ tự bóc tách các ví dụ (example payload) trong file Blueprint gửi vào API `http://localhost:3000/books` và assert xem có ra đúng mã 200/201 không!
