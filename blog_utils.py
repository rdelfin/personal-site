from flask import Response, abort, render_template
from jinja2.exceptions import TemplateNotFound
import re
from thrift import TSerialization
from typing import Dict

from iface.gen.blog_pb2 import Blog
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def respond_blog(number: int) -> Response:
    blog = _fetch_blog(number)
    return _get_blog_template(blog)


def respond_blog_list() -> Response:
    blogs = _fetch_all_blogs()
    return _get_blog_list_template(blogs)


class InvalidBlogKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid blog key found: {key}")


def _fetch_blog(number: int) -> Blog:
    storage = StorageFactory.create(StorageType.S3)
    try:
        data = storage.get_blob(f"blogs/{number}.blob")
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
        return render_template("blog_page.html", blog=blog)
    except TemplateNotFound:
        abort(404)


def _get_blog_list_template(blogs: Dict[str, Blog]) -> Response:
    try:
        return render_template("blog.html", blogs=blogs)
    except TemplateNotFound:
        abort(404)


_key_regex = re.compile("blogs/(\w+)\.blob")


def _blog_number_from_key(key: str) -> str:
    match = _key_regex.search(key)
    if not match:
        raise InvalidBlogKeyError(key)
    return match.group(1)
