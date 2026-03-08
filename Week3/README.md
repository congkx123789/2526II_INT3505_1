# Buổi 3 – API Design Best Practices

> **Môn học:** INT3505 – Kiến trúc Hướng Dịch vụ (SOA)  
> **Chủ đề:** Thiết kế RESTful API chuẩn mực – Naming, Consistency, Extensibility

---

## 📁 Cấu trúc thư mục

```
Week3/
├── README.md                         ← File này
├── docs/
│   ├── naming_conventions.md         ← Lý thuyết & bảng so sánh Naming Conventions
│   ├── consistency_extensibility.md  ← Lý thuyết Consistency & Extensibility
│   └── swagger_template.yaml         ← Mẫu OpenAPI/Swagger cho thực hành
├── case_study/
│   ├── poorly_designed_api.md        ← Đề bài: Bộ API lỗi cần phát hiện & sửa
│   └── answer_key.md                 ← Đáp án chi tiết (dành cho giảng viên)
├── practice/
│   ├── peer_review_template.md       ← Template nhóm dùng để trình bày & review
│   └── group_exercise.md             ← Đề bài thực hành nhóm
└── demo/
    ├── app.py                        ← Flask demo: Bad API vs Good API
    ├── requirements.txt
    └── test_api.py                   ← Script test tự động bằng requests
```

---

## 🎯 Mục tiêu buổi học

| # | Kỹ năng | Mô tả |
|---|---------|-------|
| 1 | **Nhận diện** | Phân biệt API thiết kế tốt vs kém qua các tiêu chí cụ thể |
| 2 | **Áp dụng** | Đặt tên endpoint đúng chuẩn REST (Naming Conventions) |
| 3 | **Phân tích** | Đảm bảo tính nhất quán (Consistency) trong JSON Payload |
| 4 | **Thiết kế** | Xây dựng Response chuẩn hỗ trợ mở rộng (Extensibility) |
| 5 | **Thực hành** | Peer Review thiết kế API trong nhóm |

---

## 🚀 Hướng dẫn chạy Demo

```bash
cd Week3/demo
pip install -r requirements.txt
python app.py
```

Sau đó mở trình duyệt hoặc dùng Postman truy cập:
- **Bad API (minh họa lỗi):** `http://localhost:5000/bad/...`
- **Good API (chuẩn mực):**  `http://localhost:5000/good/v1/...`

Chạy test script:
```bash
python test_api.py
```
