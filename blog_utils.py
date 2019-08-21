from flask import Response, abort, redirect, render_template
from jinja2.exceptions import TemplateNotFound
import re
import time
from typing import Dict

from iface.gen.blog_pb2 import Blog, HeaderImage
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def respond_blog(number: int) -> Response:
    blog = _fetch_blog(number)
    return _get_blog_template(blog)


def respond_blog_list() -> Response:
    blogs = _fetch_all_blogs()
    return _get_blog_list_template(blogs)


def create_blog(form) -> Response:
    return _create_blog(
        form["path"],
        form["title"],
        form["header-img"],
        form["header-cap-strong"],
        form["header-cap-rest"],
        form["teaser"],
        form["content"],
    )


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

    storage.put_blob(f"blogs/{path}", blob)

    return redirect("/admin")
