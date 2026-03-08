import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_uniform_interface():
    print(f"\n{'='*60}\n1. Thử nghiệm UNIFORM INTERFACE & HATEOAS\n{'='*60}")
    print("Client gửi: GET /api/products")
    try:
        response = requests.get(f'{BASE_URL}/api/products')
        print(f"Server trả về Status: {response.status_code}")
        print("Dữ liệu JSON Server trả về (Lưu ý mảng 'links'):")
        print(response.json())
        print("\n=> GIẢI THÍCH: Server không chỉ trả về dữ liệu (products), mà còn cung cấp sẵn các đường dẫn (hyperlinks) ở trường 'links'. Client biết ngay rằng nó có thể gọi POST vào '/api/products' để tạo mới sản phẩm mà không cần phải tự đoán dựa trên tài liệu API.")
    except Exception as e:
        print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_uniform_interface()
