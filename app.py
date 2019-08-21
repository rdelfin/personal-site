from flask import Flask, Response, abort, render_template, send_from_directory
from flask_sslify import SSLify
import blog_utils

app = Flask(__name__)
sslify = SSLify(app)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/documents/<path:path>")
def send_document(path):
    return send_from_directory("documents", path)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/blog")
def blog():
    return blog_utils.respond_blog_list()


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/projects/car")
def car_project():
    return render_template("projects/car.html")


@app.route("/projects/twitcher")
def twitcher_project():
    return render_template("projects/twitcher.html")


@app.route("/blog/post<int:post_num>")
def blog_post(post_num: int) -> Response:
    return blog_utils.respond_blog(post_num)


@app.route("/admin")
def admin() -> Response:
    return render_template("admin/main.html")


@app.route("/admin/blog/create")
def create_blog() -> Response:
    return render_template("admin/create_blog.html")


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
