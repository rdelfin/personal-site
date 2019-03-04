from enum import Enum

from storage.interface import IStorage
from storage.s3 import S3Storage
from storage.tmp import TmpStorage


class StorageType(Enum):
    S3 = 1
    TMP = 2

class StorageFactory:
    @staticmethod
    def create(type: StorageType) -> IStorage:
        if type == StorageType.S3:
            return S3Storage()
        elif type == StorageType.TMP:
            return TmpStorage()

        raise ValueError()