# Parallel Task Isolation

`agent-checkpoint` records parallel task state; it does not initiate parallel
execution. Use the environment's approved worktree workflow before writers
start.

## Isolation

- Use one task ID, branch, worktree, handoff, and writer per write task.
- Keep approvals, scopes, checkpoint numbers, and completion states
  independent.
- Read-only investigations may share a repository when they do not mutate it.
- Never stage paths from another task or worktree.

## Dependency check

Parallelize only when tasks do not share files, schemas, public contracts,
generated artifacts, or mutable state. Serialize shared work or assign one
writer. Do not rely on later conflict resolution as the isolation strategy.

## Late adoption

If parallel work began before skill invocation:

1. Run `git worktree list` and inspect the branch and status in each worktree.
2. Map each approved task to exactly one existing branch and worktree.
3. Treat unexplained changes as user-owned or external-owned.
4. Stop if two writers used one worktree, tasks overlap, or ownership is
   ambiguous.
5. Create and checkpoint each handoff independently after its baseline is
   approved.

If the base advances, report divergence and assess impact. Never merge, rebase,
cherry-pick, or synchronize automatically. Combining task branches is a
separately approved integration task with conflict assessment and combined
verification.
