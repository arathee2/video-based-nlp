import flask
import requests
app = flask.Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    if flask.request.method == "POST":
        return flask.render_template("print-url.html", url=flask.request.form['url'])
    else:
        return flask.render_template("home.html")


if __name__ == "__main__":
    app.run()