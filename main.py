import os
import re
from flask import Flask, request, render_template, flash, get_flashed_messages, url_for

app = Flask(__name__)
basepath = "/Users/mayank"

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
        if file.lower().endswith(('.mkv', '.mp4', '.mpeg', '.mov')):
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

    if os.path.isfile(current_path) and current_path.lower().endswith(('.mkv', '.mp4', '.mpeg', '.mov')):
        details = {"page_location": page_location, "base": basepath}
        return render_template("video.html", details=details)
    else:
        flash(f"This is a file {current_path}")
        return render_template("video.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.add_url_rule(f"/{basepath}/<path:filename>", endpoint='css', view_func=app.send_static_file)
    app.run(debug=True, host='0.0.0.0', port=4000)
