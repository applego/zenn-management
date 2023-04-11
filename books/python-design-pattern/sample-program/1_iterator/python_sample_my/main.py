# from book_shelf import BookShelf
from book_shelf import MyBookShelf
from book import Book


def main():
    book_shelf = MyBookShelf(4)
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
