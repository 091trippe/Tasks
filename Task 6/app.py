from flask import Flask
import socket

app = Flask(__name__)

VERSION = "2.0.0"
POD_NAME = socket.gethostname()

@app.route("/")
def hello():

    message = f"Hello from pod {POD_NAME} (version {VERSION})"

    print(f"[{POD_NAME}] Handled request — 200 OK")

    return message + "\n"

@app.route("/health")
def health():

    return "OK\n"

if __name__ == "__main__":

    print(f"Starting python-backend {VERSION} on pod {POD_NAME}")

    app.run(
        host="0.0.0.0",
        port=5000
    )
