# 📚 Danh Sách API Gợi Ý Để Phân Tích

> Chọn **3 API** từ danh sách dưới đây để hoàn thành bài tập.
> Nếu muốn tìm API ngoài danh sách này, hãy trao đổi với thầy trước!

---

## 🟢 Nhóm Dễ — Không cần Auth hoặc Auth rất đơn giản

Phù hợp nếu đây là lần đầu bạn tiếp xúc với API.

| Tên API | Link Docs | Đặc điểm nổi bật |
|---|---|---|
| **PokéAPI** | https://pokeapi.co/ | Dữ liệu về Pokémon. Chuẩn RESTful, không cần đăng ký. |
| **JSONPlaceholder** | https://jsonplaceholder.typicode.com/ | Fake API để test: Users, Posts, Comments. Hoàn toàn miễn phí. |
| **REST Countries** | https://restcountries.com/ | Trả về thông tin về các quốc gia: dân số, diện tích, tiền tệ. |
| **Open Library API** | https://openlibrary.org/developers/api | Tra cứu thông tin sách theo ISBN, tên tác giả... |
| **Agify.io** | https://agify.io/ | Đoán tuổi dựa trên tên người. Ví dụ: `/api?name=michael` |

---

## 🟡 Nhóm Thực Tế — Cần đăng ký API Key

Cần tạo tài khoản miễn phí để lấy API Key. Trải nghiệm sát thực tế nhất!

| Tên API | Link Docs | Đặc điểm nổi bật |
|---|---|---|
| **OpenWeatherMap** | https://openweathermap.org/api | Dữ liệu thời tiết toàn cầu. _(Xem ví dụ mẫu thầy đã làm)_ |
| **TMDB (The Movie DB)** | https://developer.themoviedb.org/docs | Tra cứu phim, diễn viên, review phim. |
| **CoinGecko API** | https://www.coingecko.com/api/documentation | Giá tiền điện tử (Bitcoin, ETH...) theo thời gian thực. |
| **NewsAPI** | https://newsapi.org/ | Tin tức toàn cầu theo từ khóa, nguồn báo. |
| **Nutritionix API** | https://www.nutritionix.com/business/api | Thông tin dinh dưỡng thực phẩm. |

---

## 🔴 Nhóm Nâng Cao — Phân tích sự khác biệt kiến trúc

Phù hợp nếu bạn muốn thử thách thêm. Mục tiêu: so sánh REST vs GraphQL.

| Tên API | Link Docs | Đặc điểm nổi bật |
|---|---|---|
| **GitHub REST API** | https://docs.github.com/rest | Quản lý repo, user, issue... Rất đầy đủ tài liệu. |
| **GitHub GraphQL API** | https://docs.github.com/graphql | **Cùng dữ liệu đó nhưng dùng GraphQL!** Hãy so sánh sự khác biệt với REST. |
| **Shopify GraphQL** | https://shopify.dev/docs/api/storefront | API thương mại điện tử dùng GraphQL. |

---

## 💡 Câu hỏi thầy sẽ hỏi khi chữa bài

Hãy suy nghĩ trước các câu hỏi này khi phân tích API của bạn:

1. **"Điểm tốt trong cách thiết kế của API này là gì?"**
   _(Ví dụ: Tên endpoint rõ ràng? Response JSON có cấu trúc logic? Auth an toàn?)_

2. **"Nếu là em, em có đổi tên endpoint đó không? Đổi thành gì?"**
   _(Gợi ý để dẫn vào Buổi 3: Nguyên tắc thiết kế REST)_

3. **"Em đã thử gọi thử API này chưa? Dùng công cụ gì?"**
   _(Thử dùng Postman hoặc gõ thẳng URL vào trình duyệt)_

---

> **📌 Ghi chú:** Bài tập nộp dưới dạng file `.md` (Markdown) hoặc trên Notion.
> Deadline: Trước 15 phút đầu của **Buổi 2**.
