import os
import re
from flask import Flask, request, render_template, flash, get_flashed_messages, url_for, send_from_directory
import ffmpeg
import json

with open('config.local.json') as config_file:
    config_data = json.load(config_file)

basepath = config_data['basepath']
host = config_data['host']
port = config_data['port']

app = Flask(__name__, static_folder='static')


def check_directory(path):
    if not(os.path.exists(path)) and re.match(f"^{basepath}", path):
        return False
    return True


def get_path(basepath, page_location):
    if page_location:
        page_location = page_location.strip("\"\'")
        path = basepath + page_location
    else:
        path = basepath
    return path


@app.route('/')
def list_directories():
    file_details = []
    page_location = request.args.get("page-location")
    page_location = page_location if page_location else ""
    current_path = get_path(basepath, page_location)

    if not(check_directory(current_path)):
        flash(f"Wrong Directory")
        return render_template("files.html")

    if os.path.isfile(current_path):
        flash(f"This is a file {current_path}")
        return render_template("files.html")

    for file in os.listdir(current_path):
        if file.lower().endswith(('.mkv', '.mp4', '.mpeg', '.mov', '.avi')):
            details = {"name": file, "path": f"/play?page-location={page_location}/{file}"}
        else:
            details = {"name": file, "path": f"/?page-location={page_location}/{file}"}
        file_details.append(details)

    header = page_location if page_location else 'Home'

    details = {'file_details': file_details,
               'header': header}

    return render_template("files.html", details=details)


@app.route('/play')
def play_videos():
    page_location = request.args.get("page-location")
    page_location = page_location if page_location else ""
    current_path = get_path(basepath, page_location)

    if os.path.isfile(current_path) and current_path.lower().endswith(('.mp4','.mov')):
        details = {"path": f"/videos{page_location}", "type": "video/mp4"}
        return render_template("video.html", details=details)
    elif os.path.isfile(current_path) and current_path.lower().endswith(('.avi')):
        details = {"path": f"/videos{page_location}", "type": "video/avi"}
        return render_template("video.html", details=details)
    elif os.path.isfile(current_path) and current_path.lower().endswith(('.mkv')):
        details = {"path": f"/videos{page_location}", "type": "video/x-matroska; codecs='theora, vorbis'"}
        return render_template("video.html", details=details)
    else:
        flash(f"This is a file {current_path}")
        return render_template("video.html")


@app.route('/videos/<path:page_location>')
def download_file(page_location):
    if not page_location:
        flash(f"page-location parameter is required")
        return render_template("base.html")

    current_path = get_path(basepath, page_location)
    filename, file_extension = os.path.splitext(current_path)
    # stream = ffmpeg.input(current_path)
    # stream = ffmpeg.output(stream, f'{filename}.mp4')
    # ffmpeg.run(stream)
    return send_from_directory(basepath, page_location, as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host=host, port=port)
