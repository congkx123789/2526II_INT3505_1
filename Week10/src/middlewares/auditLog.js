const logger = require('../utils/logger');
const { httpRequestCounter } = require('../utils/metrics');

const auditLogAndMetrics = (req, res, next) => {
    res.on('finish', () => {
        // Tăng bộ đếm metrics
        httpRequestCounter.inc({ method: req.method, route: req.path, status: res.statusCode });
        
        // Ghi log
        logger.info(`${req.method} ${req.path} - Trạng thái: ${res.statusCode} - IP: ${req.ip}`);
    });
    next();
};

module.exports = auditLogAndMetrics;
