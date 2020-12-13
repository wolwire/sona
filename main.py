import os
import re
from flask import Flask, request, render_template, flash, get_flashed_messages

app = Flask(__name__)
basepath = "/Users/mayank"

def check_directory(path):
    if not(os.path.exists(path)):
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
    dir_names = []
    file_name = []
    page_location = request.args.get("page-location")
    page_location = page_location if page_location else ""
    current_path = get_path(basepath, page_location)

    if not(check_directory(current_path)):
        flash(f"Wrong Directory {current_path}")
        return render_template("files.html")

    if os.path.isfile(current_path):
        flash(f"This is a file {current_path}")
        return render_template("files.html")

    for file in os.listdir(current_path):
        if os.path.isfile(os.path.join(basepath, file)):
            file_name.append(file)
        else:
            dir_names.append(file)

    header = page_location if page_location else 'Home'

    details = {'prev_path': page_location,
               'file_name': file_name,
               'dir_names': dir_names,
               'header': header}

    return render_template("files.html", details=details)



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port=4000)
