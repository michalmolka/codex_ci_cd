# Project Instructions

## Project purpose

This repository is a learning lab for Codex, FastAPI, Docker, GitHub Actions, and CI/CD.
The app is intentionally small: a FastAPI service with `/health` and `/hello/{name}`, tests,
a Dockerfile, and a workflow that validates the app and publishes a container image.

## Collaboration rules

- If the user says we are only discussing, do not edit files.
- Before editing files, explain the intended change briefly.
- Prefer small, focused changes that are easy to review in a pull request.
- Preserve user changes in the working tree. Do not revert unrelated edits.
- Explain CI/CD behavior in plain language when the user is learning a concept.

## Local validation

Use the same checks that matter in CI when a change touches code, dependencies, Docker, or workflow
behavior:

```bash
ruff check .
ruff format --check .
pytest
docker build -t fastapi-app .
docker run --rm -p 8000:8000 fastapi-app
```

For Docker validation, check:

```bash
curl -fsS http://127.0.0.1:8000/health
```

## CI/CD model

- Pull requests targeting `main` validate the app, dependencies, tests, Docker build, and `/health`.
- Pushes to `main` and version tags run the same validation and publish the Docker image to GHCR.
- Manual `workflow_dispatch` runs are allowed. They validate by default and can publish only when
  the `publish_image` input is set to `"true"`.
- The image name is `ghcr.io/<owner>/<repo>/fastapi-app`.

## Definition of done

A change is ready when:

- tests pass;
- Ruff lint and format checks pass;
- Docker build succeeds when Docker behavior is touched;
- `/health` smoke test passes when runtime behavior is touched;
- the final summary says what changed, what was verified, and any remaining risk.

## Preferred learning flow

When the user is exploring, favor this order:

1. Explain the concept.
2. Show how it maps to this repository.
3. Suggest the smallest useful experiment.
4. Implement only after the user confirms or asks to proceed.
