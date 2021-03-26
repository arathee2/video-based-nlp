import flask
app = flask.Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    DEFAULT_URL = "https://youtu.be/KE-hrWTgDjk"
    return flask.render_template("home.html", default_url=DEFAULT_URL)

if __name__ == "__main__":
    app.run()