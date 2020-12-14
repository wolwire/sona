import os
import re
from flask import Flask, request, render_template, flash, get_flashed_messages, url_for, send_from_directory

app = Flask(__name__, static_folder='static')
basepath = "/Users/mayank"
host = '0.0.0.0'
port = 4000

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

    if os.path.isfile(current_path) and current_path.lower().endswith(('.mkv', '.mp4', '.mpeg', '.mov', '.avi')):
        filename, file_extension = os.path.splitext(current_path)
        details = {"path": f"/videos{page_location}"}
        return render_template("video.html", details=details)
    else:
        flash(f"This is a file {current_path}")
        return render_template("video.html")


@app.route('/videos/<path:page_location>')
def download_file(page_location):
    print(page_location)
    if not page_location:
        flash(f"page-location parameter is required")
        return render_template("base.html")
    return send_from_directory(basepath, page_location, as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host=host, port=port)
