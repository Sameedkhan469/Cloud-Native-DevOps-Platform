
from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "project": "Cloud-Native DevOps Platform",
        "message": "Application is running successfully!",
        "status": "healthy"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route("/info")
def info():
    return jsonify({
        "application": "DevOps EKS Project",
        "version": "1.0",
        "environment": "development"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
