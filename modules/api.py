from flask import Blueprint, Response, request
from flask_json import json_response

from utils import auth as app_auth
from utils import blog as blog_utils
from utils import images as images_utils
from utils import tags as tag_utils


bp = Blueprint("api", __name__)


@bp.route("/blog/get", methods=["GET"])
def get_blog_post() -> Response:
    return blog_utils.get_blog({"path": request.args.get("path")})


@bp.route("/tags", methods=["GET"])
def get_tags() -> Response:
    return tag_utils.get_tags()


@bp.route("/admin/tags/add", methods=["POST"])
@app_auth.authenticate
def add_tag() -> Response:
    return tag_utils.add_tag_req(request.get_json())


@bp.route("/admin/blog/create", methods=["POST"])
@app_auth.authenticate
def create_blog_post() -> Response:
    return blog_utils.create_blog(request.get_json())


@bp.route("/admin/blog/delete", methods=["POST"])
@app_auth.authenticate
def delete_blog_post() -> Response:
    return blog_utils.delete_single_blog(request.get_json())


@bp.route("/admin/blog/update", methods=["POST"])
@app_auth.authenticate
def update_blog_post() -> Response:
    return blog_utils.update_blog(request.get_json())


@bp.route("/admin/image/add", methods=["POST"])
@app_auth.authenticate
def add_image() -> Response:
    if 'img' not in request.files:
        return json_response(
            ok=False, err="Request does not contain an image", status=400
        )

    return images_utils.add_image(request.files['img'])


@bp.route("/admin/image/delete", methods=["POST"])
@app_auth.authenticate
def delete_image() -> Response:
    return images_utils.delete_image(request.get_json())


@bp.route("/admin/get_token", methods=["POST"])
def get_token() -> Response:
    return app_auth.get_login_token(request.get_json())
