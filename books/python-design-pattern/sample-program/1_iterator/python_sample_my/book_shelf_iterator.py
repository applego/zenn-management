# from book_shelf import BookShelf
from iterator import Iterator


# def __init__(self, book_shelf: BookShelf):
class BookShelfIterator(Iterator):
    def __init__(self, book_shelf):
        self.book_shelf = book_shelf
        self.index = 0

    # Iteratorインターフェース?のhas_nextメソッドを実装
    def has_next(self) -> bool:
        if self.index < self.book_shelf.get_length():
            return True
        else:
            return False

    # Iteratorインターフェース?のnextメソッドを実装
    def next(self) -> object:
        book = self.book_shelf.get_book_at(self.index)
        self.index += 1
        return book
