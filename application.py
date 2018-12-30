from flask import Flask, send_from_directory

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@application.route('/documents/<path:path>')
def send_document(path):
    return send_from_directory('documents', path)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
