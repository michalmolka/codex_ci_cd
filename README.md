# FastAPI CI/CD

Minimal project showing a Python FastAPI service packaged as a Docker image and built through GitHub Actions.

## Local development

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

Run tests:

```bash
pytest
```

## Docker

Build and run the container locally:

```bash
docker build -t fastapi-app .
docker run --rm -p 8000:8000 fastapi-app
```

## CI/CD

The workflow in `.github/workflows/ci-cd.yml` does two things:

1. Validates the Python app with Ruff, pytest, and pip-audit.
2. Builds the Docker image, starts it, and checks `/health`.
3. Publishes the image to GitHub Container Registry on `push` events.

It runs automatically for pull requests targeting `main`, pushes to `main`, and `v*.*.*` tags.
It can also be started manually from GitHub Actions with `workflow_dispatch`. Manual runs validate
by default; set `publish_image` to `true` when you intentionally want that manual run to publish to
GHCR.

Image name:

```text
ghcr.io/<owner>/<repo>/fastapi-app
```

Typical tags:

- `sha-<commit>`
- `main`
- `latest` for the default branch
- `v1.0.0` style release tags
