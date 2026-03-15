import unittest
import json
import sys
import os

# Thêm đường dẫn để import app từ flask_demo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset database giả lập (trong thực tế nên dùng database riêng cho test)
        import app as api_module
        api_module.books_db = []

    def test_create_book(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "publishedYear": 2024,
            "genre": "Testing"
        }
        response = self.app.post('/books', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Book")
        self.assertIn('id', data)

    def test_get_all_books(self):
        # Thêm 1 sách trước
        self.app.post('/books', 
                      data=json.dumps({"title": "B1", "author": "A1"}),
                      content_type='application/json')
        
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_single_book(self):
        # Thêm sách
        res = self.app.post('/books', 
                           data=json.dumps({"title": "B1", "author": "A1"}),
                           content_type='application/json')
        book_id = json.loads(res.data)['id']

        response = self.app.get(f'/books/{book_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], book_id)

    def test_get_book_not_found(self):
        response = self.app.get('/books/B999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
