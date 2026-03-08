"""
Week 3 – Demo: Bad API vs Good API Design
==========================================
So sánh trực tiếp API thiết kế kém và API chuẩn mực trên cùng một Flask app.

Chạy: python app.py
Bad  API: http://localhost:5000/bad/...
Good API: http://localhost:5000/good/v1/...
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────
# Dữ liệu mẫu (in-memory database)
# ─────────────────────────────────────────────────────────────────
USERS = [
    {"id": 1, "username": "nguyenvana", "email_address": "vana@gmail.com", "phone_number": "0901234567", "is_active": True, "created_at": "2024-01-10T08:00:00Z"},
    {"id": 2, "username": "tranthib",   "email_address": "b@gmail.com",    "phone_number": "0987654321", "is_active": True, "created_at": "2024-01-12T09:00:00Z"},
    {"id": 3, "username": "lehongc",    "email_address": "c@gmail.com",    "phone_number": "0912345678", "is_active": False,"created_at": "2024-01-14T10:00:00Z"},
]

ORDERS = [
    {"id": "ord_001", "user_id": 1, "status": "completed", "total_amount": 150000, "created_at": "2024-01-20T14:00:00Z"},
    {"id": "ord_002", "user_id": 1, "status": "pending",   "total_amount": 89000,  "created_at": "2024-01-21T10:00:00Z"},
    {"id": "ord_003", "user_id": 2, "status": "completed", "total_amount": 220000, "created_at": "2024-01-22T16:00:00Z"},
]


# ═════════════════════════════════════════════════════════════════
# ❌ BAD API – Thiết kế kém
# Các lỗi được cố ý đặt vào để minh họa trong buổi học
# ═════════════════════════════════════════════════════════════════

@app.route("/bad/getAllUsers", methods=["GET"])
def bad_get_all_users():
    """
    ❌ Lỗi 1: Dùng động từ 'get' trong URL
    ❌ Lỗi 2: Trả về mảng trực tiếp – không có envelope, không có pagination
    ❌ Lỗi 3: Field names không nhất quán (PascalCase)
    ❌ Lỗi 4: Không có versioning
    """
    # Trả mảng trực tiếp – không thể thêm pagination sau này mà không breaking!
    return jsonify([
        {
            "UserID": u["id"],
            "UserName": u["username"],
            "EmailAddress": u["email_address"],
        }
        for u in USERS
    ])


@app.route("/bad/createUser", methods=["POST"])
def bad_create_user():
    """
    ❌ Lỗi 1: Dùng động từ 'create' trong URL
    ❌ Lỗi 2: Status code trả về 200 thay vì 201 khi tạo mới
    ❌ Lỗi 3: Response thiếu data đầy đủ
    """
    data = request.get_json()
    return jsonify({"message": "User created successfully", "id": 99}), 200  # ❌ Phải là 201


@app.route("/bad/User_Profile", methods=["GET"])
def bad_get_user_profile():
    """
    ❌ Lỗi 1: PascalCase + Underscore trong URL
    ❌ Lỗi 2: Dùng query string cho resource ID thay vì path param
    ❌ Lỗi 3: Response fields không nhất quán (trộn lẫn nhiều convention)
    ❌ Lỗi 4: Date format không chuẩn
    """
    user_id = request.args.get("UserID", type=int)
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return jsonify({"msg": "not found"}), 404  # ❌ Error response không nhất quán

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "EmailAddr": user["email_address"],   # ❌ PascalCase trộn với snake_case
        "PhoneNum": user["phone_number"],      # ❌ Viết tắt + PascalCase
        "Created": "15-01-2024",               # ❌ Date format sai chuẩn
    })


@app.route("/bad/getOrdersByUserID/<int:user_id>", methods=["GET"])
def bad_get_orders_by_user(user_id):
    """
    ❌ Lỗi 1: Động từ + thông tin thừa trong URL
    ❌ Lỗi 2: Không thể hiện hierarchy (user → orders)
    ❌ Lỗi 3: Trả mảng trực tiếp, không có pagination
    ❌ Lỗi 4: Field names không nhất quán
    """
    user_orders = [o for o in ORDERS if o["user_id"] == user_id]
    return jsonify([
        {"order_id": o["id"], "Status": o["status"], "Amt": o["total_amount"]}
        for o in user_orders
    ])


# ═════════════════════════════════════════════════════════════════
# ✅ GOOD API – Thiết kế chuẩn mực
# ═════════════════════════════════════════════════════════════════

# ── Helper functions ──────────────────────────────────────────────

def success_response(data, status_code=200, pagination=None):
    """Tạo envelope response nhất quán cho thành công."""
    body = {"success": True, "data": data}
    if pagination:
        body["pagination"] = pagination
    return jsonify(body), status_code


def error_response(code, message, status_code, details=None):
    """Tạo envelope response nhất quán cho lỗi."""
    return jsonify({
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }), status_code


def paginate(items, page, limit):
    """Phân trang đơn giản."""
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    paged = items[start:end]
    total_pages = (total + limit - 1) // limit
    pagination = {
        "page": page,
        "limit": limit,
        "total_records": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return paged, pagination


# ── Users Endpoints ───────────────────────────────────────────────

@app.route("/good/v1/users", methods=["GET"])
def good_list_users():
    """
    ✅ GET /v1/users – Lấy danh sách users
    - Danh từ số nhiều, không có động từ
    - Versioning /v1/
    - Envelope pattern với pagination
    - Query string cho filter
    """
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    name_filter = request.args.get("name", "").lower()

    filtered = [u for u in USERS if name_filter in u["username"]] if name_filter else USERS[:]
    paged, pagination = paginate(filtered, page, limit)

    return success_response(paged, pagination=pagination)


@app.route("/good/v1/users", methods=["POST"])
def good_create_user():
    """
    ✅ POST /v1/users – Tạo user mới
    - HTTP Method POST + danh từ số nhiều
    - Trả 201 Created
    - Envelope response đầy đủ
    """
    data = request.get_json()
    if not data:
        return error_response("INVALID_BODY", "Request body is required.", 400)

    required = ["username", "email_address", "phone_number"]
    missing = [f for f in required if f not in data]
    if missing:
        return error_response(
            "VALIDATION_ERROR",
            "Missing required fields.",
            400,
            details=[{"field": f, "issue": "This field is required."} for f in missing],
        )

    # Kiểm tra email trùng
    if any(u["email_address"] == data["email_address"] for u in USERS):
        return error_response("CONFLICT", f"Email '{data['email_address']}' already exists.", 409)

    new_user = {
        "id": max(u["id"] for u in USERS) + 1,
        "username": data["username"],
        "email_address": data["email_address"],
        "phone_number": data["phone_number"],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    USERS.append(new_user)
    return success_response(new_user, status_code=201)


@app.route("/good/v1/users/<int:user_id>", methods=["GET"])
def good_get_user(user_id):
    """
    ✅ GET /v1/users/{user_id} – Lấy thông tin một user
    - Resource ID là path parameter
    - 404 đúng chuẩn khi không tìm thấy
    """
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("RESOURCE_NOT_FOUND", f"User with id '{user_id}' does not exist.", 404)
    return success_response(user)


@app.route("/good/v1/users/<int:user_id>", methods=["PATCH"])
def good_update_user(user_id):
    """
    ✅ PATCH /v1/users/{user_id} – Cập nhật một phần thông tin user
    - PATCH (cập nhật từng phần) vs PUT (thay thế toàn bộ)
    - Chỉ cho phép update các field cho phép
    """
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("RESOURCE_NOT_FOUND", f"User with id '{user_id}' does not exist.", 404)

    data = request.get_json() or {}
    allowed_fields = ["username", "email_address", "phone_number"]
    for field in allowed_fields:
        if field in data:
            user[field] = data[field]

    return success_response(user)


@app.route("/good/v1/users/<int:user_id>", methods=["DELETE"])
def good_delete_user(user_id):
    """
    ✅ DELETE /v1/users/{user_id} – Xóa user
    - Trả 204 No Content (không có body) khi thành công
    """
    global USERS
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("RESOURCE_NOT_FOUND", f"User with id '{user_id}' does not exist.", 404)

    USERS = [u for u in USERS if u["id"] != user_id]
    return "", 204  # ✅ 204 No Content – không có body


# ── Orders Endpoints (Sub-resource Hierarchy) ────────────────────

@app.route("/good/v1/users/<int:user_id>/orders", methods=["GET"])
def good_list_user_orders(user_id):
    """
    ✅ GET /v1/users/{user_id}/orders – Orders của một user
    - Thể hiện hierarchy: orders thuộc về user
    - Filter theo status
    - Pagination
    """
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("RESOURCE_NOT_FOUND", f"User with id '{user_id}' does not exist.", 404)

    status_filter = request.args.get("status")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    user_orders = [o for o in ORDERS if o["user_id"] == user_id]
    if status_filter:
        user_orders = [o for o in user_orders if o["status"] == status_filter]

    paged, pagination = paginate(user_orders, page, limit)
    return success_response(paged, pagination=pagination)


@app.route("/good/v1/orders/<string:order_id>", methods=["PATCH"])
def good_update_order_status(order_id):
    """
    ✅ PATCH /v1/orders/{order_id} – Cập nhật trạng thái đơn hàng
    - PATCH cho partial update
    - Không có "cancel" hay "update" trong URL
    """
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return error_response("RESOURCE_NOT_FOUND", f"Order with id '{order_id}' does not exist.", 404)

    data = request.get_json() or {}
    valid_statuses = ["pending", "completed", "cancelled"]
    if "status" in data:
        if data["status"] not in valid_statuses:
            return error_response(
                "VALIDATION_ERROR",
                f"Invalid status. Must be one of: {valid_statuses}",
                400,
            )
        order["status"] = data["status"]

    return success_response(order)


# ─────────────────────────────────────────────────────────────────
# Summary Endpoint – So sánh Bad vs Good
# ─────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Trang tổng hợp các endpoint để test."""
    return jsonify({
        "message": "Week 3 Demo – Bad API vs Good API",
        "bad_api_endpoints": [
            "GET  /bad/getAllUsers",
            "POST /bad/createUser",
            "GET  /bad/User_Profile?UserID=1",
            "GET  /bad/getOrdersByUserID/1",
        ],
        "good_api_endpoints": [
            "GET    /good/v1/users",
            "GET    /good/v1/users?page=1&limit=2&name=nguyen",
            "POST   /good/v1/users",
            "GET    /good/v1/users/1",
            "PATCH  /good/v1/users/1",
            "DELETE /good/v1/users/3",
            "GET    /good/v1/users/1/orders",
            "GET    /good/v1/users/1/orders?status=pending",
            "PATCH  /good/v1/orders/ord_001",
        ],
    })


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Week 3 Demo Server – API Design Best Practices")
    print("=" * 60)
    print("  Bad  API → http://localhost:5000/bad/...")
    print("  Good API → http://localhost:5000/good/v1/...")
    print("  Summary  → http://localhost:5000/")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
