import flask
import youtube_dl

app = flask.Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    DEFAULT_URL = "https://youtu.be/9MHYHgh4jYc"
    if flask.request.method == "POST":
        youtube_download(flask.request.form['url'])
        return "<h3> Video downloaded successfully to root directory.</h3>"
    else:
        return flask.render_template("home.html", default_url=DEFAULT_URL)

def youtube_download(url):
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    ydl_opts = {
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook]
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
if __name__ == "__main__":
    app.run()