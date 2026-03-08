"""
test_api.py – Kiểm thử tự động: Bad API vs Good API
Chạy: python test_api.py  (khi app.py đang chạy trên port 5000)
"""
import requests
import json

BASE = "http://localhost:5000"


def print_section(title):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


def call(method, url, data=None, label=""):
    full_url = BASE + url
    try:
        r = getattr(requests, method)(full_url, json=data, timeout=5)
        status_color = "\033[92m" if r.status_code < 300 else "\033[91m"
        print(f"\n{'─' * 50}")
        print(f"  [{label}]")
        print(f"  {method.upper()} {url}")
        print(f"  Status: {status_color}{r.status_code}\033[0m")
        print(f"  Response:")
        print(json.dumps(r.json(), ensure_ascii=False, indent=4))
    except requests.exceptions.ConnectionError:
        print("\n❌ Không kết nối được. Hãy chắc chắn app.py đang chạy!")
        exit(1)


# ─────────────────────────────────────
# 1. BAD API – Nhận diện vấn đề
# ─────────────────────────────────────
print_section("❌ BAD API DEMO – Nhận diện các lỗi thiết kế")

call("get", "/bad/getAllUsers",
     label="Lỗi: Động từ trong URL + Mảng trực tiếp (không có envelope/pagination)")

call("get", "/bad/User_Profile?UserID=1",
     label="Lỗi: PascalCase URL + ID trong query string + Fields không nhất quán")

call("get", "/bad/getOrdersByUserID/1",
     label="Lỗi: Động từ URL + Không có hierarchy + Mảng trực tiếp")

call("post", "/bad/createUser",
     data={"UserName": "test", "Email": "t@test.com"},
     label="Lỗi: Động từ URL + Status 200 thay vì 201 + Response thiếu data")


# ─────────────────────────────────────
# 2. GOOD API – Thiết kế chuẩn mực
# ─────────────────────────────────────
print_section("✅ GOOD API DEMO – Thiết kế chuẩn mực")

call("get", "/good/v1/users",
     label="✅ Danh từ số nhiều + Envelope + Pagination")

call("get", "/good/v1/users?page=1&limit=2",
     label="✅ Pagination với query string")

call("get", "/good/v1/users?name=nguyen",
     label="✅ Filter với query string")

call("get", "/good/v1/users/1",
     label="✅ Resource ID là path parameter")

call("get", "/good/v1/users/99",
     label="✅ 404 chuẩn với envelope error")

call("post", "/good/v1/users",
     data={"username": "phamvane", "email_address": "e@gmail.com", "phone_number": "0988888888"},
     label="✅ POST tạo user + 201 + Envelope đầy đủ")

call("post", "/good/v1/users",
     data={"username": "test"},
     label="✅ Validation error 400 + Chi tiết lỗi từng field")

call("patch", "/good/v1/users/1",
     data={"email_address": "updated@gmail.com"},
     label="✅ PATCH cập nhật một phần")

call("get", "/good/v1/users/1/orders",
     label="✅ Hierarchy: orders của user 1")

call("get", "/good/v1/users/1/orders?status=pending",
     label="✅ Filter sub-resource theo status")

call("patch", "/good/v1/orders/ord_001",
     data={"status": "cancelled"},
     label="✅ PATCH cập nhật trạng thái (không dùng /cancelOrder)")

call("patch", "/good/v1/orders/ord_001",
     data={"status": "INVALID_STATUS"},
     label="✅ Validation error cho enum field")

print(f"\n{'═' * 60}")
print("  🎉 Test hoàn thành!")
print(f"{'═' * 60}\n")
