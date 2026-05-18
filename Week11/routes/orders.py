import time
from datetime import datetime
from flask import Blueprint, request, jsonify, url_for
from database import orders
from services.webhook_service import WebhookService
from services.notification_service import NotificationService

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

def get_hateoas_links(order_id):
    base_url = "http://localhost:3000/api/orders"
    return {
        "self": {"href": f"{base_url}/{order_id}", "method": "GET"},
        "update": {"href": f"{base_url}/{order_id}", "method": "PUT"},
        "delete": {"href": f"{base_url}/{order_id}", "method": "DELETE"},
        "pay": {"href": f"{base_url}/{order_id}/pay", "method": "POST"}
    }

@orders_bp.route('', methods=['GET'])
def get_orders():
    status_filter = request.args.get('status')
    sort_by = request.args.get('sortBy')
    order_direction = request.args.get('order', 'ASC').upper()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    result = list(orders)

    # 1. Filtering by status
    if status_filter:
        result = [o for o in result if o['status'].upper() == status_filter.upper()]

    # 2. Sorting
    if sort_by and sort_by in ['amount', 'createdAt']:
        reverse = (order_direction == 'DESC')
        result.sort(key=lambda x: x.get(sort_by), reverse=reverse)

    # 3. Pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    total_items = len(result)
    paginated_items = result[start_index:end_index]

    # 4. HATEOAS Links
    items_with_links = []
    for item in paginated_items:
        item_copy = dict(item)
        item_copy['_links'] = get_hateoas_links(item['id'])
        items_with_links.append(item_copy)

    total_pages = (total_items + limit - 1) // limit

    return jsonify({
        "success": True,
        "count": len(items_with_links),
        "pagination": {
            "totalItems": total_items,
            "totalPages": total_pages,
            "currentPage": page,
            "limit": limit
        },
        "data": items_with_links,
        "_links": {
            "self": {"href": "http://localhost:3000" + request.full_path.rstrip('?'), "method": "GET"},
            "create": {"href": "http://localhost:3000/api/orders", "method": "POST"}
        }
    }), 200

@orders_bp.route('/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"success": False, "message": "Không tìm thấy đơn hàng"}), 404

    order_data = dict(order)
    order_data['_links'] = get_hateoas_links(order['id'])
    return jsonify({"success": True, "data": order_data}), 200

@orders_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    customer = data.get('customer')
    product = data.get('product')
    amount = data.get('amount')

    if not customer or not product or amount is None:
        return jsonify({"success": False, "message": "Vui lòng cung cấp đủ customer, product, amount"}), 400

    new_order = {
        "id": f"ORD-{int(time.time() * 1000)}",
        "customer": customer,
        "product": product,
        "amount": amount,
        "status": "PENDING",
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    orders.append(new_order)

    # Phát sự kiện Webhook (Event-driven)
    WebhookService.dispatch_event("order.created", new_order)

    # Ghi thông báo hệ thống
    NotificationService.add_notification(
        "ORDER_CREATED",
        f"Đơn hàng mới {new_order['id']} vừa được tạo bởi {customer}.",
        new_order
    )

    resp_data = dict(new_order)
    resp_data['_links'] = get_hateoas_links(new_order['id'])

    return jsonify({
        "success": True,
        "message": "Tạo đơn hàng thành công",
        "data": resp_data
    }), 201

@orders_bp.route('/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order_idx = next((i for i, o in enumerate(orders) if o['id'] == order_id), -1)

    if order_idx == -1:
        return jsonify({"success": False, "message": "Không tìm thấy đơn hàng"}), 404

    current_order = orders[order_idx]
    current_order['customer'] = data.get('customer', current_order['customer'])
    current_order['product'] = data.get('product', current_order['product'])
    if 'amount' in data:
        current_order['amount'] = data['amount']
    if 'status' in data:
        current_order['status'] = data['status']

    # Phát sự kiện Webhook
    WebhookService.dispatch_event("order.updated", current_order)

    resp_data = dict(current_order)
    resp_data['_links'] = get_hateoas_links(current_order['id'])

    return jsonify({
        "success": True,
        "message": "Cập nhật đơn hàng thành công",
        "data": resp_data
    }), 200

@orders_bp.route('/<order_id>/pay', methods=['POST'])
def pay_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"success": False, "message": "Không tìm thấy đơn hàng"}), 404

    if order['status'] == 'PAID':
        return jsonify({"success": False, "message": "Đơn hàng này đã được thanh toán"}), 400

    order['status'] = 'PAID'

    # Phát sự kiện thanh toán thành công
    WebhookService.dispatch_event("payment.success", order)

    NotificationService.add_notification(
        "PAYMENT_SUCCESS",
        f"Đơn hàng {order['id']} đã thanh toán thành công số tiền {order['amount']} VND.",
        order
    )

    resp_data = dict(order)
    resp_data['_links'] = get_hateoas_links(order['id'])

    return jsonify({
        "success": True,
        "message": "Thanh toán đơn hàng thành công",
        "data": resp_data
    }), 200

@orders_bp.route('/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order_idx = next((i for i, o in enumerate(orders) if o['id'] == order_id), -1)
    if order_idx == -1:
        return jsonify({"success": False, "message": "Không tìm thấy đơn hàng"}), 404

    deleted = orders.pop(order_idx)
    return jsonify({
        "success": True,
        "message": "Xóa đơn hàng thành công",
        "data": deleted
    }), 200
