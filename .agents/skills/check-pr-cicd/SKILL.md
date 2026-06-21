---
name: check-pr-cicd
description: Build a CI/CD-only checklist for a specific GitHub pull request. Use when asked to check, summarize, audit, or report the CI/CD stages for an indicated PR, including each pipeline stage/job status and one overall CI/CD status, without reviewing code quality, merge readiness, human reviews, or non-CI PR signals.
---

# Check PR CI/CD

## Overview

Produce a concise CI/CD-only checklist for one indicated GitHub pull request. Focus on workflow runs, jobs, steps, check runs, and publish/deploy gates; do not assess code review status, diff risk, approvals, labels, or mergeability unless needed only to identify the PR head commit.

This skill is intentionally narrow for demo clarity. It answers one question:
are the expected CI/CD stages green, red, pending, missing, or intentionally
skipped for the current PR head commit?

## Inputs

Accept a PR number, PR URL, branch name, or "current PR". Resolve the repository from explicit input first, then from the current git remote when needed.

If the target PR is ambiguous, inspect local git context and GitHub metadata before asking. Ask only when the repository or PR cannot be determined safely.

## Data To Fetch

1. Read active repository instructions and workflow files when available, especially `AGENTS.md` and `.github/workflows/*`, to identify expected CI/CD stages.
2. Fetch the PR metadata needed to identify the current head SHA, source branch, target branch, and PR event context.
3. Fetch CI/check data for the PR head SHA. Prefer GitHub Actions workflow runs and jobs over generic combined status when both are available.
4. Fetch job steps only when they help explain a failure, pending state, or skipped publish gate.
5. For this FastAPI CI/CD lab, map `.github/workflows/ci-cd.yml` as:
   - `Validate Python app`: checkout, Python setup, dependency install, Ruff lint, Ruff format check, pytest, dependency audit.
   - `Validate and publish Docker image`: checkout, Buildx setup, Docker metadata, Docker build, `/health` smoke test, GHCR login gate, image publish gate.
   - Publishing is expected on pushes to `main`, version tags, or manual dispatch with `publish_image == "true"`; it is normally skipped for pull requests.

Use GitHub app tools when available for PR metadata and status. Use `gh` as a fallback for workflow runs, jobs, and logs when app tools do not expose enough CI/CD detail.

## Status Rules

Use these exact status words for individual stages:

- `passed`: completed successfully.
- `failed`: completed with failure, cancelled, timed out, action required, or neutral when the workflow expected a pass/fail validation.
- `pending`: queued, requested, waiting, in progress, or not yet reported for the current head SHA.
- `skipped`: intentionally skipped by workflow conditions, such as publish steps on pull_request events.
- `not visible`: data could not be fetched or the stage/check cannot be found.
- `not applicable`: the stage does not apply to the PR event or repository workflow.

Compute the overall CI/CD status from the current PR head SHA:

- `passed`: every required validation stage passed, and skipped/not applicable stages are expected.
- `failed`: at least one required validation stage failed, was cancelled, timed out, or requires action.
- `pending`: at least one required validation stage is still queued or running and none have failed.
- `missing`: expected CI/CD data is absent for the current head SHA.
- `unknown`: CI/CD data could not be fetched reliably enough to classify.

Treat publish/deploy stages carefully. For pull requests, a skipped publish step is usually expected and should not make the overall status fail. For pushes, tags, or manual publish requests, a skipped or failed publish stage may affect the overall status.

## Workflow

1. Identify the PR and current head SHA.
2. Identify expected CI/CD stages from workflow files and visible GitHub Actions runs.
3. Match visible workflow runs/checks to the current head SHA. Ignore stale runs from older commits unless explaining why data changed.
4. Build a checklist with one row per meaningful CI/CD stage or job. Include key sub-steps only when they clarify a failure, skipped publish gate, or pending state.
5. Explain skipped publish/deploy gates in plain language.
6. Return only CI/CD evidence and next CI/CD action. Do not make a merge recommendation.

## Output Format

Start with:

```text
Overall CI/CD status: <passed|failed|pending|missing|unknown>
PR: <repo>#<number> @ <short head sha>
```

Then include a Markdown checklist:

```markdown
- [x] Validate Python app - passed
  Evidence: <workflow/job/check name and conclusion>
- [ ] Validate and publish Docker image - failed
  Evidence: <workflow/job/check name and conclusion>
  Next CI/CD action: <rerun, inspect logs, fix failing step, or wait>
- [-] Publish Docker image - skipped
  Evidence: skipped on pull_request as expected
```

Use checkbox markers consistently:

- `[x]` for `passed`
- `[ ]` for `failed`, `pending`, `missing`, or `unknown`
- `[-]` for `skipped` or `not applicable`

After the checklist, include a short table only when it adds clarity:

| Stage | Status | Evidence | Meaning | Next CI/CD action |
| --- | --- | --- | --- | --- |

End with one sentence naming the smallest useful CI/CD next step. Keep the answer brief and concrete enough to paste into a PR comment or demo article.

## Guardrails

- Do not inspect or judge code changes except workflow files when needed to understand CI/CD stages.
- Do not include review, approval, label, assignee, or unresolved-thread status.
- Do not say whether the PR is merge-ready; say only whether CI/CD is green, red, pending, missing, or unknown.
- If CI/CD evidence is incomplete, say exactly what was not visible and whether that prevents an overall CI/CD status.
- If a workflow has no Docker, deploy, or publish job, do not invent one.
- Do not include a code review, risk assessment, or approval recommendation. Use `assess-pr-readiness` for that broader question.
