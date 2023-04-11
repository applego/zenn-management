from book_shelf import BookShelf
from book import Book


def main():
    book_shelf = BookShelf(4)
    book_shelf.append_book(Book("Around the World in 80 Days"))
    book_shelf.append_book(Book("Bible"))
    book_shelf.append_book(Book("Cinderella"))
    book_shelf.append_book(Book("Daddy-Long-Legs"))
    it = iter(book_shelf)
    while True:
        try:
            book = next(it)  # book = it.__next__()でも可
            print(book.get_name())
        except StopIteration:
            break


if __name__ == "__main__":
    main()
