---
name: assess-pr-readiness
description: Evaluate whether a specific GitHub pull request is ready to approve and merge, needs human review, is not merge-ready, or cannot be assessed. Use when asked to assess PR readiness, approval readiness, merge readiness, CI/check status, review/comment blockers, respond to PR comments, or whether a person should inspect a PR before merge.
---

# Assess PR Readiness

## Overview

Assess one indicated pull request and return a clear merge-readiness recommendation with reasons. When explicitly asked to handle PR comments, reply only to comments where the answer is supported by visible repository, PR, CI, or review context. Do not approve, merge, close, label, resolve threads, or otherwise modify the PR unless the user explicitly asks for that separate action.

This skill is broader than `check-pr-cicd`. It uses CI/CD as one signal, then
adds PR state, review signals, unresolved comments, mergeability, and human
diff risk.

## Inputs

Accept a PR number, PR URL, branch name, or "current PR". Resolve the repository from the explicit user input first, then from the current git remote when needed.

If the target PR is ambiguous, inspect local git context and GitHub metadata before asking the user. Ask only when the repository or PR cannot be determined safely.

## Workflow

1. Read active repository instructions, especially `AGENTS.md`, for the local definition of done, validation expectations, and demo constraints.
2. Fetch PR metadata: title, base, head, draft state, mergeability, changed files, additions/deletions, commits, and diff.
3. Fetch CI/check status for the current head commit. Prefer workflow run conclusions and job names when available.
4. Fetch review signals: submitted reviews, unresolved review threads, requested reviewers, requested team reviewers, and PR comments.
5. Inspect the diff for human-review risk. Focus on behavior changes, tests, workflow/Docker/dependency changes, secrets, debug code, noisy logging, broad refactors, generated files, and anything that conflicts with `AGENTS.md`.
6. If the user asked to respond to PR comments, evaluate each actionable comment using the Comment Response Mode below.
7. Classify the PR using the readiness categories below.
8. Return a concise structured answer with the classification first, then a table that makes the evidence, meaning, and next action clear to a human reader.

## Comment Response Mode

Use this mode only when the user explicitly asks to respond to PR comments, answer review feedback, or handle comments.

For each open or relevant PR comment/review thread:

1. Determine whether the comment is actionable, already resolved by the diff, informational, or unclear.
2. Reply only when the answer is directly supported by visible context such as the PR diff, current files, CI results, prior discussion, repository instructions, or the user's explicit direction.
3. Keep replies short, specific, and grounded in evidence. Mention the file, behavior, test, or CI signal when it helps.
4. Do not invent product intent, reviewer intent, business context, or future commitments.
5. If the right answer is uncertain, do not reply publicly. Add it to the final user-facing summary under `Needs user input before replying`.
6. If a comment requires a code change rather than an explanation, say that in the summary and do not claim it is fixed unless the change was actually implemented and verified.
7. Do not resolve review threads after replying unless the user explicitly asks to resolve them.

Safe replies include:

- explaining what the current diff does when the code clearly shows it;
- pointing to a passing check or test when CI data is visible;
- acknowledging a valid issue and saying it should be fixed before merge;
- saying a requested change has already been made when the current diff proves it.

Unsafe replies that must go to the user summary instead include:

- guesses about why the author made a choice;
- commitments about roadmap, product behavior, or team policy not visible in the repo;
- answers that depend on private context not present in the PR;
- disagreement with a reviewer when evidence is weak or ambiguous.

## Readiness Categories

Use exactly one primary classification:

- `Ready to approve and merge`: PR is open, non-draft, mergeable, CI/checks are green, no unresolved review/comment blockers are visible, and the diff looks intentional and low risk for this small lab.
- `Technically merge-ready, but needs human review`: GitHub/CI gates are green, but the diff has a risk, intent question, or demo/storytelling concern a person should confirm before approval or merge.
- `Not merge-ready`: CI/checks fail or are missing when required, the PR is draft, GitHub reports conflicts or non-mergeable state, requested changes/unresolved threads exist, or the diff clearly violates repo expectations.
- `Blocked / cannot determine`: GitHub, CI, review, or diff data could not be fetched enough to make a reliable call.

## Decision Rules

- Treat a failing required check as `Not merge-ready`.
- Treat an in-progress required check as `Not merge-ready` unless the user asked for a provisional assessment; then state that it is pending.
- Treat no visible CI as `Not merge-ready` when `AGENTS.md` or the repo workflow expects CI validation.
- Treat unresolved requested changes or unresolved review threads as `Not merge-ready`.
- Treat no reviews as a human-process signal, not an automatic blocker, unless branch protection or the user says reviews are required.
- Treat green CI plus suspicious or unclear code as `Technically merge-ready, but needs human review`.
- In this FastAPI CI/CD lab, flag debug-style runtime code such as `print(...)` in request handlers as human-review risk even when CI is green.
- When Docker, dependency, or workflow behavior changes, require evidence that the relevant CI/Docker checks passed before recommending merge.
- Never say "safe to merge" without mentioning residual risk. Prefer "appears ready" or "technically merge-ready" based on observed signals.
- When comment replies were requested, count unresolved or unanswered actionable comments as review risk unless they are clearly non-blocking.
- Keep the recommendation understandable for beginners: name the concrete blocker first, then explain the GitHub or CI/CD term only if needed.

## Output Format

Start with:

```text
Classification: <one category>
Recommendation: <approve/merge, human review first, do not merge, or cannot determine>
```

Then include a Markdown table:

| Area | What was checked | Result | What it means | What to do |
| --- | --- | --- | --- | --- |
| Why | Strongest readiness signals | <short evidence> | <decision impact> | <action or none> |
| CI/checks | Head SHA, workflow runs, job names, required status | <current status> | <whether CI supports merge> | <rerun, wait, fix, or none> |
| Review signals | Reviews, comments, unresolved threads, requested reviewers | <current status> | <whether humans are blocking or still needed> | <request/review/resolve or none> |
| Diff risk | Changed files and risk patterns | <short evidence> | <why a person should or should not inspect> | <smallest code/process action> |
| Next action | Single smallest useful next step | <one action> | <why this is next> | <owner/action wording> |

Keep each cell short and concrete. Prefer plain language over GitHub jargon when explaining "What it means" and "What to do". If a signal is unavailable, write `Not visible` and explain whether that blocks the recommendation.

If comment replies were requested, add a short section after the table:

```markdown
Comment replies:
- Replied: <count and short summary, or "none">
- Not replied: <count and why, or "none">

Needs user input before replying:
- <comment author/thread/file if known>: <what is uncertain and proposed next step>
```

Omit `Needs user input before replying` when every relevant comment was answered confidently or no comment response was requested.

Keep the answer brief. For automation runs, report only new or decision-relevant changes compared with available automation memory.

## Examples

Green CI and clean diff:

```markdown
Classification: Ready to approve and merge
Recommendation: Approve/merge appears reasonable based on current signals.

| Area | What was checked | Result | What it means | What to do |
| --- | --- | --- | --- | --- |
| Why | PR state, mergeability, CI, review blockers, diff | Open, non-draft, mergeable, green CI, no blockers | Current signals support approval and merge with normal residual risk | Approve/merge if this matches the team's process |
| CI/checks | Head SHA and workflow jobs | `abc123`; CI passed | Validation supports merge | No CI action needed |
| Review signals | Reviews, comments, unresolved threads | No blockers visible | No visible human-process blocker | No action unless team requires review |
| Diff risk | Changed files and behavior risk | Small intentional app change | Low human-review risk | No code action needed |
| Next action | Smallest useful step | Approve/merge | PR appears ready | Follow normal merge process |
```

Green CI but debug code:

```markdown
Classification: Technically merge-ready, but needs human review
Recommendation: Have a person confirm or remove debug-style runtime code before approval/merge.

| Area | What was checked | Result | What it means | What to do |
| --- | --- | --- | --- | --- |
| Why | CI, mergeability, and diff risk | Green CI, but request handler contains `print(...)` | GitHub gates pass, but the code may include accidental debug output | Human review first |
| CI/checks | Head SHA and workflow jobs | `abc123`; CI passed | Validation does not block merge | No CI action needed |
| Review signals | Reviews, comments, unresolved threads | No blockers visible | No formal review blocker is visible | Ask a reviewer to confirm intent |
| Diff risk | Runtime code in request path | Debug-style `print(...)` in handler | Could add noisy runtime output | Remove it or document why it is intentional |
| Next action | Smallest useful step | Remove or justify debug code | Clears the main risk | Update PR before approval/merge |
```
