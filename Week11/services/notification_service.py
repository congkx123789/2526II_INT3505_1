from datetime import datetime
import time
from database import notifications

class NotificationService:
    @staticmethod
    def add_notification(notif_type, message, related_data=None):
        if related_data is None:
            related_data = {}
        new_notif = {
            "id": f"NOTIF-{int(time.time() * 1000)}",
            "type": notif_type,
            "message": message,
            "data": related_data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        notifications.insert(0, new_notif) # Thêm vào đầu danh sách
        print(f"[Notification Service] Đã tạo thông báo mới: \"{message}\"")
        return new_notif

    @staticmethod
    def get_notifications(limit=10):
        return notifications[:limit]
