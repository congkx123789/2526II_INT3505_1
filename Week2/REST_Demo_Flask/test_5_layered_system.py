import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_layered_system():
    print(f"\n{'='*60}\n5. Thử nghiệm LAYERED SYSTEM (Hệ thống phân lớp)\n{'='*60}")
    try:
        print("Mô phỏng: Client gửi HTTP Request đến máy chủ Web Server. Nó không cần phân biệt đằng sau là ngõ cụt 1 server (Flask 5000) hay là cả một Load Balancer chia tải cho 100 máy nội bộ đằng sau.")
        print("\nChúng ta gửi HTTP OPTIONS để xem cách CORS/Proxy phản hồi tại biên:")
        
        response = requests.options(f'{BASE_URL}/api/products')
        print(f"Client gửi: OPTIONS /api/products")
        print(f"Status phản hồi (Tại Node biên/CORS Middleware): {response.status_code}")
        print("Trích xuất một số Headers từ Node nhận lệnh:")
        for k, v in response.headers.items():
            if 'Access-Control' in k or 'Server' in k:
                print(f" - {k}: {v}")
                
        print("\n=> GIẢI THÍCH: Tính chất phân lớp mang lại khả năng bảo mật che giấu IP nội bộ. Lớp API Gateway/CORS Middleware có vai trò cản các luồng kết nối độc hại hoặc kiểm soát Access-Control từ sớm. Bản thân Code Controller bên trong của Server/Python không cần phải bận tâm việc lọc IP hay điều hướng Proxy.")
    except Exception as e:
        print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_layered_system()
