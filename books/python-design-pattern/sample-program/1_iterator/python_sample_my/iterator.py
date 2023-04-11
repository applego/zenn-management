from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> object:
        pass


"""
Iteratorを使用すれば不要
代わりに
__iter__
__next__
を実装する
"""
