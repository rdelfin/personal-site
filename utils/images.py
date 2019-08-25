from storage import StorageFactory, StorageType
from flask_json import json_response


def _get_storage():
    return StorageFactory.create(StorageType.S3)


def add_image(img_file):
    blob_key = f"imgs/{img_file.filename}"
    img_data = img_file.read()
    s = _get_storage()

    if blob_key in s.list_blobs("imgs/"):
        return json_response(
            ok=False, err=f'Image with name "{blob_key}" already exists.', status=400
        )

    s.put_blob(blob_key, img_data)
    return json_response(ok=True)
