import json
from typing import Dict, Iterable, Any

from flask import abort, render_template, send_file, Response
from flask_json import json_response
from google.protobuf.json_format import MessageToJson as ProtoBufToJson

from iface.gen.blog_pb2 import Tag
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def _get_storage():
    return StorageFactory.create(StorageType.S3)


def get_tags() -> Response:
    s = _get_storage()

    tag_list = s.list_blobs("tags/")

    tags = [Tag.FromString(s.get_blob(tag_path)) for tag_path in tag_list]

    return json_response(
        ok=True, tags={tag.name: json.loads(ProtoBufToJson(tag)) for tag in tags}
    )


def add_tag_req(data: Dict[str, Any]) -> Response:
    fields = ['name', 'image_path', 'description']

    if not all(field in data.keys() for field in fields):
        return json_response(
            ok=False,
            err='Not all required fields were provided in the request. (should '
            f'contain {", ".join(fields)}',
            status=400
        )

    add_tags(data['name'], data['image_path'], data['description'])
    return json_response(ok=True)

def add_tags(name: str, image_path: str, description: str):
    s = _get_storage()
    tag = Tag(name=name, image_path=image_path, description=description)
    s.put_blob(f'tags/{name}.blob', tag.SerializeToString())


def delete_tag_req(data: Dict[str, Any]) -> Response:
    if "name" not in data:
        return json_response(
            ok=False, err='The request does not contain a "name" field.', status=400
        )

    tag_key = f'tags/{data["name"]}.blob'
    s = _get_storage()
    tag_keys = s.list_blobs(tag_key)
    if not any(key == tag_key for key in tag_keys):
        return json_response(
            ok=False, err='The tag name specified does not exist.', status=404
        )

    s.delete_blob(tag_key)
    return json_response(ok=True)
