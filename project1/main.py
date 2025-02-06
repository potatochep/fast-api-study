from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/book/{book_name}")
async def read_one_books(book_name: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_name.casefold():
            return book


@app.get("/book-category/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/book-autor/{author}/category/")
async def read_category_by_query(autor: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("category").casefold() == category.casefold()
            and book.get("author") == autor
        ):
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{author}")
async def get_all_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author") == author:
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def create_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.put("/books/delete_book/{book_title}")
async def create_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
