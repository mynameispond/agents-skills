# Start, Checkpoint, and Complete

## Start

1. Read applicable `AGENTS.md` files, repository documentation, and the
   approved specification, plan, or brief.
2. Confirm the authorization record required by `SKILL.md`, including permission
   for the handoff path. Discover Git facts read-only; do not infer permission
   from those facts or from a request to hurry.
3. Inspect `git status --short`, the current branch, recent commits, and
   `git worktree list`.
4. Refuse direct checkpoint commits on a protected or base branch.
5. Once authorization is complete, copy the handoff template and record the
   approved requirements, permission evidence, Git state, writer, and next one
   to three actions. Keep a brief durable summary alongside plan/approval references.
6. Do not create an empty checkpoint. Wait for a recoverable milestone.

### Late adoption

When work began before skill invocation, remain read-only while discovering
the baseline:

1. Inspect staged, unstaged, untracked, and recent committed changes.
2. Derive task ownership and scope only from repository evidence and explicit
   approval.
3. Treat unexplained or out-of-scope changes as user-owned or external-owned.
4. Stop for ambiguous ownership, branch ancestry, overlap, or scope.
5. After the baseline and checkpoint authorization are explicit, create the
   handoff and use the first coherent milestone as checkpoint 1.

## Checkpoint

Checkpoint an approved specification or plan, confirmed reproduction or
intentional failing test, coherent implementation slice, successful
verification or review, or the state before compaction or a high-risk pause.

1. Inspect `git status --short`, staged, unstaged, and untracked files.
2. Compare every changed path with the approved scope and preserve unrelated
   or external-owned changes.
3. Run fresh verification for the milestone.
4. Update the handoff with decisions, changed paths, exact commands and fresh
   results, checkpoint state, failures, risks, next actions, and the previous
   checkpoint SHA. Record unexpected failures explicitly and use the same
   results and state in the commit trailers.
5. Prune resolved failures, completed actions, raw logs, and obsolete state;
   keep the handoff at or below 500 words.
6. If unrelated staged changes exist, leave the index intact and resolve their
   ownership with the user before checkpointing. Stage explicit approved paths
   with `git add -- <path>` only when the resulting commit stays in scope.
7. Inspect `git diff --cached --check`, `git diff --cached --name-status`, and
   the complete staged diff.
8. Stop for secrets, conflicts, unexplained generated files, out-of-scope
   changes, or an unrecoverable state.
9. Commit without bypassing hooks.
10. Locate the latest reachable commit with the matching `AI-Task` trailer,
    then report its SHA and remaining worktree changes.

Do not write the current commit SHA into that same commit. Resolve it from Git
after commit creation.

Use a descriptive subject and these trailers:

```text
checkpoint(auth): complete token validation

AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

Allowed states:

- `red`: intentional failing test or confirmed reproduction;
- `partial`: coherent recoverable implementation;
- `green`: targeted milestone checks pass;
- `verified`: required final checks and review pass.

Never label an unexpected failure as passing.

## Complete

1. Run fresh targeted and broader checks required by the approved plan.
2. Review scope, security boundaries, tests, documentation, compatibility, and
   unintended changes.
3. Mark the handoff complete with exact checks, skipped checks, failures, and
   residual risks.
4. Create `Checkpoint-State: verified` only when required checks and review
   pass.
5. Report the final state required by `SKILL.md`.
6. Stop before push, merge, rebase, squash, tags, branch deletion, handoff
   deletion, or history cleanup; those require a separate integration task.
