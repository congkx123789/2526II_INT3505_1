const client = require('prom-client');

// Thu thập thông số hệ thống Node.js (RAM, CPU)
client.collectDefaultMetrics();

// Biến đếm tổng số request
const httpRequestCounter = new client.Counter({
    name: 'http_requests_total',
    help: 'Tổng số request vào API',
    labelNames: ['method', 'route', 'status']
});

module.exports = { client, httpRequestCounter };
