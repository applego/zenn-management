from book import Book

# from book_shelf import BookShelf
from typing import Iterator


class BookShelfIterator(Iterator):
    # def __init__(self, book_shelf: BookShelf):
    def __init__(self, book_shelf):
        self.book_shelf = book_shelf
        self.index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Book:
        if self.index < self.book_shelf.get_length():
            book = self.book_shelf.get_book_at(self.index)
            self.index += 1
            return book
        else:
            raise StopIteration()
