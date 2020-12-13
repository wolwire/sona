import os
import re
from flask import Flask, request, render_template, flash, get_flashed_messages

app = Flask(__name__)
basepath = "/Users/mayank/"

def check_directory(path):
    if not(os.path.exists(path)):
        return False
    return True


def get_path(basepath, page_location):
    if page_location:
        page_location = page_location.strip(" ,.\"\'")
        path = basepath + page_location
    else:
        path = basepath

    if not(check_directory(path)):
        raise Exception("not a correct path")
    return path

@app.route('/')
def list_directories():
    dir_names = []
    file_name = []
    try:
        page_location = request.args.get("page-location")
        current_path = get_path(basepath, page_location)
        for file in os.listdir(current_path):
            if os.path.isfile(os.path.join(basepath, file)):
                file_name.append(file)
            else:
                dir_names.append(file)

        header = page_location if page_location else 'Home'

        details = {'file_name': file_name,
                   'dir_names': dir_names,
                   'header': header}

        return render_template("files.html", details=details)
    except Exception:
        flash("Something went wrong")
        return render_template("files.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port=4000)
