from typing import Dict, Any

from flask import abort, render_template, send_file, Response
from flask_json import json_response

from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def _get_storage():
    return StorageFactory.create(StorageType.S3)


def get_tags() -> Response:
    s = _get_storage()

    try:
        tags = s.get_blob("tags").decode('utf8').splitlines()
    except KeyNotFoundError:
        tags = []

    return json_response(ok=True, tags=tags)


def add_tag_req(data: Dict[str, Any]) -> Response:
    if 'tag' not in data:
        return json_response(ok=False, err='A "tag" was not provided.', status=400)

    add_tag(data['tag'])
    return json_response(ok=True)

def add_tag(tag: str):
    s = _get_storage()

    try:
        tags = s.get_blob("tags").decode('utf8').splitlines()
    except KeyNotFoundError:
        tags = []

    tags.append(tag)
    tags = sorted(tags)

    s.put_blob('tags', bytes("\n".join(tags) + "\n", "utf8"))
