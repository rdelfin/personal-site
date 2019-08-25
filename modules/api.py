from flask import Blueprint, Response, request

import auth as app_auth
import blog_utils


bp = Blueprint("api", __name__)


@bp.route("/admin/blog/create", methods=["POST"])
@app_auth.authenticate
def create_blog_post() -> Response:
    return blog_utils.create_blog(request.get_json())


@bp.route("/admin/blog/delete", methods=["POST"])
@app_auth.authenticate
def delete_blog_post() -> Response:
    return blog_utils.delete_single_blog(request.get_json())


@bp.route("/admin/get_token", methods=["POST"])
def get_token() -> Response:
    return app_auth.get_login_token(request.get_json())
