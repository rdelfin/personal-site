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

@bp.route("/tag/<tag_name>", methods=["GET"])
def tag(tag_name: str) -> Response:
    tag = tag_utils.get_tag(tag_name)
    if not tag:
        abort(404)
    blogs = blog_utils.get_blogs_with_tag(tag_name)

    return render_template("blog_tag_page.html", tag=tag, blogs=blogs.items())
