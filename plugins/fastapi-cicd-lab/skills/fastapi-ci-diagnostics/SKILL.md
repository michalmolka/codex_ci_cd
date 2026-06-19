---
name: fastapi-ci-diagnostics
description: Use when diagnosing, explaining, or fixing GitHub Actions CI/CD failures for this FastAPI Docker lab, including lint, format, pytest, pip-audit, Docker build, smoke test, GHCR publish, and manual workflow_dispatch runs.
---

# FastAPI CI Diagnostics

Use this skill when the user asks why CI/CD failed, how a workflow behaves, or how to rerun/publish
the Docker image.

## Workflow map

The workflow is `.github/workflows/ci-cd.yml`.

Expected triggers:

- `pull_request` to `main`: validate only.
- `push` to `main`: validate and publish.
- `push` of `v*.*.*` tags: validate and publish.
- `workflow_dispatch`: validate manually; publish only when `publish_image` is `"true"`.

Expected stages:

1. install Python dependencies;
2. `ruff check .`;
3. `ruff format --check .`;
4. `pytest`;
5. `pip-audit`;
6. Docker build;
7. container smoke test against `/health`;
8. GHCR login and publish when publishing is enabled.

## Diagnostic workflow

1. Identify the failing job and step.
2. Classify the failure as lint, format, test, audit, Docker build, runtime smoke test, permissions,
   or publish/tagging.
3. Explain the failure using the relevant log lines.
4. Propose the smallest fix.
5. If the user wants implementation, change only the needed files.
6. Re-run the matching local check when possible.

## Publishing notes

- PR runs should not publish images.
- Pushes to `main` and version tags should publish.
- Manual runs publish only when the `publish_image` input is set to `"true"`.
- GHCR image path is `ghcr.io/<owner>/<repo>/fastapi-app`.
