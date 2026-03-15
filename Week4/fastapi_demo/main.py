from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Khởi tạo ứng dụng FastAPI và định nghĩa thông tin chung cho OpenAPI/Swagger
app = FastAPI(
    title="Book Management API",
    description="API đơn giản để quản lý kho sách trong thư viện.",
    version="1.0.0",
    servers=[
        {"url": "http://localhost:8000", "description": "Local development server"}
    ]
)

# Định nghĩa Schema cho lúc thêm mới/cập nhật (BookInput) - tương ứng với components/schemas/BookInput
class BookInput(BaseModel):
    title: str = Field(..., examples=["Sapiens: Lược sử loài người"])
    author: str = Field(..., examples=["Yuval Noah Harari"])
    publishedYear: Optional[int] = Field(None, examples=[2011])
    genre: Optional[str] = Field(None, examples=["Khoa học, Lịch sử"]) # Trường thể loại được thêm vào

# Định nghĩa Schema cho sách hiển thị (Book) - tương ứng với components/schemas/Book
class Book(BookInput):
    id: str = Field(..., examples=["B001"])

# Database giả lập
books_db = []

@app.get("/books", response_model=List[Book], summary="Lấy danh sách tất cả các cuốn sách")
def get_books():
    return books_db

@app.post("/books", response_model=Book, status_code=201, summary="Thêm một cuốn sách mới")
def create_book(book_input: BookInput):
    new_book = Book(id=f"B{len(books_db)+1:03d}", **book_input.model_dump())
    books_db.append(new_book)
    return new_book

@app.get("/books/{id}", response_model=Book, summary="Lấy thông tin chi tiết một cuốn sách")
def get_book(id: str):
    for b in books_db:
        if b.id == id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{id}", response_model=Book, summary="Cập nhật thông tin sách")
def update_book(id: str, book_input: BookInput):
    for i, b in enumerate(books_db):
        if b.id == id:
            updated_book = Book(id=id, **book_input.model_dump())
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}", status_code=204, summary="Xóa một cuốn sách")
def delete_book(id: str):
    for i, b in enumerate(books_db):
        if b.id == id:
            del books_db[i]
            return
    raise HTTPException(status_code=404, detail="Book not found")
