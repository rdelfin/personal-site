import boto3
from botocore.exceptions import ClientError
from flask import Response, abort, render_template
from jinja2.exceptions import TemplateNotFound
from thrift import TSerialization

from iface.gen.blog.pb_pb2 import Blog


def respond_blog(number: int) -> Response:
    blog = fetch_aws_blob(number)
    return get_blog_template(blog)


def fetch_aws_blob(number: int) -> Blog:
    s3 = boto3.client("s3")
    try:
        response = s3.get_object(Bucket="personal-site-data", Key=f"blog/{number}.blob")
    except ClientError:
        abort(404)
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        abort(404)

    data = response["Body"].read()
    blog = Blog()
    blog.ParseFromString(blog)
    return blog


def get_blog_template(blog: Blog) -> Response:
    try:
        return render_template("blog_page.html", blog=blog)
    except TemplateNotFound:
        abort(404)
