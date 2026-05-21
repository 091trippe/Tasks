from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():

    return jsonify({
        "message": "Kubernetes працює 🚀",
        "hostname": socket.gethostname(),
        "time": datetime.datetime.now().isoformat()
    })

@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
