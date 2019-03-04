from storage.interface import IStorage, KeyNotFoundError
import os

class TmpStorage(IStorage):
    SOURCE_DIR = "/tmp/personal-site-data"

    def __init__(self):
        if not os.path.exists(self.SOURCE_DIR):
            os.makedirs(self.SOURCE_DIR)

    def get_blob(self, key: str) -> bytes:
        try:
            with open(f"{self.SOURCE_DIR}/{key}", "br") as f:
                return f.read()
        except FileNotFoundError:
            raise KeyNotFoundError()

    def put_blob(self, key: str, data: bytes) -> None:
        path = f"/{self.SOURCE_DIR}/{key}"
        folder = "/".join(path.split("/")[:-1])

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(path, "bw") as f:
            f.write(data)

    def delete_blob(self, key: str) -> None:
        try:
            os.remove(f"{self.SOURCE_DIR}/{key}")
        except FileExistsError:
            raise KeyNotFoundError()