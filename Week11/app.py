from flask import Flask, jsonify, request
from routes.orders import orders_bp
from routes.webhooks import webhooks_bp, notifications_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Đăng ký Blueprints
app.register_blueprint(orders_bp)
app.register_blueprint(webhooks_bp)
app.register_blueprint(notifications_bp)

@app.before_request
def log_request():
    print(f"[HTTP Request] {request.method} {request.path}")

@app.route('/', methods=['GET'])
def index():
    base_url = "http://localhost:3000"
    return jsonify({
        "success": True,
        "message": "Hệ thống Demo Flask API Design Patterns (Week 11 - 12)",
        "description": "Minh họa kết hợp CRUD, Query (filtering/sorting/pagination), HATEOAS, Webhook, Event-driven bằng Python Flask",
        "_links": {
            "orders": {"href": f"{base_url}/api/orders", "method": "GET"},
            "create_order": {"href": f"{base_url}/api/orders", "method": "POST"},
            "webhook_subscribe": {"href": f"{base_url}/api/webhooks/subscribe", "method": "POST"},
            "webhook_subscriptions": {"href": f"{base_url}/api/webhooks/subscriptions", "method": "GET"},
            "notifications": {"href": f"{base_url}/api/notifications", "method": "GET"}
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Endpoint không tồn tại"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Lỗi máy chủ nội bộ", "error": str(error)}), 500

if __name__ == '__main__':
    print("====================================================")
    print("🚀 Week 11 Flask API Server đang chạy tại: http://localhost:3000")
    print("====================================================")
    app.run(host='0.0.0.0', port=3000, debug=False)
