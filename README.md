# FastAPI CI/CD & Codex Agent Lab

A minimal lab demonstrating a containerized FastAPI application with a complete GitHub Actions CI/CD pipeline, paired with OpenAI Codex agent instructions and custom PR skills.

## What This Repository Contains

- **FastAPI Application (`app/`)**: A clean and lightweight Python web service exposing health check (`/health`) and greeting (`/hello/{name}`) endpoints.
- **Automated CI/CD Pipeline (`.github/workflows/ci-cd.yml`)**: GitHub Actions workflow that automatically runs Ruff linting/formatting, Pytest suites, dependency vulnerability audits (`pip-audit`), container build, and runtime smoke testing before publishing images to GitHub Container Registry (GHCR).
- **Docker Packaging (`Dockerfile`)**: Standard containerization configuration for production and local environments.
- **Codex Agent Integration (`AGENTS.md` & `.agents/skills/`)**:
  - `AGENTS.md`: Repository instructions and collaboration rules for AI coding assistants.
  - `check-pr-cicd`: Specialized agent skill for checking and auditing pull request CI/CD pipeline stages.
  - `assess-pr-readiness`: Agent skill to evaluate pull requests for merge readiness and diff risks.

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
