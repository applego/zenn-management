---
title: "Iteratorパターン"
---

## サンプルプログラム 1

### できたクラス図

pyreverse で出力した

![](/images/books/python-design-pattern/classes_0412_1111.png)

本の通りにならん。。。

### Aggregate インターフェース

「集合体」を表す

```python
from abc import ABC, abstractmethod
from iterator import Iterator


class Aggregate(ABC):
    @abstractmethod
    def iterator(self) -> Iterator:
        pass
```

### Iterator インターフェース

要素の数え上げを行う、ループ変数のようなもの

```python
from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> object:
        pass
```

### Book クラス

本を表すクラス

```python
class Book:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
```

### BookShelf クラス

本棚を表すクラス
集合体として扱うために Aggregate インターフェースを実装する

```python
from book import Book
from book_shelf_iterator import BookShelfIterator
from iterator import Iterator
from aggregate import Aggregate


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
```

### BookShelfIterator クラス

BookShelf（本棚）クラスのスキャンを行うクラス

```python
from iterator import Iterator


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
        book = self.book_shelf.get_book_at(self.index)
        self.index += 1
        return book
```

### Main

本棚に本を追加して、本棚の中身を表示する

```python
from book_shelf import BookShelf
from book import Book


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
```

## 練習問題

BookShelf クラスでは、本棚の最大本数を指定しており、それ以上本を追加できませんでしたが、java.util.ArrayList を使って、本棚の最大本数を超えて本を追加できるようにしてください。

この仕様変更で、改修する箇所が BookShelf クラスだけで Main クラスは変更する必要がない。
これが良いところ？
