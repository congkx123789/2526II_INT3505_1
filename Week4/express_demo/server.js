const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const app = express();
app.use(express.json());

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Book Management API (Express)',
      version: '1.0.0',
      description: 'API đơn giản để quản lý kho sách, tự động sinh từ JSDoc.',
    },
    servers: [
      {
        url: '/',
        description: 'Current environment (Local/Vercel)',
      },
    ],
  },
  apis: ['./server.js'], // Đường dẫn tới file chứa các annotation
};

const specs = swaggerJsdoc(options);
app.use(
  '/api-docs',
  swaggerUi.serve,
  swaggerUi.setup(specs, {
    customCssUrl:
      'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css',
    customJs: [
      'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.js',
      'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-standalone-preset.js',
    ],
  })
);

/**
 * @openapi
 * components:
 *   schemas:
 *     Book:
 *       type: object
 *       properties:
 *         id:
 *           type: string
 *           example: B001
 *         title:
 *           type: string
 *           example: "Sapiens: Lược sử loài người"
 *         author:
 *           type: string
 *           example: Yuval Noah Harari
 *         publishedYear:
 *           type: integer
 *           example: 2011
 *         genre:
 *           type: string
 *           example: "Khoa học, Lịch sử"
 *     BookInput:
 *       type: object
 *       required:
 *         - title
 *         - author
 *       properties:
 *         title:
 *           type: string
 *         author:
 *           type: string
 *         publishedYear:
 *           type: integer
 *         genre:
 *           type: string
 */

let books = [];

/**
 * @openapi
 * /books:
 *   get:
 *     summary: Lấy danh sách tất cả các cuốn sách
 *     responses:
 *       200:
 *         description: Thành công
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Book'
 */
app.get('/books', (req, res) => {
  res.json(books);
});

/**
 * @openapi
 * /books:
 *   post:
 *     summary: Thêm một cuốn sách mới
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/BookInput'
 *     responses:
 *       201:
 *         description: Đã tạo thành công
 */
app.post('/books', (req, res) => {
  const newBook = { id: `B${(books.length + 1).toString().padStart(3, '0')}`, ...req.body };
  books.push(newBook);
  res.status(201).json(newBook);
});

/**
 * @openapi
 * /books/{id}:
 *   get:
 *     summary: Lấy thông tin chi tiết một cuốn sách
 *     parameters:
 *       - name: id
 *         in: path
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Thành công
 *       404:
 *         description: Không tìm thấy sách
 */
app.get('/books/:id', (req, res) => {
  const book = books.find(b => b.id === req.params.id);
  if (book) res.json(book);
  else res.status(404).json({ message: 'Book not found' });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Swagger docs available at http://localhost:${PORT}/api-docs`);
  });
}

module.exports = app;
