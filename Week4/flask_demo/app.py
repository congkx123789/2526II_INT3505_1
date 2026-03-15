from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

# Cấu hình Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Book Management API (Flask)",
        "description": "API đơn giản để quản lý kho sách, tự động sinh từ docstrings.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "definitions": {
        "Book": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "example": "B001"},
                "title": {"type": "string", "example": "Sapiens: Lược sử loài người"},
                "author": {"type": "string", "example": "Yuval Noah Harari"},
                "publishedYear": {"type": "integer", "example": 2011},
                "genre": {"type": "string", "example": "Khoa học, Lịch sử"}
            }
        },
        "BookInput": {
            "type": "object",
            "required": ["title", "author"],
            "properties": {
                "title": {"type": "string"},
                "author": {"type": "string"},
                "publishedYear": {"type": "integer"},
                "genre": {"type": "string"}
            }
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=template)

# Database giả lập
books_db = []

@app.route('/books', methods=['GET'])
def get_books():
    """
    Lấy danh sách tất cả các cuốn sách
    ---
    responses:
      200:
        description: Thành công
        schema:
          type: array
          items:
            $ref: '#/definitions/Book'
    """
    return jsonify(books_db)

@app.route('/books', methods=['POST'])
def create_book():
    """
    Thêm một cuốn sách mới
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/BookInput'
    responses:
      201:
        description: Đã tạo thành công
        schema:
          $ref: '#/definitions/Book'
    """
    data = request.get_json()
    new_book = {
        "id": f"B{len(books_db)+1:03d}",
        "title": data.get("title"),
        "author": data.get("author"),
        "publishedYear": data.get("publishedYear"),
        "genre": data.get("genre")
    }
    books_db.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    """
    Lấy thông tin chi tiết một cuốn sách
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Thành công
        schema:
          $ref: '#/definitions/Book'
      404:
        description: Không tìm thấy sách
    """
    book = next((b for b in books_db if b["id"] == id), None)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
