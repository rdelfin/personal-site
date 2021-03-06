import io
from typing import Any, Dict

from flask import abort, render_template, send_file, Response
from flask_json import json_response

from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError

EXT_MIME_MAP = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "bmp": "image/bmp",
    "gif": "image/gif",
    "png": "image/png",
    "svg": "image/svg+xml",
    "tiff": "image/tiff",
}


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


def delete_image(data: Dict[str, Any]) -> Response:
    if 'name' not in data:
        return json_response(
            ok=False, err="The request does not contain a name field.", status=400
        )
    blob_key = f"imgs/{data['name']}"
    s = _get_storage()
    blob_names = s.list_blobs(blob_key)
    if blob_key not in blob_names:
        return json_response(
            ok=False,
            err=f'The specified image "{blob_key}" does not exist',
            status=404,
        )

    s.delete_blob(blob_key)
    return json_response(ok=True)


def get_request_image(img_name) -> Response:
    blob_key = f"imgs/{img_name}"
    ext = blob_key.split('.')[-1]
    s = _get_storage()

    if ext not in EXT_MIME_MAP:
        abort(404)

    try:
        blob = s.get_blob(blob_key)
    except KeyNotFoundError:
        abort(404)

    return send_file(io.BytesIO(blob), mimetype=EXT_MIME_MAP[ext])


def list_images_template() -> Response:
    s = _get_storage()
    images = s.list_blobs('imgs/')

    return render_template(
        "admin/list_images.html", images=sorted([img.split("/")[-1] for img in images])
    )
