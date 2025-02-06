from typing import Optional
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID 는 필수가 아닙니다", default=None)
    title: str = Field(min_length=3, max_length=20)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "새로운 책",
                "author": "hyojin",
                "description": "책설명",
                "rating": "10",
            }
        }
    }


BOOKS = [
    Book(1, "컴퓨터학개론", "hyojin", "Very nicde Book!", 5),
    Book(2, "LLM 마스터", "hyojin", "Very nicde Book!", 2),
    Book(3, "파이썬 마스터", "author1", "Very nicde Book!", 3),
    Book(4, "자바 마스터", "author2", "Very nicde Book!", 5),
    Book(5, "CSS 마스터", "author3", "Very nicde Book!", 4),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/book/{book_id}")
async def read_one_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")


@app.get("/book-rating/{rating}")
async def read_one_book_by_rating(rating: int = Path(gt=0, lt=6)):
    for book in BOOKS:
        if book.rating == rating:
            return book


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):

    # **는 book_request의 key/value를 Book 생성자에 전달
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
