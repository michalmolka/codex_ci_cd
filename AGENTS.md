# Project Instructions

## Project purpose

This repository is a small learning lab for Codex, FastAPI, Docker, GitHub Actions,
and CI/CD. Keep the project intentionally simple: one FastAPI app, tests, a
Dockerfile, and one workflow that validates the app and publishes a container image.

The application exposes:

- `GET /health`
- `GET /hello/{name}`

## Repository map

- `app/` contains the FastAPI application code.
- `tests/` contains pytest tests for the app.
- `Dockerfile` packages the service.
- `.github/workflows/ci-cd.yml` validates the app and publishes the image.
- `.agents/skills/` contains local Codex skills used to demonstrate repeatable
  PR and CI/CD workflows.
- `docs/` contains article/demo notes about Codex agents, skills, and this lab.
- `requirements.txt` contains runtime dependencies.
- `requirements-dev.txt` contains development and CI dependencies.

## Codex demo model

Use this repo to show three Codex concepts clearly:

- `AGENTS.md` is the always-on project context. It tells Codex how to behave in
  this repository.
- `.agents/skills/check-pr-cicd` is a focused workflow for checking only CI/CD
  evidence on a pull request.
- `.agents/skills/assess-pr-readiness` is a broader workflow for deciding whether
  a pull request appears ready to approve or merge.

Keep these concepts separate in explanations. `AGENTS.md` sets the rules, skills
describe repeatable task workflows, and plugins or automations should be treated
as optional next steps unless the user asks to build them.

## Collaboration rules

- If the user says we are only discussing, do not edit files.
- Before editing files, briefly explain the intended change.
- Prefer small, focused changes that are easy to review in a pull request.
- Preserve user changes in the working tree. Do not revert unrelated edits.
- Keep explanations beginner-friendly when discussing CI/CD, Docker, or GitHub Actions.
- When the user is learning, explain the concept first, then map it to this repo,
  then suggest the smallest useful experiment.
- For Medium/demo material, prefer short sections, concrete examples, and plain
  language over exhaustive platform detail.

## Coding rules

- Follow the current FastAPI style in `app/main.py`.
- Keep endpoint behavior explicit and easy to test.
- Add or update tests when behavior changes.
- Do not introduce new frameworks, services, or large abstractions unless the user asks.
- Keep dependency changes minimal and explain why each new dependency is needed.

## CI/CD model

- Pull requests targeting `main` validate Python code, dependencies, tests, Docker build,
  and the `/health` runtime smoke test.
- Pushes to `main` and version tags run the same validation and publish the Docker image
  to GitHub Container Registry.
- Manual `workflow_dispatch` runs validate by default.
- Manual runs publish only when the `publish_image` input is set to `"true"`.
- The image name is `ghcr.io/<owner>/<repo>/fastapi-app`.

## Skill behavior

- Use `check-pr-cicd` when the user asks only whether CI/CD passed, failed, is
  pending, or is missing for a PR.
- Use `assess-pr-readiness` when the user asks whether a PR is ready to approve
  or merge, or when review comments and diff risk matter.
- Do not mix the two outputs: a CI/CD checklist should not become a merge
  recommendation, and a readiness assessment should include CI/CD as only one
  part of the decision.

## Local validation

Use the same checks that matter in CI when a change touches code, dependencies, Docker,
or workflow behavior:

```bash
ruff check .
ruff format --check .
pytest
docker build -t fastapi-app .
docker run --rm -p 8000:8000 fastapi-app
```

For Docker runtime validation, check:

```bash
curl -fsS http://127.0.0.1:8000/health
```

Run the Docker checks when Docker behavior, runtime behavior, dependencies, or workflow
logic changes. For docs-only changes, Ruff, pytest, and Docker are usually not required.

## Definition of done

A change is ready when:

- relevant tests pass;
- Ruff lint and format checks pass when Python code changes;
- Docker build succeeds when Docker or runtime behavior changes;
- `/health` smoke test passes when runtime behavior changes;
- the final summary says what changed, what was verified, and any remaining risk.
