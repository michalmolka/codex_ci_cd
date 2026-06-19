---
name: fastapi-pr-flow
description: Use when working with pull requests for this FastAPI CI/CD lab, including PR summaries, review preparation, changed-file analysis, review comments, merge readiness, and branch-to-main flow.
---

# FastAPI PR Flow

Use this skill for repository pull request work.

## PR model

- Feature branches can have any name.
- Pull requests should target `main`.
- PR events validate the app but do not publish the Docker image.
- After merge, the push to `main` validates again and publishes to GHCR.

## Review workflow

1. Identify the PR, target branch, source branch, author, and status.
2. Read the diff before making claims.
3. Check changed areas:
   - FastAPI behavior
   - tests
   - dependencies
   - Dockerfile or runtime behavior
   - GitHub Actions workflow
4. Check CI status and call out failing jobs before proposing code changes.
5. Separate actionable issues from learning notes.
6. If implementing fixes, keep commits small and aligned to review comments.

## Merge readiness checklist

- PR targets `main`.
- Ruff, tests, dependency audit, Docker build, and smoke test are green.
- Runtime changes have tests.
- Workflow changes are explained in the PR summary.
- Publishing behavior is only expected after merge to `main`, a version tag push, or a manual run
  with publish enabled.

## Summary format

Lead with the current state:

- whether the PR is merge-ready;
- which checks pass or fail;
- what changed;
- what risk remains.
