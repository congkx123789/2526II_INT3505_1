from datetime import datetime

# In-memory mock database cho đơn hàng (Orders) và danh sách Webhook Subscriptions

orders = [
    {
        "id": "ORD-001",
        "customer": "Nguyen Van A",
        "product": "Khóa học API Design Patterns",
        "amount": 1500000,
        "status": "PENDING",
        "createdAt": "2026-05-18T10:00:00Z"
    },
    {
        "id": "ORD-002",
        "customer": "Tran Thi B",
        "product": "Khóa học Microservices",
        "amount": 2500000,
        "status": "PAID",
        "createdAt": "2026-05-18T11:30:00Z"
    },
    {
        "id": "ORD-003",
        "customer": "Le Van C",
        "product": "Khóa học Kubernetes",
        "amount": 2000000,
        "status": "CANCELLED",
        "createdAt": "2026-05-18T12:00:00Z"
    },
    {
        "id": "ORD-004",
        "customer": "Pham Minh D",
        "product": "Khóa học System Design",
        "amount": 3000000,
        "status": "PAID",
        "createdAt": "2026-05-18T14:15:00Z"
    }
]

webhook_subscriptions = [
    {
        "id": "SUB-001",
        "url": "http://localhost:3000/api/webhooks/receiver", # Endpoint mặc định để test demo
        "events": ["order.created", "order.updated", "payment.success"],
        "secret": "whsec_supersecretkey123" # Secret key dùng để ký HMAC SHA256
    }
]

notifications = [
    {
        "id": "NOTIF-001",
        "type": "SYSTEM_EVENT",
        "message": "Hệ thống Flask API E-learning khởi tạo thành công.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
]
