from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

# --- Mock Data ---
authors = [
    {"id": "a1", "name": "J.K. Rowling"},
    {"id": "a2", "name": "George R. R. Martin"}
]

books = [
    {"id": "b1", "title": "Harry Potter and the Sorcerer's Stone", "isbn": "111", "published_year": 1997, "quantity": 5, "author_id": "a1", "category": "Fiction"},
    {"id": "b2", "title": "Harry Potter and the Chamber of Secrets", "isbn": "222", "published_year": 1998, "quantity": 3, "author_id": "a1", "category": "Fiction"},
    {"id": "b3", "title": "A Game of Thrones", "isbn": "333", "published_year": 1996, "quantity": 4, "author_id": "a2", "category": "Fantasy"},
    {"id": "b4", "title": "A Clash of Kings", "isbn": "444", "published_year": 1998, "quantity": 2, "author_id": "a2", "category": "Fantasy"},
    {"id": "b5", "title": "Harry Potter and the Prisoner of Azkaban", "isbn": "555", "published_year": 1999, "quantity": 6, "author_id": "a1", "category": "Fiction"}
]

users = [
    {"id": "u1", "full_name": "John Doe", "email": "john@example.com", "registered_at": "2023-01-01"},
    {"id": "u2", "full_name": "Jane Smith", "email": "jane@example.com", "registered_at": "2023-02-15"}
]

loans = [
    {"id": "l1", "user_id": "u1", "book_id": "b1", "borrow_date": "2023-10-01", "return_date": "2023-10-15", "status": "RETURNED"}
]

@app.route('/books', methods=['GET'])
def get_books():
    title = request.args.get('title')
    category = request.args.get('category')
    author_id = request.args.get('author_id')
    sort = request.args.get('sort')
    page = request.args.get('page')
    size = request.args.get('size')
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    result = list(books)

    # Search & Filter
    if title:
        result = [b for b in result if title.lower() in b['title'].lower()]
    if category:
        result = [b for b in result if category.lower() == b['category'].lower()]
    if author_id:
        result = [b for b in result if author_id == b['author_id']]

    # Sorting
    if sort:
        is_desc = sort.startswith('-')
        field = sort[1:] if is_desc else sort
        result.sort(key=lambda x: x.get(field, ''), reverse=is_desc)

    total_items = len(result)
    meta = {"total_items": total_items}
    paginated_data = result

    # Pagination
    if page or size:
        p = int(page) if page else 1
        s = int(size) if size else 10
        start_index = (p - 1) * s
        paginated_data = result[start_index:start_index + s]
        total_pages = (total_items + s - 1) // s
        meta.update({"page": p, "size": s, "total_pages": total_pages})
    elif offset is not None or limit is not None:
        o = int(offset) if offset is not None else 0
        l = int(limit) if limit is not None else 10
        paginated_data = result[o:o + l]
        meta.update({"offset": o, "limit": l})

    return jsonify({"data": paginated_data, "meta": meta})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = {"id": f"b{len(books) + 1}"}
    new_book.update(data)
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<string:id>', methods=['GET'])
def get_book_by_id(id):
    book = next((b for b in books if b['id'] == id), None)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<string:id>/loans', methods=['GET'])
def get_user_loans(id):
    user_loans = [l for l in loans if l['user_id'] == id]
    return jsonify(user_loans)

@app.route('/users/<string:id>/loans', methods=['POST'])
def add_user_loan(id):
    data = request.json
    new_loan = {
        "id": f"l{len(loans) + 1}",
        "user_id": id,
        "book_id": data.get('book_id'),
        "borrow_date": str(date.today()),
        "return_date": None,
        "status": "BORROWED"
    }
    loans.append(new_loan)
    return jsonify(new_loan), 201

@app.route('/books/<string:id>/authors', methods=['GET'])
def get_book_authors(id):
    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    author = next((a for a in authors if a['id'] == book['author_id']), None)
    return jsonify([author] if author else [])

if __name__ == '__main__':
    app.run(port=5000)
