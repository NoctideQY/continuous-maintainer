# Scheduler Adapters

The scheduler is responsible only for waking the agent and delivering the project path. The skill remains responsible for decisions, edits, verification, and reporting.

## Codex

Create one recurring thread automation for the project. Its prompt should include:

```text
Open the project at <absolute-project-path>. Invoke $continuous-maintainer. Read the project's durable state and repository instructions. Perform at most one goal-aligned, reviewable improvement. Do not push to the default branch. Report Decision, Why, Change, Verification, Risk, and Next. Stay quiet when a run is unchanged unless a blocker, failure, or human decision is required.
```

Use a heartbeat/thread automation when the work should continue in the same conversation. Use a standalone scheduled task only when the project has its own isolated workspace and review process. Inspect existing automations before creating a new one.

## Claude or external cron

Run the same prompt through the host's scheduler. Preserve the project path, branch policy, and durable state files between runs. The scheduler must not grant broader credentials than a human would use for the same review workflow.

## Cadence

Weekly is a reasonable default for a small open-source project. Increase frequency only when there is fresh user feedback or an active maintenance window. A schedule is not permission to release changes automatically.
