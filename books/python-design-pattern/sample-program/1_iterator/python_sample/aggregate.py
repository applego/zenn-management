from abc import ABC, abstractmethod
from iterator import Iterator


class Aggregate(ABC):
    @abstractmethod
    def iterator(self) -> Iterator:
        pass
