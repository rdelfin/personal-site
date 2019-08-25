from flask import Blueprint, Response, render_template

import auth as app_auth
import blog_utils


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


@bp.route("/login", methods=["GET"])
def login() -> Response:
    return render_template("admin/login.html")
