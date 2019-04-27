from botocore.exceptions import ClientError
from flask import current_app
from storage.interface import IStorage, KeyNotFoundError
from typing import List
import boto3


class S3Storage(IStorage):
    BUCKET = "personal-site-data"

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_KEY"],
        )

    def get_blob(self, key: str) -> bytes:
        try:
            response = self.s3.get_object(Bucket=self.BUCKET, Key=key)
        except ClientError:
            raise KeyNotFoundError()
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise KeyNotFoundError()

        return response["Body"].read()

    def put_blob(self, key: str, data: bytes) -> None:
        self.s3.put_object(Bucket=self.BUCKET, Key=key, Body=data)

    def delete_blob(self, key: str) -> None:
        self.s3.delete_object(Bucket=self.BUCKET, Key=key)

    def list_blobs(self, prefix: str) -> List[str]:
        keys: List[str] = []
        list_obj_kwargs = {"Bucket": self.BUCKET, "Prefix": prefix}

        while True:
            response = self.s3.list_objects_v2(**list_obj_kwargs)

            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise KeyNotFoundError()

            keys += [elem["Key"] for elem in response["Contents"]]

            try:
                list_obj_kwargs["ContinuationToken"] = response["NextContinuationToken"]
            except KeyError:
                break

        return keys
