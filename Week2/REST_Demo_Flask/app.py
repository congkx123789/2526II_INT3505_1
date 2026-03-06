from flask import Flask, request, jsonify, render_template
import jwt

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
    """
    Client lấy Token. Server KHÔNG LƯU session trong RAM hay ổ cứng.
    """
    data = request.json
    if data and data.get('username') == 'admin':
        token = jwt.encode({'user': 'admin'}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/secure-data', methods=['GET'])
def secure_data():
    """
    Client BẮT BUỘC gửi kèm Token ở mọi Request nếu muốn pass qua cửa này.
    Server tự giải nghĩa Token chứ Server không tra Session từ Database.
    Hệ thống lúc này có Scale 10 máy lên cũng không sập vì chia sẻ Session dễ dàng.
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    
    try:
        token = token.split(" ")[1] # Xóa chữ Bearer
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Welcome admin!', 'secret_data': 'Phi trạng thái có nghĩa là Server quên bạn ngay sau khi gửi xong Request.'})
    except Exception as e:
        return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
