import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_stateless():
    print(f"\n{'='*60}\n3. Thử nghiệm STATELESS (Phi trạng thái)\n{'='*60}")
    try:
        print("[Mô phỏng 1] Client cố tình gọi dữ liệu bảo mật mà KHÔNG CÓ TOKEN:")
        print("Client gửi: GET /api/secure-data")
        res1 = requests.get(f'{BASE_URL}/api/secure-data')
        print(f"Server từ chối (Status: {res1.status_code}) - Lỗi: {res1.json()}")
        
        print("\n[Mô phỏng 2] Client tiến hành đăng nhập để lấy Token (Không lưu Session ở Server):")
        print("Client gửi: POST /api/login với username='admin'")
        res2 = requests.post(f'{BASE_URL}/api/login', json={"username": "admin"})
        token = res2.json().get('token')
        print(f"Thành công! Client nhận được Token: {token[:30]}...")
        
        print("\n[Mô phỏng 3] Client đính kèm Token vào Header để lấy dữ liệu (Server KHÔNG cần bộ nhớ Session):")
        print("Client gửi: GET /api/secure-data (kèm header Authorization: Bearer <token>)")
        res3 = requests.get(f'{BASE_URL}/api/secure-data', headers={'Authorization': f'Bearer {token}'})
        print(f"Server chấp nhận (Status {res3.status_code}) - Dữ liệu: {res3.json()}")
        print("\n=> GIẢI THÍCH: Nhờ có Token ở mỗi request, Server quên hoàn toàn Client sau khi login. Khi request thứ 3 bay tới, Server đọc Token -> giải mã ra chữ 'admin' -> biết được ai đang gọi và trả data. Việc mở rộng Server (Scale-out) dễ dàng vì các Server không cần đồng bộ RAM cho Session.")
    except Exception as e:
         print("Lỗi kết nối tới Server. Hãy đảm bảo 'python app.py' đang chạy trên cổng 5000!")

if __name__ == "__main__":
    test_stateless()
