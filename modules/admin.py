from flask import Blueprint, Response, render_template

from utils import auth as app_auth
from utils import blog as blog_utils
from utils import images as image_utils
from utils import tags as tag_utils


bp = Blueprint("admin", __name__)


@bp.route("/")
@app_auth.authenticate
def admin() -> Response:
    return render_template("admin/main.html")


@bp.route("/blog/create", methods=["GET"])
@app_auth.authenticate
def create_blog() -> Response:
    return render_template("admin/create_blog.html")


@bp.route("/blog/edit", methods=["GET"])
@app_auth.authenticate
def edit_blog() -> Response:
    return render_template("admin/edit_blog.html")


@bp.route("/blog/list", methods=["GET"])
@app_auth.authenticate
def delete_blog() -> Response:
    return blog_utils.list_blogs()


@bp.route("/image/upload", methods=["GET"])
@app_auth.authenticate
def upload_image() -> Response:
    return render_template("admin/add_image.html")


@bp.route("/image/list", methods=["GET"])
def list_images() -> Response:
    return image_utils.list_images_template()


@bp.route("/tags/create", methods=["GET"])
@app_auth.authenticate
def create_tag() -> Response:
    return render_template("admin/create_tag.html")


@bp.route("/tags", methods=["GET"])
@app_auth.authenticate
def list_tag() -> Response:
    return tag_utils.list_tag_req()

@bp.route("/tags/edit", methods=["GET"])
@app_auth.authenticate
def edit_tag() -> Response:
    return render_template("admin/edit_tag.html")


@bp.route("/login", methods=["GET"])
def login() -> Response:
    return render_template("admin/login.html")
