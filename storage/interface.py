from abc import ABCMeta, abstractmethod
from typing import List


class KeyNotFoundError(Exception):
    pass


class IStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_blob(self, key: str) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def put_blob(self, key: str, data: bytes) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_blob(self, key: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def list_blobs(self, prefix: str) -> List[str]:
        raise NotImplementedError()
