# Agent Checkpoint Design

Status: approved for specification on 2026-07-01

## Problem

Coding-agent quotas can expire while a task is in progress. A different agent
cannot reliably consume the original agent's conversation context, and all
agents may be unavailable long enough for a user to make additional manual
changes before agent work resumes.

The repository needs a provider-neutral checkpoint workflow that:

- preserves a recoverable code state in Git;
- records enough task context for another agent to continue;
- respects the existing approval gate;
- protects manual or external changes made after a checkpoint; and
- supports multiple independent tasks running concurrently.

## Goals

- Keep the source of truth in the repository and local Git history.
- Allow local checkpoint commits after the user approves a task plan that
  explicitly includes checkpoint authorization.
- Let a new agent reconcile current repository state against the last
  checkpoint before writing files.
- Isolate parallel write tasks by task branch and worktree.
- Keep the workflow usable by agents that can read `AGENTS.md` and
  `.agents/skills`, with documented manual instructions for other agents.
- Avoid dependencies, global configuration changes, and provider-specific
  runtime requirements in the first version.

## Non-goals

- Sharing or translating complete provider conversation transcripts.
- Automatically pushing, merging, rebasing, resetting, tagging, or deleting
  branches.
- Allowing multiple writers in the same working tree.
- Adding Codex or Claude hooks.
- Adding `CLAUDE.md`, a Claude-specific skill wrapper, or global skills and
  configuration.
- Building an MCP memory service or an agent orchestrator.

## Repository Components

Implementation will be limited to this repository:

- `AGENTS.md` will define checkpoint authorization, reconciliation, task
  isolation, and safety boundaries.
- `.agents/skills/agent-checkpoint/SKILL.md` will define the reusable `start`,
  `checkpoint`, `resume`, and `complete` workflow.
- `.agents/skills/agent-checkpoint/assets/handoff-template.md` will provide the
  provider-neutral handoff format.
- `.agents/skills/agent-checkpoint/agents/openai.yaml` may provide Codex UI
  metadata while keeping the workflow itself provider-neutral.
- `README.md` will document setup and usage, including the explicit prompt
  needed for Claude Code to read `AGENTS.md` and the canonical skill because
  no Claude-specific wrapper will be added.

The first version will be instruction-only. It will not add scripts,
dependencies, hooks, or global files.

## Authorization Model

Before changing project state, the agent must present the diagnosis or design,
implementation approach, affected scope, impact analysis, test plan,
documentation plan, and checkpoint strategy. The checkpoint strategy must name
the task, task branch or worktree, allowed scope, and expected checkpoints.

Explicit approval of that proposal authorizes the agent to:

- edit files within the approved task scope; and
- create local checkpoint commits for that task without requesting approval
  before each individual commit.

The authorization does not permit the agent to:

- commit directly to a protected or base branch;
- stage or commit unrelated user or external changes;
- expand the approved task scope;
- push, merge, rebase, reset, tag, delete branches, or rewrite history; or
- bypass repository hooks or verification.

Authorization ends when the task completes, the user revokes it, or a material
scope, requirement, design, security-boundary, or compatibility change occurs.
Only the affected task must pause when parallel tasks have separate approvals.

Superpowers workflows may create their required local specification, plan, and
implementation commits after the applicable approval grants checkpoint
authorization. Repository instructions remain authoritative when a workflow's
default commit behavior conflicts with this policy.

## Checkpoint Lifecycle

### Start

The agent will:

1. assign a stable task identifier;
2. confirm the approved scope and completion criteria;
3. record the base branch and base commit;
4. use a dedicated task branch and, for concurrent write tasks, a dedicated
   worktree; and
5. create `.ai/handoffs/<task-id>.md` from the handoff template.

### Checkpoint

A checkpoint is created after a meaningful, recoverable milestone rather than
after every tool call. Expected milestones include:

- an approved specification or implementation plan;
- a confirmed reproduction, root cause, or intentionally failing regression
  test;
- a coherent implementation slice;
- successful targeted verification or review; and
- a point immediately before compaction or a long, high-risk operation.

Before committing, the agent will:

1. inspect the working tree, staged changes, and untracked files;
2. exclude all unrelated or external-owned changes;
3. update the task handoff with decisions, current state, affected files,
   verification results, failed attempts, risks, and next actions;
4. run fresh verification appropriate to the checkpoint;
5. inspect the exact staged diff for scope, secrets, conflicts, and accidental
   files; and
6. create a local commit without bypassing hooks.

A checkpoint may represent an intentionally failing or partial state only when
the state is recoverable and accurately documented. It must not contain merge
conflicts, credentials, unexplained generated output, or a state that cannot be
safely resumed.

### Commit Metadata

Checkpoint commits will use a descriptive subject and machine-readable
trailers:

```text
checkpoint(auth): complete token validation

AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

`Checkpoint-State` will use a small documented vocabulary such as `red`,
`partial`, `green`, or `verified`. Validation must report failures and skipped
checks accurately rather than implying a passing state.

### Complete

The final task checkpoint will mark the handoff as complete and record fresh
verification and residual risks. It does not authorize integration. Squashing,
rebasing, merging, pushing, deleting the handoff, or cleaning checkpoint
history belongs to a separately approved integration phase.

## Handoff Record

Each task will use its own `.ai/handoffs/<task-id>.md`. The record will contain:

- task identifier, goal, and completion criteria;
- approved scope and constraints;
- base branch, base commit, task branch, and worktree;
- latest known checkpoint and state;
- decisions and assumptions;
- changed files and current implementation state;
- commands run and exact verification outcomes;
- failed attempts and conclusions;
- blockers, risks, and unverified behavior;
- next one to three actions; and
- last update time and current writer.

The handoff is committed with each checkpoint so it is available to another
agent from repository history. It must not contain secrets, credentials,
private session data, or complete raw transcripts.

## Resume Reconciliation

Every resumed or transferred task must begin with read-only reconciliation
before the agent edits files.

The agent will:

1. find the latest reachable checkpoint for the task from commit trailers and
   the handoff;
2. inspect commits between that checkpoint and `HEAD`;
3. inspect staged, unstaged, and untracked changes;
4. inspect branch and base divergence; and
5. compare affected paths and behavior with the approved scope.

All changes after the checkpoint are treated as user-owned or external-owned.
The agent will not infer ownership from the Git author.

Reconciliation outcomes are:

- **No changes:** continue from the recorded next action.
- **Non-overlapping changes:** preserve and exclude them from checkpoint
  commits, then continue within the existing approval.
- **Overlapping changes without a material design change:** summarize the
  overlap and request approval to adopt the current worktree as the new
  baseline before writing.
- **Behavior, requirement, design, security, or compatibility change:** stop
  and propose a revised plan; the previous authorization no longer covers the
  affected scope.
- **Missing checkpoint, rewritten history, conflicts, or ambiguous baseline:**
  stop and request a new baseline decision.

After the user approves a changed baseline, the agent will update the handoff
and create a reconciliation checkpoint before continuing implementation.

The agent must not use reset, checkout, amend, rebase, or file replacement to
make the current worktree resemble the old checkpoint.

## Parallel Task Model

Parallel write work is supported only with isolation:

```text
Task A -> worktree/auth    -> branch task/auth
       -> .ai/handoffs/auth.md

Task B -> worktree/billing -> branch task/billing
       -> .ai/handoffs/billing.md
```

Each task has independent approval, scope, base commit, branch, worktree,
handoff, checkpoint sequence, and writer. A combined proposal may request
approval for several tasks, but each task remains independently bounded.

Parallel tasks are allowed when their owned paths and behavioral contracts do
not overlap. Tasks that edit the same files, schema, public contract, generated
artifact, or shared state must be serialized or assigned a single writer.
Read-only investigation may run concurrently without a write worktree.

If the base branch advances while tasks are active, each task detects and
reports divergence. It must not automatically merge, rebase, or cherry-pick the
new base. Integration is a separate task with its own approval, conflict
assessment, and combined verification.

## Failure and Safety Handling

- A quota failure before the next checkpoint leaves the working diff intact.
  The next agent reconciles `HEAD`, the last handoff, and the current working
  tree.
- Unrelated dirty files are preserved and excluded from staging.
- Expected failing tests may be checkpointed only when their purpose and exact
  result are recorded.
- Unexpected failures, conflicts, secret detection, or ambiguous ownership
  block the checkpoint.
- A stale or unavailable agent does not transfer write ownership
  automatically. The replacement agent performs reconciliation before taking
  ownership.
- No checkpoint workflow may weaken authentication, authorization, validation,
  secret handling, or other existing safety boundaries.

## Skill Operations

The skill will expose four conceptual operations:

- `start`: validate approval and isolation, initialize the task handoff, and
  establish the baseline.
- `checkpoint`: verify scope and state, update the handoff, stage only approved
  changes, and create a local checkpoint commit.
- `resume`: perform reconciliation and either continue safely or stop for a
  baseline or plan decision.
- `complete`: run final verification, record completion state, and hand off to
  the separately approved integration workflow.

The skill description will trigger on checkpoint, handoff, quota exhaustion,
cross-agent continuation, task resumption, and parallel-agent work. Agents
without automatic `.agents/skills` discovery can be prompted to read the
canonical `SKILL.md` directly.

## Testing and Verification

Implementation verification will use temporary Git repositories and worktrees
where practical. It will cover:

1. resuming from a clean checkpoint;
2. staged, unstaged, and untracked manual changes;
3. manual commits after an agent checkpoint;
4. overlapping and non-overlapping changes;
5. missing checkpoints and rewritten history;
6. two independent tasks in separate worktrees;
7. rejection or serialization of overlapping parallel tasks;
8. exclusion of unrelated files from staged checkpoints;
9. accurate red, partial, green, and verified status reporting; and
10. confirmation that the workflow never pushes, merges, rebases, resets,
    tags, or bypasses hooks.

Repository validation will also check Markdown structure, skill frontmatter,
referenced paths, README instructions, the final diff, and Git status. No new
test framework or dependency will be introduced solely for this
instruction-only workflow.

## Documentation

`README.md` will explain:

- when to use checkpoint authorization;
- how approval grants local commit permission without granting integration
  permission;
- how to start, checkpoint, resume, and complete a task;
- how manual changes are reconciled;
- how parallel worktrees are assigned;
- how another agent reads the handoff and validates current Git state; and
- the explicit Claude Code prompt for reading `AGENTS.md` and
  `.agents/skills/agent-checkpoint/SKILL.md` without adding `CLAUDE.md` or a
  wrapper.

## Alternatives Considered

- **Commit-only checkpoints:** simple but insufficient because commits do not
  capture decisions, failed attempts, verification details, or next actions.
- **Handoff file without commits:** easy to read but does not guarantee a
  recoverable code snapshot.
- **Approval before every commit:** maximizes user control but prevents
  reliable periodic checkpoints and can fail when quota expires before
  approval.
- **Hooks or shared MCP memory:** potentially more automatic, but
  provider-specific, harder to secure, and unable to guarantee semantic
  summarization when all model quotas are exhausted.
- **Claude-specific wrapper or `CLAUDE.md`:** improves automatic discovery but
  is outside the approved first-version scope. The README will document manual
  loading instead.

## Success Criteria

The design is successful when an approved task can produce local, scoped,
recoverable checkpoints; a different agent can continue using only repository
state and documented prompts; manual changes are never silently overwritten;
independent tasks can run in isolated worktrees; and all integration or
history-rewriting actions remain separately authorized.
