from book import Book
from book_shelf_iterator import MyBookShelfIterator
from iterator import Iterator
from aggregate import Aggregate


class MyBookShelf(Aggregate):
    def __init__(self, maxsize: int):
        self.books = [None] * maxsize
        self.last = 0

    def get_book_at(self, index: int) -> Book:
        return self.books[index]

    def append_book(self, book: Book) -> None:
        self.books[self.last] = book
        self.last += 1

    def get_length(self) -> int:
        return self.last

    # Aggregate インターフェース?のiteratorメソッドを実装
    def iterator(self) -> Iterator:
        return MyBookShelfIterator(self)
