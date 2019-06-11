import os
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
    

if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
