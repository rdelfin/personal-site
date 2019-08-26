from datetime import datetime
from flask import Response, abort, redirect, render_template
from flask_json import json_response
from jinja2.exceptions import TemplateNotFound
import markdown2
import re
import time
from typing import Any, Dict

from iface.gen.blog_pb2 import Blog, HeaderImage
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def respond_blog(name: str) -> Response:
    blog = _fetch_blog(name)
    return _get_blog_template(blog)


def respond_blog_list() -> Response:
    blogs = _fetch_all_blogs()
    return _get_blog_list_template(blogs)


def create_blog(data: Dict[str, Any]) -> Response:
    return _create_blog(
        data["path"],
        data["title"],
        data["header-img"],
        data["header-cap-strong"],
        data["header-cap-rest"],
        data["teaser"],
        data["content"],
    )

def delete_single_blog(data: Dict[str, Any]) -> Response:
    if _delete_single_blog(data["path"]):
        return json_response(ok=True)
    return json_response(ok=False, err=f"Blog {data['path']} was not found.", status=404)


def delete_blog() -> Response:
    blogs = _fetch_all_blogs()
    return _delete_blog_list_template(blogs)


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
            html_content=markdown2.markdown(blog.markdown_content),
            creation_date=f"{datetime.fromtimestamp(blog.creation_time)} UTC",
            modified_date=f"{datetime.fromtimestamp(blog.modification_time)} UTC",
        )
    except TemplateNotFound:
        abort(404)


def _get_blog_list_template(blogs: Dict[str, Blog]) -> Response:
    try:
        return render_template("blog.html", blogs=blogs)
    except TemplateNotFound:
        abort(404)

def _delete_blog_list_template(blogs: Dict[str, Blog]) -> Response:
    try:
        return render_template("admin/delete_blog.html", blogs=blogs)
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
) -> Response:
    storage = StorageFactory.create(StorageType.S3)
    blog_path = f"blogs/{path}.blob"

    if blog_path in storage.list_blobs("blogs"):
        return json_response(
            ok=False, err=f"Blog titled {path} already exists", status=400
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