from flask import Flask, request, jsonify, render_template, make_response, Response
from flask_cors import CORS
import jwt
import json
import hashlib
from functools import wraps

app = Flask(__name__)

# ==========================================================
# 5. Layered System
# ==========================================================
# Cấu hình CORS ở cấp Server App: Tự động phát hành Header kiểm duyệt 
# Middleware CORS hoạt động như 1 lớp (layer) bảo vệ ngoài cùng chặn requests.
CORS(app)

app.config['SECRET_KEY'] = 'my_super_secret_key'

# Mock Database
db_products = [
    {"id": 1, "name": "Macbook Pro", "price": 2000},
    {"id": 2, "name": "Dell XPS", "price": 1500}
]

# ==========================================================
# 2. Client-Server (Separation of Concerns)
# ==========================================================
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================================
# 1. Uniform Interface & HATEOAS
# ==========================================================
@app.route('/api/products', methods=['GET'])
def get_products():
    response_data = {
        "data": db_products,
        "links": [
            {"rel": "self", "href": "/api/products", "method": "GET"},
            {"rel": "add_product", "href": "/api/products", "method": "POST"}
        ]
    }
    return jsonify(response_data), 200

@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.json
    db_products.append(new_product)
    return jsonify({"message": "Product created successfully", "product": new_product}), 201

# ==========================================================
# 3. Stateless
# ==========================================================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data and data.get('username') == 'admin':
        token = jwt.encode({'user': 'admin'}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # You could pass the decoded user info to the function if needed
            # current_user = data['user']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({
        'message': 'Welcome admin!', 
        'secret_data': 'Phi trạng thái là Server quên bạn ngay sau khi gửi xong Request.'
    })

# ==========================================================
# 4. Cacheable
# ==========================================================
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_etag(product_id):
    product = next((p for p in db_products if p["id"] == product_id), None)
    if not product:
        return jsonify({"message": "Not Found"}), 404
        
    product_str = json.dumps(product, sort_keys=True).encode('utf-8')
    etag_hash = hashlib.md5(product_str).hexdigest()
    
    if_none_match = request.headers.get('If-None-Match')
    if if_none_match and if_none_match.strip('"') == etag_hash:
        return '', 304 

    response = make_response(jsonify(product))
    response.set_etag(etag_hash)
    return response

# ==========================================================
# 6. Code on Demand
# ==========================================================
@app.route('/api/get-dynamic-script', methods=['GET'])
def get_dynamic_script():
    """
    Tùy chọn. Server không trả Data Data tĩnh nữa mà đẩy nguyên 1 mảnh Code (Hàm JS). 
    Client có thể tải xuống và chạy Hàm JS này.
    """
    js_code = """
        console.log("Mã này được cấp phát từ Server API");
        function showGreeting() {
            alert("Xin chào! Tính năng này được thực thi từ mảnh Javascript Python truyền xuống!");
        }
        window.showGreeting = showGreeting;
    """
    return Response(js_code, mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
