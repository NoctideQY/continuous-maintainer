# Durable State Schema

The files are plain Markdown so a human can edit them and any compatible agent can read them.

## `maintenance-state.md`

This file is required after first-use initialization. Use ISO 8601 timestamps with an explicit timezone. `last_maintenance_at` means the last completed due or explicitly overridden maintenance decision; `last_run_at` means the last time the scheduler invoked the skill, even when the run was skipped because it was not due.

```markdown
# Maintenance State

initialized: true
timezone: Asia/Shanghai
cadence: weekly
automation_provider: codex
automation_id: heartbeat-or-cron-id
automation_status: active
automation_created_at: 2026-09-26T20:15:00+08:00
last_run_at: 2026-09-26T20:00:00+08:00
last_maintenance_at: 2026-09-26T20:15:00+08:00
next_due_at: 2026-10-03T20:15:00+08:00
consecutive_blocked_runs: 0
```

Supported cadence values should be human-readable and unambiguous, for example `daily`, `weekly`, `biweekly`, `monthly`, or an agreed interval such as `every 3 days`. If the cadence is changed, record the change in `decisions.md` and recompute `next_due_at` from the last completed maintenance.

The automation fields identify the scheduler created or reused during initialization. If setup is blocked, use `automation_status: blocked` and add a human-readable `automation_error` field; never claim that a schedule exists when the provider did not confirm it.

## `maintenance-backlog.md`

Every user-reported problem or requested idea goes here before it is implemented. Keep the original wording, add evidence when available, and preserve history.

```markdown
# Maintenance Backlog

## Pending

### B-20260926-01: Short title
- reported_at: 2026-09-26T20:00:00+08:00
- source: developer
- priority: medium
- status: pending
- report: Exact problem or request in the user's words.
- evidence: Reproduction, logs, links, or `not yet verified`.

## In Progress

## Done

## Deferred or Blocked
```

When a scheduled run selects an item, move or copy it to `In Progress` and add the run date. At the end, mark it `Done`, `Deferred`, or `Blocked` with a reason and link to the maintenance log. Never remove a report merely because it is not selected.

## `project-goal.md`

```markdown
# Project Goal

## Final goal
<!-- Who is helped, what problem is solved, and what success looks like. -->

## Non-goals
-

## Constraints
-
```

## `developer-preferences.md`

Record priorities, quality expectations, technology preferences, and things the developer does not want. Do not store credentials.

## `progress.md`

Keep a compact current snapshot:

```markdown
# Progress

## Current focus

## Recently completed

## Blockers

## Next candidates
```

## `decisions.md`

Append dated decisions with the context, decision, alternatives considered, and consequences. Do not rewrite history to make an old choice look inevitable.

## `rejected-ideas.md`

Record ideas that were explicitly declined, why, and what would need to change before reconsidering them.

## `maintenance-log/`

Use one Markdown file per run named `YYYY-MM-DD-short-topic.md`. Include the report fields from `SKILL.md`, the exact verification commands, and the branch or commit if one was created.
