from flask import Blueprint, Response, render_template

from utils import auth as app_auth
from utils import blog as blog_utils
from utils import images as image_utils


bp = Blueprint("admin", __name__)


@bp.route("/")
@app_auth.authenticate
def admin() -> Response:
    return render_template("admin/main.html")


@bp.route("/blog/create", methods=["GET"])
@app_auth.authenticate
def create_blog() -> Response:
    return render_template("admin/create_blog.html")


@bp.route("/blog/delete", methods=["GET"])
@app_auth.authenticate
def delete_blog() -> Response:
    return blog_utils.delete_blog()


@bp.route("/image/upload", methods=["GET"])
@app_auth.authenticate
def upload_image() -> Response:
    return render_template("admin/add_image.html")


@bp.route("/image/list", methods=["GET"])
def list_images() -> Response:
    return image_utils.list_images_template()


@bp.route("/login", methods=["GET"])
def login() -> Response:
    return render_template("admin/login.html")
