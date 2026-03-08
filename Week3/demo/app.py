"""
Week 3 Demo: API Design Best Practices
======================================
Comparing Bad vs Good API design on a single Flask app.

Endpoints:
- Bad  API: /bad/...
- Good API: /good/v1/...
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# -----------------------------------------------------------------
# In-memory Database
# -----------------------------------------------------------------
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


# =================================================================
# ❌ BAD API - Poor Design Examples
# =================================================================

@app.route("/bad/getAllUsers", methods=["GET"])
def bad_get_all_users():
    """
    Issues:
    - Verb 'get' in URL.
    - Flat array response (no envelope, no metadata).
    - Non-standard PascalCase keys.
    """
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
    Issues:
    - Verb 'create' in URL.
    - Incorrect Status Code (200 instead of 201).
    - Opaque response with missing data.
    """
    return jsonify({"message": "User created successfully", "id": 99}), 200


@app.route("/bad/User_Profile", methods=["GET"])
def bad_get_user_profile():
    """
    Issues:
    - Mixed casing/symbols in URL.
    - ID in query string instead of path parameter.
    - Inconsistent response naming.
    - Non-ISO date format.
    """
    user_id = request.args.get("UserID", type=int)
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return jsonify({"msg": "not found"}), 404

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "EmailAddr": user["email_address"],
        "PhoneNum": user["phone_number"],
        "Created": "15-01-2024",
    })


@app.route("/bad/getOrdersByUserID/<int:user_id>", methods=["GET"])
def bad_get_orders_by_user(user_id):
    """
    Issues:
    - Redundant info in URL.
    - No resource hierarchy.
    - Missing pagination.
    """
    user_orders = [o for o in ORDERS if o["user_id"] == user_id]
    return jsonify([
        {"order_id": o["id"], "Status": o["status"], "Amt": o["total_amount"]}
        for o in user_orders
    ])


# =================================================================
# ✅ GOOD API - Best Practices
# =================================================================

def success_response(data, status_code=200, pagination=None):
    """Standardized success envelope."""
    body = {"success": True, "data": data}
    if pagination:
        body["pagination"] = pagination
    return jsonify(body), status_code


def error_response(code, message, status_code, details=None):
    """Standardized error envelope."""
    return jsonify({
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }), status_code


def paginate(items, page, limit):
    """Simple pagination logic."""
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    paged = items[start:end]
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    
    pagination = {
        "page": page,
        "limit": limit,
        "total_records": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return paged, pagination


@app.route("/good/v1/users", methods=["GET"])
def good_list_users():
    """
    Best Practices:
    - Plural nouns, no verbs.
    - Versioned prefix (/v1/).
    - Envelope with pagination.
    - Filtering via query strings.
    """
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    name_filter = request.args.get("name", "").lower()

    filtered = [u for u in USERS if name_filter in u["username"].lower()] if name_filter else USERS[:]
    paged, pagination = paginate(filtered, page, limit)

    return success_response(paged, pagination=pagination)


@app.route("/good/v1/users", methods=["POST"])
def good_create_user():
    """
    Best Practices:
    - Proper POST method usage.
    - 201 Created status.
    - Validation handled gracefully.
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
            details=[{"field": f, "issue": "Required field."} for f in missing],
        )

    if any(u["email_address"] == data["email_address"] for u in USERS):
        return error_response("CONFLICT", "Email already exists.", 409)

    new_user = {
        "id": max(u["id"] for u in USERS) + 1,
        "username": data["username"],
        "email_address": data["email_address"],
        "phone_number": data["phone_number"],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    USERS.append(new_user)
    return success_response(new_user, status_code=201)


@app.route("/good/v1/users/<int:user_id>", methods=["GET"])
def good_get_user(user_id):
    """RESTful retrieval via ID."""
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("NOT_FOUND", "User not found.", 404)
    return success_response(user)


@app.route("/good/v1/users/<int:user_id>", methods=["PATCH"])
def good_update_user(user_id):
    """Partial updates using PATCH."""
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return error_response("NOT_FOUND", "User not found.", 404)

    data = request.get_json() or {}
    for field in ["username", "email_address", "phone_number"]:
        if field in data:
            user[field] = data[field]

    return success_response(user)


@app.route("/good/v1/users/<int:user_id>", methods=["DELETE"])
def good_delete_user(user_id):
    """Standard DELETE with 204 No Content."""
    global USERS
    if not any(u["id"] == user_id for u in USERS):
        return error_response("NOT_FOUND", "User not found.", 404)

    USERS = [u for u in USERS if u["id"] != user_id]
    return "", 204


@app.route("/good/v1/users/<int:user_id>/orders", methods=["GET"])
def good_list_user_orders(user_id):
    """Hierarchy: Orders belong to a specific User."""
    if not any(u["id"] == user_id for u in USERS):
        return error_response("NOT_FOUND", "User not found.", 404)

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
    """Updating Order status without verbs in the URL."""
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return error_response("NOT_FOUND", "Order not found.", 404)

    data = request.get_json() or {}
    valid_statuses = ["pending", "completed", "cancelled"]
    if "status" in data:
        if data["status"] not in valid_statuses:
            return error_response("VALIDATION_ERROR", f"Invalid status. Choose from: {valid_statuses}", 400)
        order["status"] = data["status"]

    return success_response(order)


@app.route("/", methods=["GET"])
def index():
    """Discovery endpoint listing available APIs."""
    return jsonify({
        "message": "Week 3 Demo - API Design Best Practices",
        "bad_api": [
            "GET  /bad/getAllUsers",
            "POST /bad/createUser",
            "GET  /bad/User_Profile?UserID=1",
            "GET  /bad/getOrdersByUserID/1",
        ],
        "good_api": [
            "GET    /good/v1/users",
            "POST   /good/v1/users",
            "GET    /good/v1/users/1",
            "PATCH  /good/v1/users/1",
            "DELETE /good/v1/users/3",
            "GET    /good/v1/users/1/orders",
            "PATCH  /good/v1/orders/ord_001",
        ],
    })


if __name__ == "__main__":
    print(f"\n{'='*60}\n  Week 3 Demo: API Best Practices\n{'='*60}")
    print("  Root     -> http://localhost:5000/")
    print("  Bad API  -> /bad/...")
    print("  Good API -> /good/v1/...\n")
    app.run(debug=True, port=5000)

