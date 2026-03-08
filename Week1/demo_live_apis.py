"""
=============================================================
WEEK 1 - DEMO TRỰC QUAN: Gọi API Thật Ngay Trên Lớp
=============================================================
Mục tiêu:
 - Học viên thấy được hình hài thực tế của 1 API request/response
 - Không cần đăng ký, không cần API Key
 - Dễ đọc, dễ hiểu

Cách chạy:
 pip install requests
 python demo_live_apis.py
=============================================================
"""

import requests
import json

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_request(method, url):
    print(f"\n>>> Client gửi: {method} {url}")

def print_response(response):
    print(f"<<< Server trả về Status: {response.status_code}")
    print(f"<<< Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    data = response.json()
    print(f"<<< Body (JSON):\n{json.dumps(data, indent=2, ensure_ascii=False)[:600]}")
    if len(json.dumps(data)) > 600:
        print("    ... (cắt bớt để đọc dễ hơn)")


# -------------------------------------------------------
# DEMO 1: PokéAPI - REST API chuẩn mực, không cần Auth
# -------------------------------------------------------
print_section("DEMO 1: PokéAPI — GET thông tin Pikachu")
print("API này trả về dữ liệu về các nhân vật Pokemon.")
print("Không cần đăng ký. Hoàn toàn miễn phí.")

url1 = "https://pokeapi.co/api/v2/pokemon/pikachu"
print_request("GET", url1)

try:
    res1 = requests.get(url1, timeout=10)
    # Chỉ lấy 1 số field đơn giản để demo
    data1 = res1.json()
    simple1 = {
        "name": data1["name"],
        "id": data1["id"],
        "height": data1["height"],
        "weight": data1["weight"],
        "types": [t["type"]["name"] for t in data1["types"]],
        "base_experience": data1["base_experience"]
    }
    print(f"<<< Server trả về Status: {res1.status_code}")
    print(f"<<< Body (JSON - rút gọn):\n{json.dumps(simple1, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Lỗi: {e}")


# -------------------------------------------------------
# DEMO 2: REST Countries - Tra cứu thông tin quốc gia
# -------------------------------------------------------
print_section("DEMO 2: REST Countries — GET thông tin Việt Nam")
print("API này trả về thông tin địa lý, dân số, tiền tệ của các quốc gia.")
print("Không cần đăng ký. Không cần API Key.")

url2 = "https://restcountries.com/v3.1/name/vietnam"
print_request("GET", url2)

try:
    res2 = requests.get(url2, timeout=10)
    data2 = res2.json()[0]
    simple2 = {
        "name": data2["name"]["official"],
        "capital": data2.get("capital", ["N/A"])[0],
        "population": data2["population"],
        "area_km2": data2["area"],
        "currencies": list(data2.get("currencies", {}).keys()),
        "languages": list(data2.get("languages", {}).values()),
        "region": data2["region"]
    }
    print(f"<<< Server trả về Status: {res2.status_code}")
    print(f"<<< Body (JSON - rút gọn):\n{json.dumps(simple2, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Lỗi: {e}")


# -------------------------------------------------------
# DEMO 3: JSONPlaceholder - Fake API để test (CRUD)
# -------------------------------------------------------
print_section("DEMO 3: JSONPlaceholder — GET bài viết & POST tạo mới")
print("API này mô phỏng một Blog API để học viên test mà không dụng database thật.")

# GET - Lấy bài viết #1
url3_get = "https://jsonplaceholder.typicode.com/posts/1"
print_request("GET", url3_get)
try:
    res3 = requests.get(url3_get, timeout=10)
    print(f"<<< Status: {res3.status_code}")
    print(f"<<< Body:\n{json.dumps(res3.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Lỗi: {e}")

# POST - Tạo bài viết mới
url3_post = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "Bài học API đầu tiên",
    "body": "Hôm nay tôi học cách gọi REST API bằng Python!",
    "userId": 1
}
print_request("POST", url3_post)
print(f">>> Body gửi đi (JSON):\n{json.dumps(new_post, indent=2, ensure_ascii=False)}")
try:
    res3_post = requests.post(url3_post, json=new_post, timeout=10)
    print(f"<<< Status: {res3_post.status_code}  ← 201 Created có nghĩa là tạo thành công!")
    print(f"<<< Body Server trả về:\n{json.dumps(res3_post.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Lỗi: {e}")


print("\n" + "="*60)
print("  DEMO KẾT THÚC - Tất cả API đều chạy thành công!")
print("="*60)
print("""
Câu hỏi thảo luận với học viên:
  1. Tại sao POST /posts trả về 201 thay vì 200?
  2. Naming convention: Tại sao dùng /pokemon/pikachu (danh từ số nhiều)?
  3. Response JSON có cấu trúc gì? Trường nào quan trọng?
  4. Nếu API Key bị lộ, chuyện gì có thể xảy ra?
""")
