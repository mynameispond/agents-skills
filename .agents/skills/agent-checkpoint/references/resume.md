# Resume and Reconciliation

Remain read-only until reconciliation is complete.

1. Read the handoff, verify the authorization record required by `SKILL.md`, and
   read the recorded approved plan/spec revision or brief. A current file may
   differ from the approved revision. Locate the latest reachable commit whose
   `AI-Task` trailer matches the task. Ask for missing approval/requirements
   before writes; do not reconstruct them from an inaccessible conversation.
2. Stop and request a new baseline if the checkpoint is missing or unreachable.
3. Inspect:

```text
git log --oneline <checkpoint-sha>..HEAD
git diff --name-status <checkpoint-sha>..HEAD
git diff --cached --name-status
git diff --name-status
git status --short
branch divergence from the recorded base
```

4. Inspect relevant diff content as well as path lists to assess overlap and
   behavior; keep secrets out of tool output. Treat every post-checkpoint change
   as user-owned or external-owned, regardless of Git author.
5. Classify the repository state:

| State | Action |
| --- | --- |
| No later changes | Continue from the handoff within existing approval |
| Non-overlapping changes | Preserve and exclude them, then continue |
| Overlap without material design impact | Summarize it and request approval to adopt the current worktree as the new baseline |
| Changed behavior, requirements, design, security, compatibility, or scope | Propose a revision and obtain approval |
| Missing history, conflicts, or ambiguity | Stop and request a baseline decision |

6. After approval of a changed baseline, read and follow the **Checkpoint**
   section in [checkpoint.md](checkpoint.md) to record the reconciliation and
   create its checkpoint before implementation continues. Its verification,
   staging, and staged-diff checks apply in full. Load that reference only when
   a reconciliation checkpoint is needed.

Never use checkout, reset, amend, rebase, or file replacement to recreate the
old checkpoint. Never stage or commit post-checkpoint changes until ownership,
scope, and baseline authorization are explicit.
