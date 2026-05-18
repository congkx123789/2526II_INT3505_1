import time
from flask import Blueprint, request, jsonify
from database import webhook_subscriptions
from services.webhook_service import WebhookService
from services.notification_service import NotificationService

webhooks_bp = Blueprint('webhooks', __name__, url_prefix='/api/webhooks')
notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@webhooks_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    url = data.get('url')
    events = data.get('events')
    secret = data.get('secret')

    if not url or not events or not secret:
        return jsonify({
            "success": False,
            "message": "Vui lòng cung cấp url, events (array) và secret key"
        }), 400

    if not isinstance(events, list):
        events = [events]

    new_sub = {
        "id": f"SUB-{int(time.time() * 1000)}",
        "url": url,
        "events": events,
        "secret": secret
    }
    webhook_subscriptions.append(new_sub)
    print(f"[Webhook Controller] Đã đăng ký webhook subscription mới: {url}")

    return jsonify({
        "success": True,
        "message": "Đăng ký webhook thành công",
        "data": new_sub
    }), 201

@webhooks_bp.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    return jsonify({
        "success": True,
        "data": webhook_subscriptions
    }), 200

@webhooks_bp.route('/receiver', methods=['POST'])
def receive_webhook():
    signature = request.headers.get('X-Webhook-Signature')
    event_header = request.headers.get('X-Webhook-Event')
    
    data_json = request.get_json() or {}
    event = event_header or data_json.get('event', 'unknown')

    print(f"[Webhook Receiver] Nhận được webhook sự kiện: {event}")

    if not signature:
        print("[Webhook Receiver] Từ chối request vì thiếu header X-Webhook-Signature")
        return jsonify({"success": False, "message": "Thiếu chữ ký xác thực (Missing signature)"}), 401

    receiver_secret = "whsec_supersecretkey123"

    raw_data_str = request.get_data(as_text=True)
    is_valid = WebhookService.verify_signature(raw_data_str, signature, receiver_secret)

    if not is_valid:
        print("[Webhook Receiver] Xác thực chữ ký THẤT BẠI (Invalid Signature)")
        return jsonify({"success": False, "message": "Chữ ký không hợp lệ (Forbidden)"}), 403

    print("[Webhook Receiver] Xác thực chữ ký THÀNH CÔNG.")

    event_id = data_json.get('eventId', 'N/A')
    related_data = data_json.get('data', {})
    order_id = related_data.get('id', 'N/A')

    NotificationService.add_notification(
        f"WEBHOOK_RECEIVED_{event.upper()}",
        f"Nhận thông báo webhook [{event}]: Đơn hàng {order_id} đã được cập nhật.",
        related_data
    )

    return jsonify({
        "success": True,
        "message": "Webhook đã được tiếp nhận và xử lý thành công",
        "eventId": event_id
    }), 200

@notifications_bp.route('', methods=['GET'])
def get_notifications():
    notifs = NotificationService.get_notifications()
    return jsonify({
        "success": True,
        "count": len(notifs),
        "data": notifs
    }), 200
