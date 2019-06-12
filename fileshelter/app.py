import os
import shutil
from flask import Flask, redirect, url_for, render_template, send_file, request

app = Flask(__name__)
files_dir = os.path.abspath("./files")

if not os.path.isdir(files_dir):
    os.makedirs(files_dir)

@app.route("/")
def root_view():
    return redirect(url_for("files_list_view"))

@app.route("/files", defaults={"directory": ""})
@app.route("/files/", defaults={"directory": ""})
@app.route("/files/<path:directory>")
def files_list_view(directory):
    return render_template(
        "files.html",
        path=directory,
        files=[
            {
                "name": name,
                "directory": os.path.isdir(
                    os.path.join(files_dir, name))
            }
            for name in os.listdir(os.path.join(files_dir, directory))
        ],
        join=os.path.join,
        normpath=os.path.normpath
    )

@app.route("/internal/download/<path:filepath>")
def download_view(filepath):
    filepath = os.path.abspath(os.path.join(files_dir, filepath))
    if not filepath.startswith(files_dir):
        raise Exception("Can't access this path")
    return send_file(filepath)

@app.route("/internal/upload", defaults={"directory": ""}, methods=["POST"])
@app.route("/internal/upload/", defaults={"directory": ""}, methods=["POST"])
@app.route("/internal/upload/<path:directory>", methods=["POST"])
def upload_view(directory):
    absdir = os.path.abspath(os.path.join(files_dir, directory))
    if not absdir.startswith(files_dir):
        raise Exception("Can't access this path")
    if not os.path.isdir(absdir):
        raise Exception("Directory doesn't exist")
    file = request.files["file"]
    saveto = os.path.abspath(os.path.join(absdir, file.filename))
    if not saveto.startswith(files_dir):
        raise Exception("Can't access " + saveto)
    file.save(saveto)
    return redirect(url_for("files_list_view", directory=directory))

@app.route("/internal/create_directory", methods=["POST"])
def create_directory_view():
    directory = request.form["directory"]
    absdir = os.path.abspath(os.path.join(files_dir, directory))
    if not absdir.startswith(files_dir):
        raise Exception("Can't access this path")
    os.makedirs(absdir)
    return redirect(url_for("files_list_view", directory=directory))

@app.route("/internal/move", methods=["POST"])
def move_file_view():
    directory = request.form["working_directory"]
    source_path = request.form["source_path"]
    source_abspath = os.path.abspath(
        os.path.join(files_dir, directory, source_path)
    )
    if not source_abspath.startswith(files_dir):
        raise Exception("Can't access source filepath")
    if not os.path.isfile(source_abspath):
        raise Exception("Source file doesn't exist")
    destination_path = request.form["destination_path"]
    destination_abspath = os.path.abspath(
        os.path.join(files_dir, directory, destination_path)
    )
    if not destination_abspath.startswith(files_dir):
        raise Exception("Can't access destination filepath")
    shutil.move(source_abspath, destination_abspath)
    return redirect(url_for("files_list_view", directory=directory))


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
