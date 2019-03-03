from flask import Flask, Response, abort, render_template, send_from_directory
import blog_utils

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@application.route("/documents/<path:path>")
def send_document(path):
    return send_from_directory("documents", path)


@application.route("/")
def index():
    return render_template("home.html")


@application.route("/blog")
def blog():
    return render_template("blog.html")


@application.route("/contact")
def contact():
    return render_template("contact.html")


@application.route("/projects")
def projects():
    return render_template("projects.html")


@application.route("/projects/car")
def car_project():
    return render_template("projects/car.html")


@application.route("/projects/twitcher")
def twitcher_project():
    return render_template("projects/twitcher.html")


@application.route("/blog/post<int:post_num>")
def blog_post(post_num: int) -> Response:
    return blog_utils.respond_blog(post_num)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
