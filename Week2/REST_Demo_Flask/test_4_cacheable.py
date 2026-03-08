import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_cacheable():
    print(f"\n{'='*60}\n4. Thử nghiệm CACHEABLE (ETag)\n{'='*60}")
    try:
        print("[Lần 1] Trình duyệt tải Sản phẩm (ID=1) lần đầu tiên:")
        res1 = requests.get(f'{BASE_URL}/api/product/1')
        etag = res1.headers.get('ETag')
        print(f"Status: {res1.status_code}")
        print(f"Server trả về dữ liệu DB: {res1.json()}")
        print(f"Server dặn Client: 'Hãy nhớ mã thẻ băm ETag này nhé -> {etag}'")
        
        print("\n[Lần 2] Trình duyệt tải lại Sản phẩm. Nó đính kèm mã ETag cũ vào request thông qua Header 'If-None-Match':")
        headers = {'If-None-Match': etag}
        res2 = requests.get(f'{BASE_URL}/api/product/1', headers=headers)
        print(f"Client gửi: GET /api/product/1 (Header: If-None-Match={etag})")
        print(f"Status trả về: {res2.status_code} (Theo chuẩn HTTP nghĩa là Not Modified - Không thay đổi)")
        print(f"Nội dung thân Server trả về: '{res2.text}' (Trống rỗng!)")
        print("\n=> GIẢI THÍCH: Nhờ mã băm ETag trùng khớp, Server biết Content chưa bị sửa đổi. Do đó, Server chỉ trả Status 304 ngắn lọn để tiết kiệm vô số băng thông data. Trình duyệt nhận 304 sẽ TỰ ĐỘNG mang cái kết quả {Macbook...} cũ đã cất trong máy ra hiển thị.")
    except Exception as e:
        print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_cacheable()
