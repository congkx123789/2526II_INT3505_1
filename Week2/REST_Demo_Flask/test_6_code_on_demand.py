import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_code_on_demand():
    print(f"\n{'='*60}\n6. Thử nghiệm CODE ON DEMAND (Mã linh hoạt)\n{'='*60}")
    try:
        print("Chức năng của nút nhấn trên bộ giao diện Client chưa hoàn chỉnh. Nó gửi API để x\in Server đoạn code UI.")
        print("Client gửi: GET /api/get-dynamic-script")
        res = requests.get(f'{BASE_URL}/api/get-dynamic-script')
        
        print(f"\nServer định nghĩa phản hồi bằng Header 'Content-Type': {res.headers.get('Content-Type')}")
        print(f"Mã JS thực tế (Không phải định dạng JSON) Server tải trực tiếp xuống máy Client:\n")
        print(res.text)
        
        print("\n=> GIẢI THÍCH: Thay vì trả Data, Server truyền Logic (Mã thực thi). JavaScript này sẽ được gắn vào tài nguyên HTML tại Client và chạy qua ngàm nối (eval hoặc <script> injection). Rất linh hoạt nhưng rủi ro XSS bảo mật cao. Chỉ là tùy chọn (Optional) trong REST.")
    except Exception as e:
        print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_code_on_demand()
