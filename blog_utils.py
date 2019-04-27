from flask import Response, abort, render_template
from jinja2.exceptions import TemplateNotFound
from thrift import TSerialization

from iface.gen.blog_pb2 import Blog
from storage import StorageFactory, StorageType
from storage.interface import KeyNotFoundError


def respond_blog(number: int) -> Response:
    blog = fetch_blog(number)
    return get_blog_template(blog)


def fetch_blog(number: int) -> Blog:
    storage = StorageFactory.create(StorageType.S3)
    try:
        data = storage.get_blob(f'blogs/{number}.blob')
    except KeyNotFoundError:
        abort(404)

    blog = Blog()
    blog.ParseFromString(data)
    return blog


def get_blog_template(blog: Blog) -> Response:
    try:
        return render_template("blog_page.html", blog=blog)
    except TemplateNotFound:
        abort(404)
