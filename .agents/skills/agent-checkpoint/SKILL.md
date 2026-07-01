---
name: agent-checkpoint
description: Use when the user explicitly requests durable Git checkpoints or cross-agent handoff, work resumes after quota exhaustion or a long pause, manual or external changes require reconciliation, or independent write tasks need durable state.
---

# Agent Checkpoint

Preserve recoverable task state in Git. Invocation does not grant edit/commit authority.

## Rules
- **Authorization**: Only edit and commit locally when explicit checkpoint authorization is approved in a plan. Remain read-only otherwise.
- **Safety**: Never push, merge, rebase, reset, tag, delete branches, or bypass hooks.
- **Handoff**: Maintain one handoff per task (under 500 words) using `assets/handoff-template.md` copied to `.ai/handoffs/<task-id>.md`. Update with each checkpoint.

## Route
Read only the reference required for your operation (do not preload unselected references):
- **Start/Checkpoint/Complete**: [checkpoint.md](references/checkpoint.md)
- **Resume**: [resume.md](references/resume.md)
- **Parallel Work**: [parallel.md](references/parallel.md) (plus the operation reference above)

## Report
Upon checkpointing or completion, report:
- Task, branch, worktree, latest checkpoint SHA & state.
- Staged, unstaged, and intentionally uncommitted paths.
- Exact verification outcomes (passed/skipped checks).
- Next actions and required approvals.
