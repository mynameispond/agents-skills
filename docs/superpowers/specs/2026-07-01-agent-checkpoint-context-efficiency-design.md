# Agent Checkpoint Context Efficiency Design

## Summary

Reduce the routine context cost of the repository-local `agent-checkpoint`
workflow while preserving its Git safety, manual-change reconciliation, and
parallel-task isolation.

The skill will become explicitly invoked and progressively disclosed. A short
router remains in `SKILL.md`; operation details move to focused reference
files. The always-loaded `AGENTS.md` retains only the safety rules that must
apply even before the skill is invoked.

## Problem

The current workflow is safe but repeats detailed checkpoint instructions in
multiple places:

- checkpoint policy in the always-loaded `AGENTS.md`;
- the complete workflow in `SKILL.md`; and
- explanatory material in `README.md`, the original design, and its plan.

The documentation artifacts are not normally loaded automatically, but the
checkpoint policy in `AGENTS.md` is. When the skill is activated, its complete
1,239-word body is loaded even if the agent needs only one operation.

The user will monitor the five-hour quota window and explicitly invoke
`$agent-checkpoint` near the limit. The workflow therefore does not need
implicit activation or quota detection.

## Baseline

Measured before this change:

| File | Lines | Words | Characters | Loading behavior |
| --- | ---: | ---: | ---: | --- |
| `AGENTS.md` | 142 | 2,021 | 14,672 | Loaded for repository work |
| `.agents/skills/agent-checkpoint/SKILL.md` | 164 | 1,239 | 8,756 | Loaded when the skill activates |
| Handoff template | 72 | 199 | 1,260 | Copied when a handoff is created |
| `README.md` | 136 | 799 | 12,751 | Read on demand |

Only the checkpoint-related sections of `AGENTS.md` are in scope for
compression. The repository's general approval, debugging, feature, testing,
security, and documentation policies remain unchanged.

## Goals

- Keep checkpoint behavior inactive until the exact `$agent-checkpoint` skill
  token is used in Codex.
- Reduce always-loaded checkpoint policy to approximately 150-200 words.
- Keep the router `SKILL.md` at or below approximately 500 words when practical.
- Load only the reference needed for the selected operation.
- Support adopting work that started before the skill was invoked.
- Preserve manual and external changes when resuming.
- Preserve branch and worktree isolation for parallel write tasks even when the
  skill was not active at task start.
- Keep handoffs concise enough for a new agent to read quickly.
- Make no global configuration, model, MCP, or reasoning-setting changes.

## Non-Goals

- Detecting the user's remaining quota.
- Automatically invoking the skill near a quota boundary.
- Automatically creating or controlling a fresh Codex thread.
- Adding a Claude wrapper, `CLAUDE.md`, `.claude/skills`, hooks, or executable
  checkpoint scripts.
- Changing Superpowers behavior.
- Pushing, merging, rebasing, resetting, deleting branches, or rewriting
  history.
- Refactoring unrelated repository policy.

## Chosen Approach

Use repository-local progressive disclosure.

```text
AGENTS.md
.agents/skills/agent-checkpoint/
├── SKILL.md
├── agents/openai.yaml
├── assets/handoff-template.md
└── references/
    ├── checkpoint.md
    ├── resume.md
    └── parallel.md
README.md
```

### `AGENTS.md`

Replace the three detailed checkpoint sections with one compact checkpoint and
handoff policy. It must retain rules that apply before skill invocation:

- checkpoint commits require explicit approval and scoped local-commit
  authorization;
- unsafe integration and history-rewriting actions remain prohibited;
- post-checkpoint manual or external changes must be reconciled before writes;
- parallel write tasks use separate branches and worktrees with one writer per
  worktree; and
- overlapping files or shared contracts must be serialized.

Detailed commands, trailer formats, classifications, and completion reporting
move out of this always-loaded file.

### Router `SKILL.md`

The router contains:

- authorization and safety gates;
- operation selection;
- a one-line purpose for each operation;
- the required reference file for that operation;
- stop conditions that must be visible before loading references; and
- concise completion-report requirements.

It must not duplicate step-by-step Git commands from the references.

Operation routing:

| Requested operation | Required reference |
| --- | --- |
| `start`, `checkpoint`, or `complete` | `references/checkpoint.md` |
| `resume` | `references/resume.md` |
| Parallel task setup or checkpointing | `references/parallel.md` plus the operation reference |

The agent reads only the selected references completely. It does not preload
all references.

### Explicit Invocation

Add this Codex policy to `agents/openai.yaml`:

```yaml
policy:
  allow_implicit_invocation: false
```

The documented Codex invocation is the exact token `$agent-checkpoint`.
Natural-language phrases such as "checkpoint this" are not guaranteed to
activate the skill and must not be documented as equivalent.

This policy controls Codex skill activation only. Other agents that do not
support Codex skill metadata continue to use the manual README prompt that
directs them to read the repository files.

## Late Adoption

`start` must support work already in progress. The skill does not need to have
been invoked when implementation began.

Before changing state, late adoption performs read-only discovery:

1. Read applicable instructions and the approved task plan.
2. Inspect the current branch, worktree list, recent commits, staged changes,
   unstaged changes, and untracked files.
3. Identify the task goal, approved scope, current writer, base, branch, and
   worktree from repository evidence and user approval.
4. Treat unexplained or out-of-scope changes as user-owned or external-owned.
5. Obtain any missing checkpoint-commit authorization.
6. Create the task handoff and establish its first recoverable checkpoint only
   after the baseline is unambiguous.

Late adoption must stop rather than invent a baseline when ownership, scope,
branch ancestry, or overlapping changes are ambiguous.

## Parallel Work

`agent-checkpoint` does not initiate parallel execution. The environment's
normal workflow, such as Superpowers `using-git-worktrees`, creates isolated
worktrees before implementation.

The compact `AGENTS.md` rule ensures isolation still applies when
`$agent-checkpoint` has not been invoked:

```text
task A -> branch A -> worktree A -> writer A
task B -> branch B -> worktree B -> writer B
```

When invoked later, the skill adopts each existing task independently:

- one task ID, branch, worktree, and handoff per task;
- independent checkpoint numbering and validation;
- no broad staging across worktrees;
- no automatic merge, rebase, cherry-pick, or base synchronization; and
- serialized execution for shared files, schemas, public contracts, generated
  artifacts, or mutable shared state.

## Handoff Budget

The handoff is current operational state, not a transcript.

- Target no more than 500 words.
- Record the goal, approval, Git state, ownership, decisions, current
  implementation, latest verification, risks, and next one to three actions.
- Keep exact commands and concise outcomes, but omit raw logs and full diffs.
- Replace obsolete state rather than appending a chronological diary.
- Remove resolved failures and completed actions that no longer affect the next
  agent.
- Never store secrets, credentials, private session data, or hidden reasoning.

The existing template is already below the word limit; implementation should
clarify its pruning rules rather than expand it.

## Fresh-Thread Workflow

After a checkpoint, the user may start a fresh thread to reduce conversation
context. The new prompt should provide only:

- `$agent-checkpoint resume`;
- the task ID;
- the handoff path; and
- the exact approved plan path when one exists.

The new agent derives repository state from Git and the handoff. The user
should not paste the former conversation, raw diff, or complete plan into the
prompt.

Thread creation remains manual and outside the skill's authority.

## Error Handling and Safety

The router and references must stop before writes or commits when:

- checkpoint authorization is missing;
- the task is on a protected or base branch;
- scope, ownership, or baseline is ambiguous;
- manual or external changes overlap the task;
- behavior, requirements, design, security, or compatibility changed;
- Git history is missing or conflicting;
- staged content includes secrets or out-of-scope files; or
- the requested action requires integration or history rewriting.

Resume never uses checkout, reset, amend, rebase, or file replacement to
recreate an earlier checkpoint.

## Documentation

Update `README.md` to explain:

- exact `$agent-checkpoint` invocation;
- user-managed quota monitoring;
- late adoption of an existing branch or worktree;
- parallel isolation before checkpoint activation;
- the compact fresh-thread resume prompt;
- manual cross-agent use without a Claude wrapper; and
- the handoff size and pruning rules.

The original checkpoint design and workflow plan remain historical records and
are not rewritten.

## Validation

### Static contracts

- YAML parses and sets `allow_implicit_invocation: false`.
- Skill frontmatter remains valid and its description contains triggers only.
- Every router reference exists and every reference path resolves.
- `AGENTS.md` retains approval, reconciliation, and parallel-isolation rules.
- README uses the exact `$agent-checkpoint` token.
- No global configuration, wrapper, hook, script, or unrelated file is added.
- Word-count targets and before/after measurements are reported.

### Scratch Git scenarios

Use disposable repositories and worktrees to verify:

- late adoption of an existing clean task branch;
- late adoption with staged, unstaged, and untracked changes;
- preservation of a manual commit created after the last checkpoint;
- stop behavior for overlapping external changes;
- independent checkpoints in separate task worktrees; and
- refusal to combine tasks that share files or mutable contracts.

### Skill pressure test

Use one test-only subagent, as explicitly authorized by the user, for a
pressure scenario covering:

- a nearly exhausted quota;
- work that began without checkpoint activation;
- manual changes with uncertain ownership; and
- two apparent parallel tasks sharing a contract.

The agent must inspect first, refuse unsafe consolidation, request missing
authorization or baseline decisions, and select only the necessary reference
files. This subagent is for behavior validation only; implementation remains
inline.

### Final review

- Run repository-provided skill validation when dependencies are available.
- If an official validator cannot run, report the missing dependency and run
  equivalent frontmatter, YAML, path, and content checks.
- Run `git diff --check`.
- Self-review the final diff for safety regression, duplicated instructions,
  stale paths, unintended scope, and documentation consistency.

## Expected Impact

Routine repository conversations load fewer checkpoint-policy tokens because
`AGENTS.md` carries only the non-negotiable safety rules. Explicit skill use
loads a compact router and only the relevant operation reference. Handoffs and
fresh-thread prompts avoid replaying old conversation context.

The trade-off is that users must type `$agent-checkpoint` explicitly and agents
must follow a reference link before performing an operation. This is
intentional because the user monitors quota and wants predictable activation.

## Acceptance Criteria

- Codex implicit invocation is disabled for `agent-checkpoint`.
- Exact explicit invocation remains documented and functional.
- The compact router routes every supported operation without duplicating its
  detailed procedure.
- Late adoption works without requiring the skill at task start.
- Worktree isolation applies before and after skill activation.
- Manual and external changes remain protected during resume and adoption.
- The handoff remains at or below 500 words after normal checkpoint updates.
- The README describes fresh-thread and manual cross-agent continuation.
- Only repository-local files are changed.
- No model, MCP, reasoning, global configuration, Claude wrapper, or
  `CLAUDE.md` change is introduced.
