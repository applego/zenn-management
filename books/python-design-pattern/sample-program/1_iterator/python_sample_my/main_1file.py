from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> object:
        pass


class Aggregate(ABC):
    @abstractmethod
    def iterator(self) -> Iterator:
        pass


class Book:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class BookShelf(Aggregate):
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
        return BookShelfIterator(self)


class BookShelfIterator(Iterator):
    def __init__(self, book_shelf: BookShelf):
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


def main():
    book_shelf = BookShelf(4)
    book_shelf.append_book(Book("Around the World in 80 Days"))
    book_shelf.append_book(Book("Bible"))
    book_shelf.append_book(Book("Cinderella"))
    book_shelf.append_book(Book("Daddy-Long-Legs"))
    it = book_shelf.iterator()
    while it.has_next():
        book = it.next()  # next(it)も可
        print(book.get_name())


if __name__ == "__main__":
    main()
