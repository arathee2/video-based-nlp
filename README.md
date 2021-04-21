# Video-based NLP

A web application that provides insights about natural language used in a video.

# Quickstart

1. Create S3 bucket. I used my bucket = "audio-from-video-based-nlp". Use your bucket name [here](https://github.com/arathee2/video-based-nlp/blob/e57395c704be5c0013268c53cc9a052ea63aa5e2/app/app.py#L78).
2. Install and configure AWS CLI. More information [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

```bash
$ pip install aws cli
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

3. Run Flask app.

```bash
git clone https://github.com/arathee2/video-based-nlp.git
cd video-based-nlp.git
make
```

4. Go to the URL listed in the app, and follow the instructions on the screen.