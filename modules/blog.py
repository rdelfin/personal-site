from flask import Blueprint, Response, render_template

from utils import blog as blog_utils
from utils import tags as tag_utils

bp = Blueprint("blog", __name__)


@bp.route("/", methods=["GET"])
def blog():
    return blog_utils.respond_blog_list()


@bp.route("/post_<post_name>", methods=["GET"])
def blog_post(post_name: str) -> Response:
    return blog_utils.respond_blog(post_name)


@bp.route("/tags", methods=["GET"])
def tags() -> Response:
    tags = tag_utils.list_tags()
    return render_template('blog_tags.html', tags=tags)
