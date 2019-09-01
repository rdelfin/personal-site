from flask import Flask, Response, abort, render_template, request, send_file, send_from_directory
from flask_sslify import SSLify
from flask_json import FlaskJSON

from utils import auth as app_auth
from utils import images as image_utils
from modules import admin, api, blog

app = Flask(__name__)
sslify = SSLify(app)
json = FlaskJSON(app)

app.register_blueprint(admin.bp, url_prefix="/admin")
app.register_blueprint(api.bp, url_prefix="/api")
app.register_blueprint(blog.bp, url_prefix="/blog")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/favicon.ico")
def send_favicon():
    return send_file("static/favicon/favicon.ico")


@app.route("/documents/<path:path>")
def send_document(path):
    return send_from_directory("documents", path)


@app.route("/img/<path:path>", methods=["GET"])
def send_image(path):
    return image_utils.get_request_image(path)


@app.route("/")
def index():
    return render_template("home.html")


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


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
