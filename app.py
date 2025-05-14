from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)
BASE_DIR = "/data/files"
TOKEN = os.environ.get("ACCESS_TOKEN", "your_secure_token")

@app.route("/download")
def download():
    filename = request.args.get("file")
    token = request.args.get("token")
    if token != TOKEN:
        return abort(403)

    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        return abort(404)

    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)