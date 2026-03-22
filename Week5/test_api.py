import unittest
import json
from app import app, books, loans

class LibraryAPITestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        self.app = app.test_client()
        self.app.testing = True

    def test_get_books_pagination_page_based(self):
        # 5 books total, request page 1, size 2
        response = self.app.get('/books?page=1&size=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['meta']['page'], 1)
        self.assertEqual(data['meta']['size'], 2)
        self.assertEqual(data['meta']['total_pages'], 3)
        self.assertEqual(data['meta']['total_items'], 5)

    def test_get_books_search_and_sort(self):
        # Filter by title 'Harry' and sort by published_year descending
        response = self.app.get('/books?title=Harry&sort=-published_year')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # 3 matching books: 1999, 1998, 1997
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(data['data'][0]['published_year'], 1999)
        self.assertEqual(data['data'][1]['published_year'], 1998)
        self.assertEqual(data['data'][2]['published_year'], 1997)

    def test_get_single_book(self):
        response = self.app.get('/books/b1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Harry Potter and the Sorcerer's Stone")

    def test_post_user_loan(self):
        initial_loans = len(loans)
        payload = {"book_id": "b2"}
        response = self.app.post('/users/u2/loans', json=payload)
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], 'u2')
        self.assertEqual(data['book_id'], 'b2')
        self.assertEqual(data['status'], 'BORROWED')
        self.assertEqual(len(loans), initial_loans + 1)

if __name__ == '__main__':
    unittest.main()
