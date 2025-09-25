from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from face_analyzer import brutal_report

app = Flask(__name__)
UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = UPLOAD_FOLDER / filename
            file.save(path)
            report = brutal_report(path)
            return render_template(
                "result.html",
                report=report,
                image=url_for("static", filename=f"uploads/{filename}")
            )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
