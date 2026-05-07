const CircuitBreaker = require('opossum');

// Giả lập một hàm gọi Database hoặc API bên ngoài cực kỳ chập chờn
const fetchExternalData = async () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (Math.random() > 0.4) reject(new Error("Lỗi kết nối DB/API"));
            resolve({ data: "Dữ liệu quan trọng lấy thành công!" });
        }, 500);
    });
};

// Bọc hàm trên bằng Circuit Breaker
const breaker = new CircuitBreaker(fetchExternalData, {
    timeout: 1000,               // Chờ tối đa 1s
    errorThresholdPercentage: 50,// Tỷ lệ lỗi > 50% là ngắt mạch
    resetTimeout: 5000           // 5 giây sau mới thử mở mạch lại
});

// Fallback: Nếu mạch bị ngắt (Open), trả về cái này ngay lập tức
breaker.fallback(() => ({ warning: "Dịch vụ đang gián đoạn, đây là dữ liệu tạm (Cache)." }));

module.exports = { breaker };
