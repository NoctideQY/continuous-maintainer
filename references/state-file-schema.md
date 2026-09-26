# Durable State Schema

The files are plain Markdown so a human can edit them and any compatible agent can read them.

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
