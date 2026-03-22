const express = require('express');
const app = express();
const port = 3000;

// Middleware to parse JSON body
app.use(express.json());

// --- Mock Data (Mô phỏng Database) ---
let authors = [
  { id: 'a1', name: 'J.K. Rowling' },
  { id: 'a2', name: 'George R. R. Martin' }
];

let books = [
  { id: 'b1', title: 'Harry Potter and the Sorcerer is Stone', isbn: '111', published_year: 1997, quantity: 5, author_id: 'a1', category: 'Fiction' },
  { id: 'b2', title: 'Harry Potter and the Chamber of Secrets', isbn: '222', published_year: 1998, quantity: 3, author_id: 'a1', category: 'Fiction' },
  { id: 'b3', title: 'A Game of Thrones', isbn: '333', published_year: 1996, quantity: 4, author_id: 'a2', category: 'Fantasy' },
  { id: 'b4', title: 'A Clash of Kings', isbn: '444', published_year: 1998, quantity: 2, author_id: 'a2', category: 'Fantasy' },
  { id: 'b5', title: 'Harry Potter and the Prisoner of Azkaban', isbn: '555', published_year: 1999, quantity: 6, author_id: 'a1', category: 'Fiction' },
];

let users = [
  { id: 'u1', full_name: 'John Doe', email: 'john@example.com', registered_at: '2023-01-01' },
  { id: 'u2', full_name: 'Jane Smith', email: 'jane@example.com', registered_at: '2023-02-15' }
];

let loans = [
  { id: 'l1', user_id: 'u1', book_id: 'b1', borrow_date: '2023-10-01', return_date: '2023-10-15', status: 'RETURNED' }
];

// ==========================================
// 1. ROOT RESOURCES (TÀI NGUYÊN ĐỘC LẬP)
// ==========================================

// [GET] /books: Tích hợp Tìm kiếm (Search), Lọc (Filter), Sắp xếp (Sort) & Phân trang (Pagination)
app.get('/books', (req, res) => {
  let { title, category, author_id, sort, page, size, offset, limit } = req.query;
  let result = [...books];

  // A. Search & Filter (Tìm kiếm & Lọc)
  if (title) result = result.filter(b => b.title.toLowerCase().includes(title.toLowerCase()));
  if (category) result = result.filter(b => b.category.toLowerCase() === category.toLowerCase());
  if (author_id) result = result.filter(b => b.author_id === author_id);

  // B. Sorting (Sắp xếp) - vd: sort=-published_year (Giảm dần theo năm)
  if (sort) {
    const isDesc = sort.startsWith('-');
    const field = isDesc ? sort.substring(1) : sort;
    result.sort((a, b) => {
      if (a[field] < b[field]) return isDesc ? 1 : -1;
      if (a[field] > b[field]) return isDesc ? -1 : 1;
      return 0;
    });
  }

  const totalItems = result.length;
  let paginatedData = result;
  let meta = { total_items: totalItems };

  // C. Pagination (Phân trang)
  // 1. Theo chiến lược Page-based (Khuyên dùng cho bài tập)
  if (page || size) {
    const p = parseInt(page) || 1;
    const s = parseInt(size) || 10;
    const startIndex = (p - 1) * s;
    paginatedData = result.slice(startIndex, startIndex + s);
    meta = { ...meta, page: p, size: s, total_pages: Math.ceil(totalItems / s) };
  } 
  // 2. Theo chiến lược Offset/Limit (Dựa trên độ lệch)
  else if (offset !== undefined || limit !== undefined) {
    const o = parseInt(offset) || 0;
    const l = parseInt(limit) || 10;
    paginatedData = result.slice(o, o + l);
    meta = { ...meta, offset: o, limit: l };
  }

  // Trả về dữ liệu chuẩn JSON
  res.json({ data: paginatedData, meta });
});

// [POST] /books: Thêm sách mới
app.post('/books', (req, res) => {
  const newBook = { id: `b${books.length + 1}`, ...req.body };
  books.push(newBook);
  res.status(201).json(newBook);
});

// [GET] /books/{id}: Xem chi tiết 1 quyển sách
app.get('/books/:id', (req, res) => {
  const book = books.find(b => b.id === req.params.id);
  if (!book) return res.status(404).json({ message: 'Book not found' });
  res.json(book);
});

// [GET] /users: Lấy danh sách độc giả
app.get('/users', (req, res) => {
  res.json(users);
});


// ==========================================
// 2. SUB-RESOURCES (TÀI NGUYÊN LỒNG NHAU)
// ==========================================

// [GET] /users/{id}/loans: Xem lịch sử mượn sách của 1 Độc giả cụ thể
app.get('/users/:id/loans', (req, res) => {
  const userLoans = loans.filter(l => l.user_id === req.params.id);
  res.json(userLoans);
});

// [POST] /users/{id}/loans: Tạo phiếu mượn sách cho Độc giả
app.post('/users/:id/loans', (req, res) => {
  const { book_id } = req.body;
  const newLoan = {
    id: `l${loans.length + 1}`,
    user_id: req.params.id,
    book_id: book_id,
    borrow_date: new Date().toISOString().split('T')[0], // Ngày hiện tại
    return_date: null,
    status: 'BORROWED' // Trạng thái đang mượn
  };
  loans.push(newLoan);
  res.status(201).json(newLoan);
});

// [GET] /books/{id}/authors: Xem thông tin tác giả của quyển sách (Lấy thêm thông tin quan hệ)
app.get('/books/:id/authors', (req, res) => {
  const book = books.find(b => b.id === req.params.id);
  if (!book) return res.status(404).json({ message: 'Book not found' });
  
  const author = authors.find(a => a.id === book.author_id);
  res.json(author ? [author] : []); 
});

// Khởi chạy server
app.listen(port, () => {
  console.log(`API quản lý Thư Viện đang chạy tại đường dẫn: http://localhost:${port}`);
  console.log(`- Thử test API tìm kiếm/phân trang: http://localhost:${port}/books?title=Harry&page=1&size=2&sort=-published_year`);
});
