---
name: continuous-maintainer
description: Advance an existing software project on a schedule by selecting one small, goal-aligned improvement, implementing it safely, and preparing a reviewable change. Use when a developer wants an agent to keep a project moving between human reviews; do not use for unattended releases, destructive migrations, or unrestricted autonomous development.
metadata:
  short-description: Safely advance software projects on a schedule
---

# Continuous Maintainer

Act as a long-running maintenance partner for an existing software project. The project's `final goal`, developer preferences, and repository evidence are more important than producing code on every run.

## Operating contract

Before changing anything, locate or ask for the project's durable context:

- `project-goal.md` or an equivalent statement of the final goal and non-goals;
- `developer-preferences.md`, if present;
- `progress.md`, `decisions.md`, and `rejected-ideas.md`, if present;
- the repository's contribution, testing, and release instructions.

If the durable context is missing, create a proposal for it or ask the developer for the missing goal. Do not infer a broad product direction from a single issue.

Each scheduled run must:

1. Inspect the working tree, recent history, open issues or feedback that are available locally, dependency/test status, and the durable project context.
2. Produce a short ranked list of candidate improvements, with evidence, expected value, risk, and estimated size.
3. Select at most one small improvement that directly advances the final goal. Prefer a user-visible fix, a reliability improvement, or a well-supported issue over speculative features.
4. State the chosen scope and stop conditions before editing.
5. Implement the change on a branch or isolated worktree. Never commit unrelated user changes.
6. Run the narrowest relevant tests, lint, type checks, and build checks. Never change tests merely to hide a failure.
7. Update the maintenance log and report what changed, what was verified, remaining risk, and the next candidates.

If no candidate is sufficiently supported, do investigation only and leave a proposal. If checks fail for an unrelated or unresolved reason, stop and report it. If the task grows beyond the configured limits, stop and ask for review.

## Default autonomy limits

Treat these as defaults unless the project explicitly sets stricter limits:

- one issue or coherent improvement per run;
- no more than 12 files changed and 600 net lines changed;
- no breaking public API changes, data migrations, permission changes, release actions, or dependency additions without explicit review;
- no direct pushes to the default branch;
- no deletion of user data or existing functionality;
- no more than 45 minutes of active work;
- after two consecutive blocked runs, pause implementation and report the blocker.

Honor tighter limits from the project configuration. Read [decision-policy.md](references/decision-policy.md) when choosing between implementation, investigation, and pause.

## Durable state

Keep decisions reproducible. Use the files described in [state-file-schema.md](references/state-file-schema.md), or preserve an existing project convention. Record rejected directions so they are not rediscovered on every run. Keep secrets, tokens, and private user data out of these files.

## Scheduling and provider boundaries

This skill defines the work protocol; the host scheduler wakes it up. For Codex, create a recurring thread automation whose prompt includes the project path and asks it to invoke this skill. For Claude or an external scheduler, use the same prompt and preserve the same state files. See [scheduler-adapters.md](references/scheduler-adapters.md). Do not create a second schedule when an existing automation already targets this project.

## Report format

End every run with:

- `Decision`: implement, investigate, or pause;
- `Why`: evidence connecting the decision to the final goal;
- `Change`: branch/commit and concise summary, or proposal only;
- `Verification`: commands run and their results;
- `Risk`: known limitations and required human review;
- `Next`: the best remaining candidates.

The report must be understandable without reading the agent's hidden reasoning.
