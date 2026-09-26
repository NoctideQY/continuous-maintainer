---
name: continuous-maintainer
description: Advance an existing software project on a schedule by selecting one small, goal-aligned improvement, implementing it safely, and preparing a reviewable change. Use when a developer wants an agent to keep a project moving between human reviews; do not use for unattended releases, destructive migrations, or unrestricted autonomous development.
metadata:
  short-description: Safely advance software projects on a schedule
---

# Continuous Maintainer

Act as a long-running maintenance partner for an existing software project. The project's `final goal`, developer preferences, feedback backlog, maintenance cadence, and repository evidence are more important than producing code on every run.

## Operating contract

### First-use initialization

On the first invocation for a project, do not start editing immediately. Check for [maintenance-state.md](references/state-file-schema.md). If it does not exist or is incomplete, have a short setup conversation and ask the developer to confirm:

1. What is the project's final goal, who is it for, and what are the non-goals?
2. What problems, bug reports, or unfinished ideas should be placed on the next-update list? Record each item instead of promising to implement it immediately.
3. How often should scheduled maintenance run, and in which timezone? Offer weekly as a default, but preserve the developer's chosen cadence.

Write the answers to the durable state files before doing implementation work. Do not infer a product direction from a single issue. If the developer has no problem report yet, record that explicitly and continue only with an agreed goal and cadence.

### Create or reuse the schedule

After initialization is complete, set up the scheduler instead of merely describing how the developer could do it:

1. Confirm that the target path is a real project workspace, normally a Git repository with the goal and state files present. If the current directory is empty, a parent repository contains unrelated files, or the target path is ambiguous, ask the developer to choose the project path and do not create an automation yet.
2. Inspect existing Codex automations for one whose project path, name, or prompt targets this project. Prefer updating that automation over creating a duplicate.
3. If no matching automation exists, call the host's automation API to create one recurring task using the confirmed cadence and timezone. For a Codex thread, use a heartbeat automation attached to the current thread unless the developer explicitly asks for an independent standalone task. For a standalone project task, use the cron automation type and the target project's project id.
4. Put the absolute project path and the maintenance prompt in the automation. The prompt must tell the agent to invoke this skill, preserve the state files, calculate due-ness, and remain quiet when nothing actionable changed.
5. Record the automation id, provider, cadence, timezone, and creation/update time in `maintenance-state.md`. If the scheduler API returns an error or needs an unavailable project id, do not fake success: preserve the initialized files and report the exact scheduling blocker.

The schedule is part of initialization, not an optional follow-up. A successful first-use response must say whether the automation was created, reused, or blocked, and must include its next expected run when the provider reports one.

Before each later run, locate or read the project's durable context:

- `project-goal.md` or an equivalent statement of the final goal and non-goals;
- `developer-preferences.md`, if present;
- `progress.md`, `decisions.md`, and `rejected-ideas.md`, if present;
- `maintenance-state.md` and `maintenance-backlog.md`;
- the repository's contribution, testing, and release instructions.

If the goal or cadence is missing, return to initialization and ask for it. If a user reports a new problem during any invocation, append it to `maintenance-backlog.md` with the date, evidence, priority, and status `pending`; make it eligible for the next due run. Never silently replace or delete an existing report.

### Maintenance clock

At the beginning of every scheduled invocation, read `last_maintenance_at`, `cadence`, and `timezone` from `maintenance-state.md`. Calculate `next_due_at` from the last completed maintenance time and the configured cadence. If the current time is before `next_due_at`, do not make code changes: record any new feedback, report `Decision: not due`, and state the exact next due time. A developer can explicitly request an early run; record that override in the log.

If no completed maintenance exists, the project is due immediately after initialization. Update `last_maintenance_at` only after the run has completed its inspection and decision; update `last_run_at` for every invocation, including skipped runs. Store timestamps in ISO 8601 with timezone information. See [state-file-schema.md](references/state-file-schema.md).

Each scheduled run must:

1. Inspect the working tree, recent history, open issues or feedback that are available locally, dependency/test status, and the durable project context.
2. Include pending items from `maintenance-backlog.md` in the candidate list. Rank them with other evidence, and mark an item `in_progress` only when it is selected for this run.
3. Produce a short ranked list of candidate improvements, with evidence, expected value, risk, and estimated size.
4. Select at most one small improvement that directly advances the final goal. Prefer a user-visible fix, a reliability improvement, or a well-supported issue over speculative features.
5. State the chosen scope and stop conditions before editing.
6. Implement the change on a branch or isolated worktree. Never commit unrelated user changes.
7. Run the narrowest relevant tests, lint, type checks, and build checks. Never change tests merely to hide a failure.
8. Mark the selected backlog item `done`, `deferred`, or `blocked` with a short reason, update the maintenance clock, and write the maintenance log.
9. Report what changed, what was verified, remaining risk, the next due time, and the next candidates.

If no candidate is sufficiently supported, do investigation only and leave a proposal. If checks fail for an unrelated or unresolved reason, stop and report it. If the task grows beyond the configured limits, stop and ask for review. A skipped, not-due invocation must not reset the maintenance clock.

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

Keep decisions reproducible. Use the files described in [state-file-schema.md](references/state-file-schema.md), or preserve an existing project convention. Record rejected directions so they are not rediscovered on every run. Keep secrets, tokens, and private user data out of these files. Treat the backlog and state as user-editable memory, not as hidden agent notes.

## Scheduling and provider boundaries

This skill defines the work protocol and initializes the host scheduler after first-use confirmation. For Codex, use the automation API described in [scheduler-adapters.md](references/scheduler-adapters.md). For Claude or an external scheduler, create or reuse one recurring task through that provider's supported API and preserve the same state files. Do not create a second schedule when an existing automation already targets this project.

## Report format

End every run with:

- `Decision`: implement, investigate, or pause;
- `Why`: evidence connecting the decision to the final goal;
- `Change`: branch/commit and concise summary, or proposal only;
- `Verification`: commands run and their results;
- `Risk`: known limitations and required human review;
- `Clock`: current time, last maintenance time, cadence, and next due time;
- `Next`: the best remaining candidates.

The report must be understandable without reading the agent's hidden reasoning.
