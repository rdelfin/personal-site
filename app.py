from flask import Flask, Response, abort, render_template, request, send_from_directory
from flask_json import FlaskJSON
from flask_sslify import SSLify

import auth
import blog_utils

app = Flask(__name__)
sslify = SSLify(app)
json = FlaskJSON(app)


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


@app.route("/blog/post_<post_name>")
def blog_post(post_name: str) -> Response:
    return blog_utils.respond_blog(post_name)


@app.route("/admin")
@app.authenticate
def admin() -> Response:
    return render_template("admin/main.html")


@app.route("/admin/blog/create", methods=["GET"])
@app.authenticate
def create_blog() -> Response:
    return render_template("admin/create_blog.html")


@app.route("/admin/blog/create", methods=["POST"])
@app.authenticate
def create_blog_post() -> Response:
    return blog_utils.create_blog(request.form)

@app.route("/admin/blog/delete", methods=["GET"])
@app.authenticate
def delete_blog() -> Response:
    return blog_utils.delete_blog()

@app.route("/admin/blog/delete", methods=["POST"])
@app.authenticate
def delete_blog_post() -> Response:
    return blog_utils.delete_single_blog(request.get_json())

@app.route("/admin/login", methods=["GET"])
def login() -> Response:
    return render_template("admin/login.html")

@app.route("/admin/get_token", method=["POST"])
def get_token -> Response:
    return auth.get_login_token(request.get_json())


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
