import flask
import requests
app = flask.Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    if flask.request.method == "POST":
        return flask.render_template("print-url.html", url=flask.request.form['default_url'])
    else:
        DEFAULT_URL = "https://youtu.be/KE-hrWTgDjk"
        return flask.render_template("home.html", default_url=DEFAULT_URL)


if __name__ == "__main__":
    app.run()