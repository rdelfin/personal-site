import boto3
from botocore.exceptions import ClientError
from storage.interface import IStorage, KeyNotFoundError

class S3Storage(IStorage):
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_blob(self, key: str) -> bytes:
        try:
            response = self.s3.get_object(Bucket="personal-site-data", Key=key)
        except ClientError:
            raise KeyNotFoundError()
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise KeyNotFoundError()

        return response["Body"].read()

    def put_blob(self, key: str, data: bytes) -> None:
        self.s3.put_object(Bucket="personal-site-data", Key=key, Body=data)

    def delete_blob(self, key: str) -> None:
        self.s3.delete_object(Bucket="personal-site-data", Key=key)
