from datetime import datetime
from flask import Response, abort, redirect, render_template
from flask_json import json_response
from jinja2.exceptions import TemplateNotFound
import json
import markdown2
import re
import time
from typing import Any, Dict, List

from google.protobuf.json_format import MessageToJson as proto_to_json

from iface.gen.blog_pb2 import Blog, HeaderImage
from utils import tags as tag_utils
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def respond_blog(name: str) -> Response:
    blog = _fetch_blog(name)
    return _get_blog_template(blog)


def respond_blog_list() -> Response:
    blogs = _fetch_all_blogs()
    return _get_blog_list_template(blogs)


def get_blog(data: Dict[str, Any]) -> Response:
    if 'path' not in data:
        return json_response(
            ok=False, err=f'Request does not contain blog path', status=400
        )

    s = StorageFactory.create(StorageType.S3)

    try:
        blob = s.get_blob(f"blogs/{data['path']}.blob")
    except KeyNotFoundError:
        return json_response(
            ok=False, err=f'Blog with path "{data["path"]}" does not exist', status=404
        )
    blog = Blog.FromString(blob)
    dict_blog = json.loads(proto_to_json(blog))
    return json_response(ok=True, path=data["path"], **dict_blog)


def create_blog(data: Dict[str, Any]) -> Response:
    return _create_blog(
        data["path"],
        data["title"],
        data["header-img"],
        data["header-cap-strong"],
        data["header-cap-rest"],
        data["teaser"],
        data["content"],
        data["tags"],
    )

def delete_single_blog(data: Dict[str, Any]) -> Response:
    if _delete_single_blog(data["path"]):
        return json_response(ok=True)
    return json_response(ok=False, err=f"Blog {data['path']} was not found.", status=404)


def update_blog(data: Dict[str, Any]) -> Response:
    data_keys = [
        'path',
        'title',
        'header-img',
        'header-cap-strong',
        'header-cap-rest',
        'teaser',
        'content',
        'tags',
    ]

    if not all(k in data for k in data_keys):
        return json_response(
            ok=False, err="The request to update blog is missing data.", status=400
        )

    s = StorageFactory.create(StorageType.S3)
    path = f"blogs/{data['path']}.blob"
    try:
        blob = s.get_blob(path)
    except KeyNotFoundError:
        return json_response(
            ok=False, err=f"The blog {data['path']} was not found", status=404
        )

    # Make sure all tags already exist
    all_tags = [tag.name for tag in tag_utils.list_tags()]
    if not all(tag in all_tags for tag in data['tags']):
        return json_response(
            ok=False,
            err=f"Some of the tags provided do not already exist.",
            status=400,
        )

    blog = Blog.FromString(blob)
    blog.modification_time = int(time.time())
    blog.name = data['title']
    blog.header_image.path = data['header-img']
    blog.header_image.caption_strong = data['header-cap-strong']
    blog.header_image.caption_cont = data['header-cap-rest']
    blog.teaser = data['teaser']
    blog.markdown_content = data['content']

    for _ in range(len(blog.tags)):
        blog.tags.pop()
    for tag in data['tags']:
        blog.tags.append(tag)

    s.put_blob(path, blog.SerializeToString())
    return json_response(ok=True)

def list_blogs() -> Response:
    blogs = _fetch_all_blogs()
    return _list_blog_template(blogs)


class InvalidBlogKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid blog key found: {key}")


def _fetch_blog(name: str) -> Blog:
    storage = StorageFactory.create(StorageType.S3)
    try:
        data = storage.get_blob(f"blogs/{name}.blob")
    except KeyNotFoundError:
        abort(404)

    blog = Blog()
    blog.ParseFromString(data)
    return blog


def _fetch_all_blogs() -> Dict[str, Blog]:
    storage = StorageFactory.create(StorageType.S3)
    try:
        keys = storage.list_blobs("blogs")
        blog_dict = {
            _blog_number_from_key(key): (Blog(), storage.get_blob(key)) for key in keys
        }
        for key in blog_dict.keys():
            blog_dict[key][0].ParseFromString(blog_dict[key][1])

    except KeyNotFoundError:
        abort(500)

    return {key: tup[0] for key, tup in blog_dict.items()}


def _get_blog_template(blog: Blog) -> Response:
    try:
        return render_template(
            "blog_page.html",
            header_image=blog.header_image,
            blog_title=blog.name,
            html_content=markdown2.markdown(
                blog.markdown_content, extras=["fenced-code-blocks", "tables"]
            ),
            creation_date=f"{datetime.fromtimestamp(blog.creation_time)} UTC",
            modified_date=f"{datetime.fromtimestamp(blog.modification_time)} UTC",
            tags=list(blog.tags),
        )
    except TemplateNotFound:
        abort(404)


def _get_blog_list_template(blogs: Dict[str, Blog]) -> Response:
    try:
        return render_template(
            "blog.html",
            blogs=sorted(
                blogs.items(), reverse=True, key=lambda kv: kv[1].creation_time
            ),
        )
    except TemplateNotFound:
        abort(404)

def _list_blog_template(blogs: Dict[str, Blog]) -> Response:
    try:
        return render_template(
            "admin/list_blogs.html",
            blogs=sorted(blogs.items(), reverse=True, key=lambda t: t[1].creation_time),
        )
    except TemplateNotFound:
        abort(404)


_key_regex = re.compile("blogs/(\w+)\.blob")


def _blog_number_from_key(key: str) -> str:
    match = _key_regex.search(key)
    if not match:
        raise InvalidBlogKeyError(key)
    return match.group(1)


def _create_blog(
    path: str,
    title: str,
    header_img: str,
    header_caption_strong: str,
    header_caption_rest: str,
    teaser: str,
    content: str,
    tags: List[str],
) -> Response:
    storage = StorageFactory.create(StorageType.S3)
    blog_path = f"blogs/{path}.blob"

    if blog_path in storage.list_blobs("blogs"):
        return json_response(
            ok=False, err=f"Blog titled {path} already exists", status=400
        )

    # Make sure all tags already exist
    all_tags = [tag.name for tag in tag_utils.list_tags()]
    if not all(tag in all_tags for tag in tags):
        return json_response(
            ok=False,
            err=f"Some of the tags provided do not already exist.",
            status=400,
        )

    ts = int(time.time())
    blog = Blog(
        name=title,
        header_image=HeaderImage(
            path=header_img,
            caption_strong=header_caption_strong,
            caption_cont=header_caption_rest,
        ),
        teaser=teaser,
        markdown_content=content,
        creation_time=ts,
        modification_time=ts,
        tags=tags,
    )

    blob = blog.SerializeToString()

    storage.put_blob(blog_path, blob)

    return json_response(ok=True)


def _delete_single_blog(path: str) -> bool:
    storage = StorageFactory.create(StorageType.S3)
    full_path = f"blogs/{path}.blob"
    try:
        storage.get_blob(full_path)
    except Exception:
        return False

    storage.delete_blob(full_path)
    return True
