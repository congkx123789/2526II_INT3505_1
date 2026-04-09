# Báo cáo So sánh Hiệu năng Pagination: Offset vs Cursor

## 1. Tổng quan
Trong kiến trúc Microservices, việc phân trang (pagination) là cực kỳ quan trọng để xử lý lượng dữ liệu lớn. Hai kỹ thuật phổ biến nhất là **Offset-based Pagination** và **Cursor-based Pagination**.

Báo cáo này trình bày kết quả đo lường thực tế trên tập dữ liệu **1,000,000 records** bằng SQLite.

## 2. Kết quả Thử nghiệm (Benchmark Results)

Dưới đây là thời gian thực thi (milliseconds) cho việc lấy 10 bản ghi ở các vị trí khác nhau trong tập dữ liệu:

| Offset / Depth | Offset Time (ms) | Cursor Time (ms) | Speedup (Cursor/Offset) |
| :--- | :--- | :--- | :--- |
| 0 | 0.0750 | 0.0242 | ~3.1x |
| 1,000 | 0.0236 | 0.0150 | ~1.5x |
| 10,000 | 0.0878 | 0.0193 | ~4.5x |
| 100,000 | 0.7274 | 0.0260 | ~28x |
| 500,000 | 3.5716 | 0.0283 | ~126x |
| 900,000 | 6.4024 | 0.0338 | **~189x** |

## 3. Phân tích Chi tiết

### Offset-based Pagination (`LIMIT 10 OFFSET X`)
- **Cơ chế:** Database phải quét qua $X$ bản ghi đầu tiên, bỏ qua chúng, rồi mới lấy 10 bản ghi tiếp theo.
- **Vấn đề:** Khi $X$ càng lớn (deep paging), Database càng tốn nhiều tài nguyên CPU và I/O để quét qua các bản ghi không cần thiết.
- **Hiệu năng:** Giảm dần theo cấp số tuyến tính $O(N)$.
- **Ưu điểm:** Dễ triển khai, hỗ trợ nhảy đến trang bất kỳ (trang 1, trang 100...).
- **Nhược điểm:** Hiệu năng kém ở trang cuối, dữ liệu có thể bị trùng hoặc sót nếu có bản ghi mới được thêm/xóa trong lúc phân trang.

### Cursor-based Pagination (`WHERE id > X LIMIT 10`)
- **Cơ chế:** Database sử dụng Index (thường là Primary Key) để nhảy trực tiếp đến điểm bắt đầu ($id > X$) và lấy 10 bản ghi.
- **Hiệu năng:** Luôn ổn định ở mức $O(log N)$ nhờ vào cấu trúc B-Tree của Index.
- **Ưu điểm:** Tốc độ cực nhanh (nhanh hơn ~200 lần ở cuối tập dữ liệu), không bị ảnh hưởng bởi việc thêm/xóa dữ liệu giữa các trang (data drift).
- **Nhược điểm:** Khó triển khai hơn, không hỗ trợ nhảy đến một trang bất kỳ (chỉ có thể đi "Next" hoặc "Previous").

## 4. Kết luận cho Microservices
Trong các hệ thống Microservices xử lý dữ liệu lớn (như feed mạng xã hội, lịch sử giao dịch), **Cursor-based Pagination** là lựa chọn tối ưu để đảm bảo trải nghiệm người dùng mượt mà và giảm tải cho Database Server. 

## 5. Hướng dẫn chạy Demo

Để tự chạy lại các thử nghiệm và kiểm chứng kết quả, bạn hãy thực hiện theo các bước sau:

1.  **Cài đặt Python**: Đảm bảo máy của bạn đã cài đặt Python 3.
2.  **Mở Terminal**: Di chuyển vào thư mục `Pagination_Benchmark`.
    ```bash
    cd Pagination_Benchmark
    ```
3.  **Chạy script**: Chạy lệnh sau để khởi tạo dữ liệu và bắt đầu đo lường.
    ```bash
    python3 benchmark.py
    ```
4.  **Xem kết quả**: Kết quả sẽ được in trực tiếp ra terminal theo dạng bảng so sánh.

> [!NOTE]
> Quá trình khởi tạo ban đầu (chèn 1 triệu records) có thể mất khoảng 10-20 giây tùy vào tốc độ ổ cứng của bạn. Các lần chạy sau sẽ sử dụng file database có sẵn nếu bạn không xóa nó.
