from flask import Flask, request, send_file, abort
import os
import datetime

app = Flask(__name__)
BASE_DIR = "/data/files"
TOKEN = os.environ.get("ACCESS_TOKEN", "your_secure_token")
LOG_FILE = "/data/files/download.log"  # 日志保存在挂载目录

def log_download(client_ip, filename, status):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {client_ip} - {filename} - {status}\n")

@app.route("/download")
def download():
    client_ip = request.remote_addr
    filename = request.args.get("file")
    token = request.args.get("token")

    if token != TOKEN:
        log_download(client_ip, filename or "(none)", "403 forbidden - bad token")
        return abort(403)

    if not filename:
        log_download(client_ip, "(none)", "400 bad request - missing file")
        return abort(400)

    # 构造并验证路径合法性
    safe_path = os.path.normpath(os.path.join(BASE_DIR, filename))
    if not safe_path.startswith(BASE_DIR):
        log_download(client_ip, filename, "403 forbidden - invalid path")
        return abort(403)

    if not os.path.isfile(safe_path):
        log_download(client_ip, filename, "404 not found")
        return abort(404)

    log_download(client_ip, filename, "200 OK")
    return send_file(safe_path, as_attachment=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)