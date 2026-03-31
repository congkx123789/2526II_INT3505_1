require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;
const SECRET_KEY = process.env.SECRET_KEY || 'default-secret-key';
const REFRESH_SECRET_KEY = process.env.REFRESH_SECRET_KEY || 'default-refresh-secret';

app.use(express.json());
app.use(cookieParser());
app.use(cors({ origin: true, credentials: true })); // Cho phép gửi Cookie

// --- Mock User Database ---
const users = {
  admin: {
    id: 1,
    username: 'admin',
    password: 'password123',
    role: 'admin',
    scopes: ['read:profile', 'read:admin_data', 'write:admin_data']
  },
  user: {
    id: 2,
    username: 'user',
    password: 'password456',
    role: 'student',
    scopes: ['read:profile']
  }
};

// --- Middleware: Verify Access Token ---
const verifyToken = (req, res, next) => {
  // Ưu tiên lấy từ Cookie, nếu không thấy thì lấy từ Authorization Header
  let token = req.cookies.access_token || '';
  
  if (!token && req.headers.authorization) {
    if (req.headers.authorization.startsWith('Bearer ')) {
      token = req.headers.authorization.split(' ')[1];
    }
  }

  if (!token) return res.status(401).json({ message: 'Authentication required' });

  jwt.verify(token, SECRET_KEY, (err, decoded) => {
    if (err) return res.status(403).json({ message: 'Invalid or expired token' });
    req.user = decoded;
    next();
  });
};

// --- Middleware: RBAC (Roles) ---
const authorizeRoles = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ message: `Forbidden: Role ${req.user.role} not authorized` });
    }
    next();
  };
};

// --- Auth Endpoints ---

// ✅ CHẾ ĐỘ 1: ĐĂNG NHẬP KHÔNG AN TOÀN (LỘ TOKEN)
app.post('/api/login-insecure', (req, res) => {
  const { username, password } = req.body;
  const user = users[username];

  if (user && user.password === password) {
    const accessToken = jwt.sign({ id: user.id, username: user.username, role: user.role, scopes: user.scopes }, SECRET_KEY, { expiresIn: '15m' });
    const refreshToken = jwt.sign({ id: user.id }, REFRESH_SECRET_KEY, { expiresIn: '7d' });

    // TRẢ VỀ TOKEN TRONG BODY -> DẪN ĐẾN RỦI RO LỘ TOKEN (TOKEN LEAKAGE)
    return res.json({ access_token: accessToken, refresh_token: refreshToken });
  }
  res.status(401).json({ message: 'Invalid credentials' });
});

// ✅ CHẾ ĐỘ 2: ĐĂNG NHẬP AN TOÀN (DÙNG HTTPONLY COOKIE)
app.post('/api/login-secure', (req, res) => {
  const { username, password } = req.body;
  const user = users[username];

  if (user && user.password === password) {
    const accessToken = jwt.sign({ id: user.id, username: user.username, role: user.role, scopes: user.scopes }, SECRET_KEY, { expiresIn: '15m' });
    
    // ĐẶT TOKEN VÀO COOKIE HTTPONLY (KHÔNG THỂ BỊ JAVASCRIPT ĐỌC)
    res.cookie('access_token', accessToken, {
      httpOnly: true, // Ngăn chặn XSS
      secure: false,  // Để false cho Demo Local (HTTPS thì true)
      sameSite: 'strict',
      maxAge: 15 * 60 * 1000 // 15 phút
    });

    return res.json({ message: 'Logged in securely with HttpOnly Cookie' });
  }
  res.status(401).json({ message: 'Invalid credentials' });
});

app.post('/api/logout', (req, res) => {
  res.clearCookie('access_token');
  res.json({ message: 'Logged out' });
});

// --- Protected Resources ---

app.get('/api/profile', verifyToken, (req, res) => {
  res.json({ user: req.user, message: 'Welcome to your protected profile!' });
});

app.get('/api/admin-only', verifyToken, authorizeRoles('admin'), (req, res) => {
  res.json({ message: 'Access granted: Secret admin data retrieved!' });
});

app.listen(PORT, () => {
  console.log(`Node.js Auth Server is running on http://localhost:${PORT}`);
});
