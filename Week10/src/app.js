const express = require('express');
const logger = require('./utils/logger');
const { client } = require('./utils/metrics');
const auditLogAndMetrics = require('./middlewares/auditLog');
const apiLimiter = require('./middlewares/rateLimiter');
const { breaker } = require('./services/dataService');

const app = express();

// 1. Gắn Middleware theo dõi
app.use(auditLogAndMetrics);

// 2. Định nghĩa Route Metrics (Dành cho Prometheus)
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', client.register.contentType);
    res.send(await client.register.metrics());
});

// 3. API an toàn (Áp dụng Rate Limit)
app.use('/api/', apiLimiter);

app.get('/api/ping', (req, res) => {
    res.json({ message: "Pong! Hệ thống hoạt động bình thường." });
});

// 4. API rủi ro (Áp dụng Circuit Breaker)
app.get('/api/unstable', async (req, res) => {
    try {
        const result = await breaker.fire();
        res.json(result);
    } catch (error) {
        // Opossum handle fallback, but we should catch any unexpected errors
        res.status(500).json({ error: error.message });
    }
});

// Khởi động
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    logger.info(`API Server đã chạy tại http://localhost:${PORT}`);
});
