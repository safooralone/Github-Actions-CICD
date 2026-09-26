from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return "GitHub Actions CI/CD demo is running. Visit /api/message or /health.\n"


@app.get("/api/message")
def message():
    return jsonify(message="Deployed automatically from GitHub Actions.")


@app.get("/health")
def health():
    return jsonify(status="ok")
