from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Mock Database
db_products = [
    {"id": 1, "name": "Macbook Pro", "price": 2000},
    {"id": 2, "name": "Dell XPS", "price": 1500}
]

# ==========================================================
# 2. Client-Server (Separation of Concerns)
# ==========================================================
# Giao diện UI (Frontend/Client) được phục vụ độc lập và xử lý riêng rẽ 
# với dữ liệu API (Backend/Server).
@app.route('/')
def index():
    # Phục vụ file giao diện HTML thuần túy. 
    # File này chứa Javascript tự gọi Data về sau.
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    """ 
    API Cung cấp dữ liệu JSON thuần túy thay vì trả HTML chứa Data.
    Frontend sẽ nhận chuỗi JSON này để ráp giao diện.
    """
    return jsonify(db_products), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
