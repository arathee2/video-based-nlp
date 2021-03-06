import os
import flask
import youtube_dl
import boto3
from urllib import parse
import hashlib

def hash_filename(url):
    video_id = parse.urlparse(url).query
    return hashlib.sha256(video_id.encode('utf8')).hexdigest()

def get_filenames(directory, extension=None):
    """ 
    Return all filenames in a directory with an arbitrary extension.
    
    Parameters:
    -----------
    directory: A string representing absolute or relative path.
    extension: Extension that you want to look for. E.g. 'mp3'
               Returns all files in current directory if no extension is None
               default=None
    
    Returns:
    --------
    A list with filenames that match the extension in directory.
    
    """
    os.chdir(directory)
    filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
    if extension is not None:
        filenames = [file for file in filenames if file.endswith(f".{extension}")]
    return filenames
    
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

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3 = boto3.client('s3')
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, bucket, object_name)

    return True

app = flask.Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    DEFAULT_URL = "https://youtu.be/9MHYHgh4jYc"
    if flask.request.method == "POST":
        # download mp3 to project root directory i.e. same level as `app`.
        youtube_download(flask.request.form['url'])

        # upload all mp3 files to s3
        MP3_DIRECTORY = "./"
        EXTENSION = 'mp3'
        filename = get_filenames(MP3_DIRECTORY, EXTENSION)[0]
        hashed_filename = hash_filename(flask.request.form['url'])
        BUCKET = 'bucket-for-audio-1234'
        file_uploaded = upload_file(filename, BUCKET, hashed_filename + ".mp3")  # pass filename_hash
        return f"<h3> {int(sum(file_uploaded) / len(file_uploaded))} videos uploaded successfully to s3 bucket: {BUCKET}.</h3>"
    else:
        return flask.render_template("home.html", default_url=DEFAULT_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)