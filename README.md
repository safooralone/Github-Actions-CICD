# GitHub Actions CI demo

A small Flask app with a GitHub Actions pipeline. On every push to `main`, the workflow runs the tests, builds a Docker image, and smoke checks it in the GitHub-hosted runner. It does not connect to or deploy to a remote server.

## Run locally

Install Python 3.12 and Docker Desktop, then from this folder run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
docker build -t flask-ci-demo .
docker run --rm -p 8000:8000 flask-ci-demo
```

Open `http://localhost:8000/`, `http://localhost:8000/health`, or `http://localhost:8000/api/message`.

## GitHub Actions

Push the project to a GitHub repository with a `main` branch. Each push runs tests, builds the Docker image, starts it locally in the runner, and checks its health and message endpoints. No deployment secrets or remote server access are required.
