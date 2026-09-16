---
name: agent-checkpoint
description: Use when the user explicitly requests this skill, durable Git checkpoints, or a checkpoint handoff/resume. A pause, quota exhaustion, or manual changes alone do not activate it.
---

# Agent Checkpoint

Preserve recoverable task state in Git. Invocation grants no write or commit authority.

## Authorization

Implementation approval and checkpoint approval are separate. Without checkpoint approval, keep checkpoint operations read-only; already-approved implementation may continue when ownership and baseline are clear. Resume reconciliation must finish before implementation writes.

Before writing a handoff, staging, or committing a checkpoint, require an approved record covering:

- Task ID, goal, completion criteria, and owned paths including the handoff.
- Approved plan/spec path and revision, or a self-contained approved brief; approval evidence (reference plus a short scope/permission summary).
- Task branch/worktree, base branch/commit, and checkpoint milestones.
- Test plan, documentation plan (or an explicit reason none is needed), and explicit local-commit authorization.

Record these in the [handoff template](assets/handoff-template.md) at `.ai/handoffs/<task-id>.md`, at most 500 words. Verify existing approval instead of asking again; request only missing fields or material scope/design/security/compatibility/ownership/baseline changes. A reference to an inaccessible plan is not a substitute for its approved requirements.

Keep unrelated changes intact. Do not push, merge, rebase, reset, amend, checkout, tag, delete branches, replace files for recovery, or bypass hooks as part of checkpointing. Integration requires separate permission and workflow.

## Route
Read only the reference required for your operation (do not preload unselected references):
- **Start/Checkpoint/Complete**: [checkpoint.md](references/checkpoint.md)
- **Resume**: [resume.md](references/resume.md)
- **Parallel Work**: [parallel.md](references/parallel.md) (plus the operation reference above)

## Report
Merge into the task report: task/branch/worktree, checkpoint SHA/state, remaining staged/unstaged/untracked paths, exact verification outcomes and skipped-check reasons, next actions, and any missing approval. Do not duplicate an existing report.
