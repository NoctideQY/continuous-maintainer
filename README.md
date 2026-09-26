# Continuous Maintainer

Continuous Maintainer is a Codex/Claude-compatible skill for keeping software projects moving through small, goal-aligned, reviewable changes.

It is designed for projects whose developers still care about the product but no longer have time to drive every iteration manually. The agent reads a project's final goal and durable decisions, inspects repository evidence, chooses at most one bounded improvement per run, verifies it, and reports the result for human review.

## What it does

- turns a project's final goal into a repeatable maintenance loop;
- initializes the project by asking for its final goal, initial problem reports, and preferred cadence;
- prioritizes reproducible bugs, user feedback, reliability, and focused features;
- keeps a durable backlog of developer-reported problems for future runs;
- remembers the last run and last completed maintenance time, so frequent scheduler wake-ups do not cause premature updates;
- preserves project memory in human-readable Markdown files;
- stops before risky changes such as migrations, public API changes, releases, or permission changes;
- works with a recurring Codex thread automation or an external Claude/cron scheduler.

## What it does not do

It does not silently release software, push to the default branch, make unrestricted rewrites, or treat code volume as progress. Every run is intended to end in a reviewable branch, a proposal, or a clear pause.

## Install

Copy the `continuous-maintainer` directory into your Codex skills directory, or invoke it from a checked-out project as `$continuous-maintainer`. The skill itself is provider-neutral; scheduling is configured by the host platform.

## Project setup

On first use, the agent asks for the final goal, any initial problem reports, and the desired maintenance cadence/timezone. It stores these in `project-goal.md`, `maintenance-backlog.md`, and `maintenance-state.md`. You can also add `developer-preferences.md`, `progress.md`, `decisions.md`, and `rejected-ideas.md`. The schemas and scheduler prompt are documented in `references/`.

## License

MIT. See [LICENSE](LICENSE).
