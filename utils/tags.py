from typing import Dict, Iterable, Any

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


def add_tags_req(data: Dict[str, Any]) -> Response:
    if 'tags' not in data:
        return json_response(ok=False, err='A "tag" was not provided.', status=400)

    add_tags(data['tags'])
    return json_response(ok=True)

def add_tags(tags: Iterable[str]):
    s = _get_storage()

    try:
        tag_set = set(s.get_blob("tags").decode('utf8').splitlines())
    except KeyNotFoundError:
        tag_set = set()

    for tag in tags:
        tag_set.add(tag)

    tag_list = sorted(list(tag_set))

    s.put_blob('tags', bytes("\n".join(tag_list) + "\n", "utf8"))
