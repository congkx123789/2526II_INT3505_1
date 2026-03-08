import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_client_server():
    print(f"\n{'='*60}\n2. Thử nghiệm CLIENT-SERVER\n{'='*60}")
    print("Mô hình: Trình duyệt (Client) độc lập gọi lấy HTML chứa UI, sau đó UI tự động gọi Data từ API Server để ráp lại.")
    try:
        print("Client gửi: GET / (Để lấy file HTML giao diện thuần túy)")
        response = requests.get(f'{BASE_URL}/')
        
        print(f"Server trả về Status: {response.status_code}")
        print(f"Header Content-Type: {response.headers.get('Content-Type')}")
        print("Nội dung trả về là HTML tĩnh (không có layout bị gắn cứng với dữ liệu từ Database ở Backend):")
        print(response.text[:200] + " \n... (HTML bị ẩn đi để bớt dài) ...")
        print("\n=> GIẢI THÍCH: Giao diện (Client - HTML/JS) chạy hoàn toàn trọn vẹn độc lập. Client có thể nằm bên app Mobile hay React. Chúng chỉ gọi Backend (Server Python) qua URL API để lấy dữ liệu thay vì bắt Server làm luôn nhiệm vụ sinh giao diện.")
    except Exception as e:
        print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_client_server()
