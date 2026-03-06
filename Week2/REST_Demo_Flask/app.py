from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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
# Cung cấp giao diện đồng nhất: '/api/products' (Dùng chung 1 Danh từ, khác Động từ GET/POST)
@app.route('/api/products', methods=['GET'])
def get_products():
    """ 
    HATEOAS: Phản hồi không chỉ có Data, mà có đính kèm các hyperlink 
    hướng dẫn Client hành động tiếp theo có thể làm gì với Resource này.
    """
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
    """
    Sử dụng đúng HTTP Method POST để tạo mới tài nguyên thay vì dùng Endpoint lạ.
    """
    new_product = request.json
    db_products.append(new_product)
    return jsonify({"message": "Product created successfully", "product": new_product}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
