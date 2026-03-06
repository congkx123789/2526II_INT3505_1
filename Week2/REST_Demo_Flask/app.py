from flask import Flask, request, jsonify, render_template, make_response
import jwt
import json
import hashlib

app = Flask(__name__)
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

@app.route('/api/secure-data', methods=['GET'])
def secure_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        token = token.split(" ")[1] 
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Welcome admin!', 'secret_data': 'Phi trạng thái có nghĩa là Server quên bạn ngay sau khi gửi xong Request.'})
    except Exception as e:
        return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

# ==========================================================
# 4. Cacheable
# ==========================================================
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_etag(product_id):
    """
    Sử dụng ETag để tiết kiệm băng thông khi Data chưa bị sờ tới.
    """
    product = next((p for p in db_products if p["id"] == product_id), None)
    if not product:
        return jsonify({"message": "Not Found"}), 404
        
    # Tạo mã băm ETAG 
    product_str = json.dumps(product, sort_keys=True).encode('utf-8')
    etag_hash = hashlib.md5(product_str).hexdigest()
    
    # Kiểm tra ETAG trong HTTP Headers Browser nếu nó quay lại
    if_none_match = request.headers.get('If-None-Match')
    
    if if_none_match and if_none_match.strip('"') == etag_hash:
        # Nếu Data Database trùng khớp mã ETag của Client gửi lên (100% Data giống nhau)
        # Server ngắt kết nối luôn và trả 304 - Băng thông siêu thấp
        return '', 304 

    response = make_response(jsonify(product))
    response.set_etag(etag_hash)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
