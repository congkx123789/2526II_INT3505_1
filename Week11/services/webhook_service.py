import hmac
import hashlib
import json
import time
import threading
import requests
from datetime import datetime
from database import webhook_subscriptions

class WebhookService:
    @staticmethod
    def generate_signature(payload_str, secret):
        """
        Tạo chữ ký HMAC SHA256 cho chuỗi payload dữ liệu (Tương tự Stripe / GitHub)
        """
        secret_bytes = bytes(secret, 'utf-8')
        payload_bytes = bytes(payload_str, 'utf-8')
        return hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()

    @staticmethod
    def verify_signature(payload_str, signature, secret):
        """
        Kiểm tra tính hợp lệ của chữ ký HMAC SHA256
        """
        expected_signature = WebhookService.generate_signature(payload_str, secret)
        return hmac.compare_digest(expected_signature, signature)

    @staticmethod
    def _post_webhook_async(url, payload_str, headers):
        try:
            print(f"[Webhook Dispatcher] Gửi HTTP POST đến {url}...")
            response = requests.post(url, data=payload_str, headers=headers, timeout=5)
            print(f"[Webhook Dispatcher] Gửi THÀNH CÔNG đến {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"[Webhook Dispatcher] Gửi THẤT BẠI đến {url} - Error: {str(e)}")

    @staticmethod
    def dispatch_event(event_name, data):
        """
        Phát sự kiện (Event dispatch) đến các webhook subscriber trong một thread riêng
        """
        print(f"[Webhook Dispatcher] Bắt đầu xử lý sự kiện: {event_name}")

        payload_obj = {
            "eventId": f"evt_{int(time.time() * 1000)}",
            "event": event_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data
        }
        
        # Chuẩn hóa chuỗi JSON chính xác để tính HMAC và gửi đi
        payload_str = json.dumps(payload_obj, ensure_ascii=False, separators=(',', ':'))

        subscribers = [sub for sub in webhook_subscriptions if event_name in sub["events"] or "*" in sub["events"]]

        if not subscribers:
            print(f"[Webhook Dispatcher] Không có subscriber nào đăng ký sự kiện {event_name}.")
            return

        for sub in subscribers:
            signature = WebhookService.generate_signature(payload_str, sub["secret"])
            headers = {
                "Content-Type": "application/json",
                "X-Webhook-Signature": signature,
                "X-Webhook-Event": event_name
            }
            thread = threading.Thread(target=WebhookService._post_webhook_async, args=(sub["url"], payload_str, headers))
            thread.daemon = True
            thread.start()
