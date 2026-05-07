const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
    windowMs: 10 * 1000, // Cấu hình 10 giây (để dễ test)
    max: 3,              // Tối đa 3 request trong 10 giây
    message: { error: 'Cảnh báo bảo mật: Bạn đang spam hệ thống!' },
    standardHeaders: true, 
    legacyHeaders: false,
});

module.exports = apiLimiter;
