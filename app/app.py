import os
import glob
import flask
import youtube_dl
import boto3

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
    print(f"Names of all files found in {directory} are:\{filenames}")
    
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
        
        print(f"Current working directory when executing app.py: {os.getcwd()}")
        
        # upload all mp3 files to s3
        directory = "./"
        extension = 'mp3'
        filenames = get_filenames(directory, extension)
        print(f"{len(filenames)} MP3 files found:\n{filenames}")
        bucket = 'audio-from-video-based-nlp'
        success = []
        for filename in filenames:
            success.append(upload_file(filename, bucket))
        return f"<h3> {sum(success) / len(success)} videos uploaded successfully to s3 bucket: {bucket}.</h3>"
    else:
        return flask.render_template("home.html", default_url=DEFAULT_URL)

if __name__ == "__main__":
    app.run()