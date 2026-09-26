# Scheduler Adapters

The scheduler wakes the agent and delivers the project path; first-use initialization is responsible for creating or reusing that schedule. The skill remains responsible for decisions, edits, verification, and reporting.

The optional read-only helper `scripts/maintenance_due.py <project-path>` can be used by a scheduler before invoking the agent. It reports `due`, `last_maintenance_at`, and `next_due_at`; a missing state file is treated as due so the agent can perform first-use initialization.

## Codex

After the developer confirms the goal and cadence, call the Codex `automation_update` tool. Inspect existing automations first and update a matching one instead of creating a duplicate. Use a heartbeat automation attached to the current thread by default. Use a standalone cron automation only when the developer explicitly wants an independent project task and a valid local project id is available.

The automation prompt should include:

```text
Open the project at <absolute-project-path>. Invoke $continuous-maintainer. On first use, ask the developer to confirm the final goal, any initial problem reports for the next-update backlog, and the desired maintenance cadence/timezone; persist them before editing. On later runs, read maintenance-state.md and maintenance-backlog.md, update last_run_at, and calculate whether the project is due. If it is not due, do not change code and report the exact next_due_at. If it is due, perform at most one goal-aligned, reviewable improvement, update the selected backlog item and maintenance clock, and do not push to the default branch. Report Decision, Why, Change, Verification, Risk, Clock, and Next. Stay quiet when a not-due run is unchanged unless a blocker, failure, new feedback, or human decision is required.
```

Use a heartbeat/thread automation when the work should continue in the same conversation. Use a standalone scheduled task only when the project has its own isolated workspace and review process. Inspect existing automations before creating a new one.

Do not create an automation when the path is not a real project workspace, initialization is incomplete, or the scheduler API cannot resolve the target. Report the blocker and leave the project state files intact so setup can resume.

## Claude or external cron

Run the same prompt through the host's scheduler. Preserve the project path, branch policy, and durable state files between runs. The scheduler must not grant broader credentials than a human would use for the same review workflow.

## Cadence

Weekly is a reasonable default for a small open-source project. Increase frequency only when there is fresh user feedback or an active maintenance window. A schedule is not permission to release changes automatically.
