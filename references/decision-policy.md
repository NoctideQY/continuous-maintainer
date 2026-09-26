# Decision Policy

Use this policy to keep scheduled maintenance useful and bounded.

## Candidate scoring

Rank candidates using:

`value = goal_alignment + user_evidence + reliability_impact - risk - size - uncertainty`

This is a qualitative comparison, not a requirement to invent numeric scores. Evidence can include reproducible bugs, existing tests, user feedback, repeated CI failures, explicit TODOs, or a clear gap in the final goal.

Prefer, in order:

1. A small fix for a reproducible user-facing bug.
2. A reliability, security, or testability improvement with a clear failure mode.
3. A narrowly scoped feature explicitly implied by the final goal.
4. Documentation or developer-experience work that removes a known maintenance bottleneck.

Deprioritize speculative features, broad rewrites, cosmetic changes, and dependency churn.

## Choose a mode

### Implement

Use when the change is small, evidence-backed, reversible, and testable within the run limits. Define an explicit acceptance check before editing.

### Investigate

Use when the opportunity is promising but the problem, design, or expected behavior is unclear. Inspect code and evidence, then write a short proposal with alternatives and a recommended next step. Do not make incidental code changes.

### Pause

Use when the repository is already in a risky state, required checks cannot run, the task needs privileged or irreversible actions, or the same blocker has persisted for two runs. Ask for the smallest missing decision or artifact.

## Human review triggers

Always stop for review before:

- changing a public API or persisted data format;
- migrating or deleting data;
- changing authentication, authorization, billing, or privacy behavior;
- adding a runtime dependency with licensing or supply-chain implications;
- changing deployment, release, signing, or production configuration;
- modifying a test expectation without first demonstrating that the product behavior changed intentionally.
