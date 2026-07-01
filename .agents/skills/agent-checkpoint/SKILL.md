---
name: agent-checkpoint
description: Use when an approved coding task needs durable Git checkpoints, cross-agent handoff, recovery after model quota exhaustion, reconciliation after manual or external changes, or multiple independent agents working in parallel. Creates local commits only when the user-approved proposal explicitly grants checkpoint authorization. Do not use it to bypass approval, integrate branches, rewrite history, or commit unrelated changes.
---

# Agent Checkpoint

Preserve recoverable task state in the repository so another agent can continue without the original conversation.

## Activation

Use this skill when any condition is true:

1. The user invokes `$agent-checkpoint`.
2. An approved implementation will span multiple recoverable milestones.
3. Work may transfer to a different AI agent or provider.
4. Work resumes after quota exhaustion, a long pause, or manual changes.
5. Two or more independent write tasks will run concurrently.

Do not activate for read-only work or as permission to change project state.

## Authorization

Before `start` or `checkpoint`, confirm that the user approved a proposal containing:

- task identifier and goal;
- allowed files or scope;
- task branch and worktree strategy;
- checkpoint milestones;
- test and documentation plans; and
- explicit authorization for local checkpoint commits.

If any item is absent, remain read-only and request the missing approval.

Checkpoint authorization permits scoped edits and local commits only. It does not permit push, merge, rebase, reset, tag creation, branch deletion, history rewriting, hook bypass, dependency installation, production changes, or unrelated staging.

## Handoff File

Copy `assets/handoff-template.md` to `.ai/handoffs/<task-id>.md` in the target repository. Keep one handoff per task. Update and commit it with every checkpoint.

Never store secrets, credentials, private session data, or full raw transcripts in the handoff.

## Operation: Start

1. Read all applicable `AGENTS.md` files and repository documentation.
2. Confirm checkpoint authorization and record its exact scope.
3. Inspect `git status --short`, the current branch, recent commits, and configured worktrees.
4. Refuse to commit directly to a protected or base branch. Use the approved task branch and worktree.
5. Record the base branch, base commit, task branch, worktree, completion criteria, and current writer in the handoff.
6. Record the next one to three concrete actions.
7. Do not create an empty checkpoint. The first checkpoint follows the first recoverable milestone.

## Operation: Checkpoint

Create a checkpoint after an approved specification or plan, a confirmed reproduction or intentionally failing regression test, a coherent implementation slice, successful verification or review, or immediately before compaction or a long high-risk operation.

Before committing:

1. Run `git status --short` and inspect staged, unstaged, and untracked files.
2. Compare every changed path with the approved scope.
3. Preserve and exclude unrelated, user-owned, and external-owned changes.
4. Update the handoff with decisions, changed files, exact verification results, failed attempts, risks, and next actions.
5. Run fresh verification appropriate to the milestone.
6. Stage explicit approved paths with `git add -- <path>`. Do not use broad staging when unrelated changes exist.
7. Inspect `git diff --cached --check`, `git diff --cached --name-status`, and the complete staged diff.
8. Stop if the staged diff contains secrets, unresolved conflicts, unexplained generated files, out-of-scope changes, or an unrecoverable state.
9. Commit without bypassing hooks.
10. Re-run `git status --short` and report any remaining changes.

Use a descriptive subject and these trailers:

```text
checkpoint(auth): complete token validation

AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

Use only these checkpoint states:

- `red`: an intentionally failing test or confirmed reproduction;
- `partial`: a coherent, recoverable implementation milestone;
- `green`: targeted checks for the milestone pass; or
- `verified`: required final checks and review pass.

Never describe an unexpected failing check as passing. Put concise results in the commit trailer and exact commands and outcomes in the handoff.

## Operation: Resume

Remain read-only until reconciliation is complete:

1. Read the task handoff and locate the latest reachable commit whose `AI-Task` trailer matches the task.
2. Record the checkpoint SHA. If it is missing or unreachable, stop and ask the user to establish a new baseline.
3. Inspect:
   - `git log --oneline <checkpoint-sha>..HEAD`;
   - `git diff --name-status <checkpoint-sha>..HEAD`;
   - `git diff --cached --name-status`;
   - `git diff --name-status`;
   - `git status --short`; and
   - branch divergence from the recorded base.
4. Treat every post-checkpoint change as user-owned or external-owned, regardless of Git author.
5. Classify the result:
   - no changes: continue from the handoff;
   - non-overlapping changes: preserve and exclude them, then continue;
   - overlapping changes without material design impact: summarize them and request approval to adopt the current worktree as the new baseline;
   - changed behavior, requirements, design, security, compatibility, or scope: propose a revised plan and obtain approval;
   - missing history, conflicts, or ambiguity: stop and request a baseline decision.
6. After approval of a changed baseline, update the handoff and create a reconciliation checkpoint before continuing.

Do not use checkout, reset, amend, rebase, or file replacement to recreate the old checkpoint.

## Operation: Complete

1. Run fresh targeted and broader verification required by the approved plan.
2. Self-review the diff against scope, security boundaries, tests, documentation, backward compatibility, and unintended changes.
3. Update the handoff status to `complete`, including exact checks, skipped checks, failures, and residual risks.
4. Create a final local checkpoint with `Checkpoint-State: verified` only if required checks and review pass.
5. Report the branch, checkpoint SHA, changed files, verification, documentation, and residual risks.
6. Stop before push, merge, rebase, squash, tag creation, branch deletion, handoff deletion, or history cleanup. These belong to a separately approved integration task.

## Parallel Tasks

- Use one task branch, one worktree, and one handoff per write task.
- Allow one writer at a time in each worktree.
- Keep approvals, scopes, checkpoint numbers, and completion states independent.
- Parallelize only when files and behavioral contracts do not overlap.
- Serialize tasks that share a file, schema, public contract, generated artifact, or mutable shared state.
- If the base advances, report divergence without automatically merging, rebasing, or cherry-picking.

## Stop Conditions

Stop and request user direction when:

- checkpoint authorization is absent or expired;
- the current branch is protected or is the recorded base branch;
- ownership or baseline is ambiguous;
- manual or external changes overlap the task;
- scope, behavior, requirements, security, or compatibility changed;
- conflicts, secrets, out-of-scope files, or unexpected failures are present; or
- the requested action requires integration or history rewriting.

## Completion Report

Report:

- task identifier, branch, worktree, and latest checkpoint SHA;
- checkpoint state and next actions or completion state;
- exact files committed and changes intentionally left uncommitted;
- verification commands, results, failures, and skipped checks;
- documentation updates; and
- remaining risks or required integration approval.
