from flask import Flask, request, send_file, abort
import os
from crypto_utils import encrypt_file

app = Flask(__name__)
BASE_DIR = "/data/files"
TOKEN = os.environ.get("ACCESS_TOKEN", "your_secure_token")

@app.route("/download")
def download():
    filename = request.args.get("file")
    token = request.args.get("token")
    if token != TOKEN:
        return abort(403)

    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(filepath):
        return abort(404)

    encrypted_path = f"/tmp/{filename}.enc"
    encrypt_file(filepath, encrypted_path)
    return send_file(encrypted_path, as_attachment=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)