---
name: agent-checkpoint
description: Use when the user explicitly requests durable Git checkpoints or cross-agent handoff, work resumes after quota exhaustion or a long pause, manual or external changes require reconciliation, or independent write tasks need durable state.
---

# Agent Checkpoint

Preserve recoverable task state in Git so another agent can continue without
the original conversation. Invocation does not grant edit or commit authority.

## Authorization

Before any write or commit, confirm an approved proposal identifies the task,
scope, branch or worktree, milestones, tests, documentation, and explicit local
checkpoint-commit authorization. If any item is missing, remain read-only.

Authorization permits scoped edits and local checkpoint commits only. It never
permits push, merge, rebase, reset, tags, branch deletion, history rewriting,
hook bypass, dependency installation, production changes, or unrelated
staging.

## Route

Read only the references required for the requested operation:

| Operation | Required reference |
| --- | --- |
| `start`, `checkpoint`, `complete` | `references/checkpoint.md` |
| `resume` | `references/resume.md` |
| Multiple write tasks | `references/parallel.md` plus the operation reference |

`start` includes late adoption when work began before this skill was invoked.
Read each selected reference completely before acting. Do not preload
unselected references.

## Handoff

Copy `assets/handoff-template.md` to `.ai/handoffs/<task-id>.md`. Keep one
handoff per task, update it with every checkpoint, and keep it at or below 500
words. Store current operational state, not raw logs, full diffs, transcripts,
secrets, credentials, private session data, or hidden reasoning.

## Hard Stops

Stop before writes or commits when authorization is absent or expired; the
branch is protected or is the base; ownership, history, baseline, or scope is
ambiguous; manual or external changes overlap; behavior, requirements, design,
security, or compatibility changed; conflicts, secrets, out-of-scope files, or
unexpected failures exist; or integration or history rewriting is requested.

Never recreate an old state with checkout, reset, amend, rebase, or file
replacement. Treat every post-checkpoint change as user-owned or
external-owned regardless of Git author.

## Common Mistakes

- Treating invocation as approval.
- Preloading every reference instead of following the route.
- Trusting Git authorship to identify manual changes.
- Sharing one worktree between writers or cleaning history during completion.

## Report

Report the task, branch, worktree, latest checkpoint SHA and state, committed
and intentionally uncommitted paths, exact verification outcomes, skipped or
failed checks, documentation, next actions, risks, and required approvals.
