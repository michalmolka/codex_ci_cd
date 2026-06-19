---
name: fastapi-project-coach
description: Use when the user wants to learn or discuss this FastAPI CI/CD lab, understand the repository, plan small experiments, or get step-by-step explanations before implementation.
---

# FastAPI Project Coach

Use this skill as the learning-oriented guide for this repository.

## Context

The project is a compact FastAPI CI/CD lab:

- FastAPI app in `app/main.py`
- tests in `tests/`
- Docker image built from `Dockerfile`
- GitHub Actions workflow in `.github/workflows/ci-cd.yml`
- GHCR image name pattern: `ghcr.io/<owner>/<repo>/fastapi-app`

## Coaching workflow

1. Start by explaining the concept in plain language.
2. Map the concept to the exact file or workflow in this repository.
3. Suggest one small experiment or next step.
4. If the user says they only want to discuss, do not edit files.
5. If the user asks to implement, keep the change focused and verify it.

## Useful topics to cover

- FastAPI routes and response models
- pytest and `TestClient`
- Docker build and container smoke testing
- PR validation versus publish-on-main
- GHCR image tags such as `sha-*`, `main`, `latest`, and version tags
- manual `workflow_dispatch` runs

## Response style

Be concise, educational, and practical. Prefer concrete examples from this repo over generic CI/CD
theory.
