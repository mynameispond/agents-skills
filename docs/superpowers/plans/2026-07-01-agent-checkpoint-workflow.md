# Agent Checkpoint Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repository-local, provider-neutral workflow for creating approved Git checkpoint commits, resuming safely after manual changes, and isolating parallel agent tasks.

**Architecture:** `AGENTS.md` supplies the mandatory authorization and safety policy, while a focused `agent-checkpoint` skill supplies the operational `start`, `checkpoint`, `resume`, and `complete` procedures. A committed handoff template carries task state between agents, and `README.md` documents installation and manual loading for tools such as Claude Code without adding provider-specific wrappers or global configuration.

**Tech Stack:** Markdown, Agent Skills `SKILL.md`, YAML UI metadata, Git, PowerShell-based repository validation with no added dependencies.

---

## File Structure

- Modify `AGENTS.md`: define checkpoint authorization, reconciliation, parallel-task isolation, and integration boundaries.
- Create `.agents/skills/agent-checkpoint/SKILL.md`: canonical provider-neutral checkpoint workflow.
- Create `.agents/skills/agent-checkpoint/assets/handoff-template.md`: task handoff schema copied to `.ai/handoffs/<task-id>.md` in consuming repositories.
- Create `.agents/skills/agent-checkpoint/agents/openai.yaml`: match existing skill metadata conventions for Codex presentation.
- Modify `README.md`: document the skill, fix stale `AGENTS.md` paths, explain checkpoint usage, manual-change recovery, parallel worktrees, and the explicit Claude Code prompt.
- Do not create `CLAUDE.md`, `.claude/`, hooks, scripts, dependencies, lockfile changes, or global configuration.

### Task 1: Define Checkpoint Policy in `AGENTS.md`

**Files:**
- Modify: `AGENTS.md:23`

- [ ] **Step 1: Run the policy contract check and confirm it fails**

Run:

```powershell
$text = Get-Content -Raw -Encoding utf8 'AGENTS.md'
$required = @(
    '## Checkpoint authorization',
    '## Resume reconciliation',
    '## Parallel task isolation',
    'local checkpoint commits',
    'user-owned or external-owned',
    'one writer',
    'push, merge, rebase, reset, tag'
)
$missing = @($required | Where-Object { -not $text.Contains($_) })
if ($missing.Count -gt 0) {
    Write-Error "Missing checkpoint policy: $($missing -join ', ')"
    exit 1
}
```

Expected: exit code `1` with all or most required policy strings reported as missing.

- [ ] **Step 2: Add the authorization and checkpoint policy**

Insert the following block after `## Approval gate` and before `## Bug workflow`:

```markdown
## Checkpoint authorization

- A change proposal may request authorization for local checkpoint commits. The proposal must name the task, approved scope, task branch or worktree, expected checkpoint milestones, test plan, and documentation plan.
- When the user explicitly approves a proposal that includes checkpoint authorization, the agent may edit within that scope and create local checkpoint commits without requesting approval before each commit.
- Checkpoint authorization applies only to the approved task and ends when the task completes, the user revokes it, or a material scope, requirement, design, security-boundary, or compatibility change occurs.
- A skill, plugin, workflow, plan, or tool instruction to commit does not grant checkpoint authorization by itself.
- Checkpoints must use a dedicated task branch and must not be committed directly to a protected or base branch.
- Before each checkpoint, inspect the working tree, exclude unrelated or external-owned changes, run fresh relevant verification, inspect the staged diff, and report failures or skipped checks accurately in the handoff and commit metadata.
- Checkpoint authorization never permits push, merge, rebase, reset, tag creation, branch deletion, history rewriting, hook bypass, or committing secrets and unresolved conflicts. These actions require separate explicit approval when applicable.

## Resume reconciliation

- Before a resumed or replacement agent writes files, it must find the latest reachable checkpoint for the task and inspect commits after it, staged changes, unstaged changes, untracked files, and branch or base divergence.
- Treat every change after the checkpoint as user-owned or external-owned. Do not infer ownership from the Git author, and do not overwrite, revert, stage, or commit those changes automatically.
- Non-overlapping changes may be preserved and excluded while work continues within the existing approval.
- If changes overlap the approved task without materially changing the design, summarize the overlap and obtain approval to adopt the current worktree as the new baseline before writing.
- If changes alter behavior, requirements, design, security, compatibility, or the approved scope, stop and obtain approval for a revised proposal.
- If the checkpoint is missing, history was rewritten, conflicts exist, or the baseline is ambiguous, stop and ask the user to establish a new baseline.
- Do not use checkout, reset, amend, rebase, or file replacement to force the worktree back to the old checkpoint.

## Parallel task isolation

- Parallel write tasks require one task branch, one worktree, and one handoff record per task, with one writer at a time in each worktree.
- Approvals, scopes, checkpoint sequences, and completion states are independent per task. A scope change in one task does not expand or invalidate another task automatically.
- Tasks that modify the same file, schema, public contract, generated artifact, or shared state must be serialized or assigned a single writer.
- Read-only investigation may run concurrently without a dedicated write worktree.
- If the base branch advances, report divergence and assess impact. Do not merge, rebase, or cherry-pick automatically.
- Combining task branches is a separate integration task requiring explicit approval, conflict assessment, and combined verification.
```

- [ ] **Step 3: Re-run the policy contract check**

Run the command from Step 1.

Expected: exit code `0` with no missing-policy error.

- [ ] **Step 4: Validate formatting and inspect scope**

Run:

```powershell
git diff --check
git diff -- AGENTS.md
git status --short
```

Expected:

- `git diff --check` produces no output.
- The diff adds only the three checkpoint policy sections.
- `git status --short` lists only `M AGENTS.md` plus any already approved plan-tracking change.

- [ ] **Step 5: Create the policy checkpoint commit**

Run:

```powershell
git add -- 'AGENTS.md'
git diff --cached --check
git diff --cached --name-status
git commit -m "docs: define agent checkpoint policy" -m "AI-Task: agent-checkpoint`nAI-Checkpoint: 3`nCheckpoint-State: verified`nValidation: policy contract check; git diff --cached --check"
```

Expected: one local commit containing only `AGENTS.md`.

### Task 2: Add the `agent-checkpoint` Skill

**Files:**
- Create: `.agents/skills/agent-checkpoint/SKILL.md`
- Create: `.agents/skills/agent-checkpoint/assets/handoff-template.md`
- Create: `.agents/skills/agent-checkpoint/agents/openai.yaml`

- [ ] **Step 1: Run the skill contract check and confirm it fails**

Run:

```powershell
$skill = '.agents/skills/agent-checkpoint/SKILL.md'
$template = '.agents/skills/agent-checkpoint/assets/handoff-template.md'
$metadata = '.agents/skills/agent-checkpoint/agents/openai.yaml'
$errors = [System.Collections.Generic.List[string]]::new()
foreach ($path in @($skill, $template, $metadata)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $errors.Add("Missing file: $path")
    }
}
if ($errors.Count -gt 0) {
    Write-Error ($errors -join [Environment]::NewLine)
    exit 1
}
```

Expected: exit code `1` reporting all three missing files.

- [ ] **Step 2: Create the canonical skill**

Create `.agents/skills/agent-checkpoint/SKILL.md` with:

```markdown
---
name: agent-checkpoint
description: Use when an approved coding task needs durable Git checkpoints or cross-agent handoff, resumes after model quota exhaustion or a long pause, must reconcile manual or external repository changes, or runs independent write tasks in parallel.
---

# Agent Checkpoint

Preserve recoverable task state in the repository so another agent can continue without the original conversation.

## Quick Reference

| Need | Operation | Required gate |
| --- | --- | --- |
| Begin durable work | `start` | Approved scope and checkpoint authorization |
| Save a recoverable milestone | `checkpoint` | Fresh verification and staged-diff review |
| Continue after a pause or handoff | `resume` | Read-only reconciliation before writes |
| Finish implementation | `complete` | Final verification and review |

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

Do not use this skill for read-only work or as permission to change project state.

## Handoff File

Copy `assets/handoff-template.md` to `.ai/handoffs/<task-id>.md` in the target repository. Keep one handoff per task. Update and commit it with every checkpoint.

Never store secrets, credentials, private session data, or full raw transcripts in the handoff.

## Operation: Start

1. Read all applicable `AGENTS.md` files and repository documentation.
2. Confirm checkpoint authorization, populate the handoff `Approval` section, and set `Checkpoint commits authorized` to `yes` only when approval is explicit.
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
4. Update the handoff with decisions, changed files, exact verification results, failed attempts, risks, next actions, and the previous checkpoint SHA.
5. Run fresh verification appropriate to the milestone.
6. Stage explicit approved paths with `git add -- <path>`. Do not use broad staging when unrelated changes exist.
7. Inspect `git diff --cached --check`, `git diff --cached --name-status`, and the complete staged diff.
8. Stop if the staged diff contains secrets, unresolved conflicts, unexplained generated files, out-of-scope changes, or an unrecoverable state.
9. Commit without bypassing hooks.
10. After the commit, derive the current checkpoint SHA from the latest reachable `AI-Task` trailer, re-run `git status --short`, and report both the SHA and any remaining changes.

Do not attempt to write the current commit's SHA into the same commit. Keep the handoff's current-SHA field as a resolution instruction and derive the value from Git after commit creation.

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

## Common Mistakes

- Treating the skill invocation as approval. Require an explicitly approved proposal.
- Staging the entire worktree. Stage explicit approved paths and inspect the staged diff.
- Trusting Git authorship to identify manual work. Treat every post-checkpoint change as external-owned.
- Letting two writers share a worktree. Use separate task worktrees or serialize the work.
- Cleaning history during completion. Stop and request separate integration approval.

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
```

- [ ] **Step 3: Create the handoff template**

Create `.agents/skills/agent-checkpoint/assets/handoff-template.md` with:

```markdown
# Agent Handoff: {{task_id}}

> Do not store secrets, credentials, private session data, or full raw transcripts in this file.

## Task

- Status: `planned`
- Goal:
- Done when:
- Last updated:

## Approval

- Approved scope:
- Approved checkpoint milestones:
- Checkpoint commits authorized: `no`
- Prohibited actions:

## Git State

- Base branch:
- Base commit:
- Task branch:
- Worktree:
- Previous checkpoint SHA:
- Current checkpoint SHA: resolve from the latest reachable `AI-Task` trailer
- Checkpoint number: `0`
- Checkpoint state:

## Ownership and Reconciliation

- Current writer:
- Last reconciled:
- Changes after checkpoint:
- Overlapping paths:
- Baseline decision:

## Decisions and Assumptions

1.

## Current Implementation

| Path | State | Summary |
| --- | --- | --- |

## Verification

| Command | Result | Notes |
| --- | --- | --- |

## Failed Attempts

| Attempt | Evidence | Conclusion |
| --- | --- | --- |

## Risks and Unverified Behavior

- None recorded.

## Next Actions

1.

## Completion

- Completed at:
- Final checkpoint SHA: resolve from the final verified `AI-Task` trailer
- Documentation:
- Residual risks:
- Integration approval required: `yes`
```

The double-braced values are template fields populated when a task starts; they are not unresolved implementation decisions.

- [ ] **Step 4: Create Codex UI metadata**

Create `.agents/skills/agent-checkpoint/agents/openai.yaml` with:

```yaml
interface:
  display_name: "Agent Checkpoint"
  short_description: "Create and resume scoped Git checkpoints"
  default_prompt: "Use $agent-checkpoint to checkpoint or resume this task without overwriting external changes."
```

- [ ] **Step 5: Run the full skill contract check**

Run:

```powershell
$skillPath = '.agents/skills/agent-checkpoint/SKILL.md'
$templatePath = '.agents/skills/agent-checkpoint/assets/handoff-template.md'
$metadataPath = '.agents/skills/agent-checkpoint/agents/openai.yaml'
$skill = Get-Content -Raw -Encoding utf8 $skillPath
$template = Get-Content -Raw -Encoding utf8 $templatePath
$metadata = Get-Content -Raw -Encoding utf8 $metadataPath
$requirements = @{
    $skillPath = @(
        'name: agent-checkpoint',
        '## Operation: Start',
        '## Operation: Checkpoint',
        '## Operation: Resume',
        '## Operation: Complete',
        'AI-Task:',
        'Checkpoint-State:',
        'user-owned or external-owned',
        'one writer',
        'push, merge, rebase, reset'
    )
    $templatePath = @(
        '## Approval',
        '## Git State',
        '## Ownership and Reconciliation',
        '## Verification',
        '## Failed Attempts',
        '## Next Actions',
        'Integration approval required: `yes`'
    )
    $metadataPath = @(
        'display_name: "Agent Checkpoint"',
        'default_prompt: "Use $agent-checkpoint'
    )
}
$contents = @{
    $skillPath = $skill
    $templatePath = $template
    $metadataPath = $metadata
}
$missing = [System.Collections.Generic.List[string]]::new()
foreach ($path in $requirements.Keys) {
    foreach ($value in $requirements[$path]) {
        if (-not $contents[$path].Contains($value)) {
            $missing.Add("$path -> $value")
        }
    }
}
if ($missing.Count -gt 0) {
    Write-Error "Missing skill contract:`n$($missing -join [Environment]::NewLine)"
    exit 1
}
```

Expected: exit code `0`.

- [ ] **Step 6: Validate the new skill files**

Run:

```powershell
git diff --check
git status --short
git diff -- '.agents/skills/agent-checkpoint'
```

Expected:

- no whitespace errors;
- exactly three new skill files;
- no scripts, hooks, dependencies, `.claude` files, or global files.

- [ ] **Step 7: Create the skill checkpoint commit**

Run:

```powershell
git add -- `
    '.agents/skills/agent-checkpoint/SKILL.md' `
    '.agents/skills/agent-checkpoint/assets/handoff-template.md' `
    '.agents/skills/agent-checkpoint/agents/openai.yaml'
git diff --cached --check
git diff --cached --name-status
git commit -m "feat: add agent checkpoint skill" -m "AI-Task: agent-checkpoint`nAI-Checkpoint: 4`nCheckpoint-State: green`nValidation: skill contract check; git diff --cached --check"
```

Expected: one local commit containing exactly the three new skill files.

### Task 3: Document Cross-Agent Usage

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Run the README contract check and confirm it fails**

Run:

```powershell
$readme = Get-Content -Raw -Encoding utf8 'README.md'
$required = @(
    '$agent-checkpoint',
    'AI-Task:',
    '.ai/handoffs/',
    'git worktree',
    '.agents/skills/agent-checkpoint/SKILL.md',
    'Claude Code',
    'user-owned',
    'ไม่ครอบคลุมการ push'
)
$missing = @($required | Where-Object { -not $readme.Contains($_) })
if ($missing.Count -gt 0) {
    Write-Error "Missing README coverage: $($missing -join ', ')"
    exit 1
}
```

Expected: exit code `1` with the new checkpoint documentation reported as missing.

- [ ] **Step 2: Correct stale repository paths**

Replace all documentation references to `.codex/AGENTS.md` with `AGENTS.md`.

Change the installation block from:

```text
.codex/AGENTS.md
.agents/skills/
```

to:

```text
AGENTS.md
.agents/skills/
```

Expected: `README.md` matches the actual repository layout without moving any files.

- [ ] **Step 3: Add the skill to component and workflow listings**

Add this bullet under `## ส่วนประกอบ`:

```markdown
- `.agents/skills/agent-checkpoint` - สร้าง local Git checkpoint ที่ได้รับอนุมัติ บันทึก handoff และตรวจ reconciliation ก่อนให้ agent ตัวใหม่ทำงานต่อ
```

Add this row to `## Workflow หลัก`:

```markdown
| งานต่อเนื่องหรือส่งต่อข้าม agent | ใช้ `$agent-checkpoint` หลัง proposal ได้รับอนุมัติให้สร้าง local checkpoint commits แล้ว; เมื่อ resume ต้องตรวจ commits, staged, unstaged, untracked และ base divergence ก่อนแก้ไฟล์ |
```

Add this row to `## Skills ที่มีในชุดนี้`:

```markdown
| `$agent-checkpoint` | ใช้สร้างและ resume local Git checkpoints ภายใน scope ที่อนุมัติ รองรับ quota หมด การแก้ไฟล์เองภายหลัง และหลายงานใน worktree แยกกัน โดยไม่อนุญาต push, merge หรือ rewrite history อัตโนมัติ |
```

- [ ] **Step 4: Add the checkpoint workflow guide**

Add the following section before `## หลักการใช้งาน`:

````markdown
## Checkpoint และการส่งต่องานข้าม Agent

ใช้ `$agent-checkpoint` เมื่องานอาจใช้หลาย session, เปลี่ยน AI provider, มีความเสี่ยงที่ quota จะหมด หรือมีหลายงานทำพร้อมกัน

ก่อนเริ่มแก้ไฟล์ proposal ต้องระบุ task ID, scope, task branch/worktree, checkpoint milestones, test plan และ documentation plan เมื่อผู้ใช้อนุมัติ proposal ที่รวม checkpoint authorization แล้ว agent สามารถสร้าง **local checkpoint commits** ภายใน scope นั้นโดยไม่ต้องขออนุมัติก่อนทุก commit

สิทธิ์นี้ไม่ครอบคลุมการ push, merge, rebase, reset, tag, ลบ branch, rewrite history, bypass hooks หรือรวมไฟล์ของผู้ใช้ที่อยู่นอก scope

แต่ละ task ใช้ handoff แยกกัน:

```text
.ai/handoffs/<task-id>.md
```

Checkpoint commit ใช้ trailers เพื่อให้ agent ตัวถัดไปค้นหา state ได้:

```text
AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

เมื่อกลับมาทำงานหลัง quota หมดหรือหลังผู้ใช้แก้ไฟล์เอง ให้ agent เริ่มด้วย `resume` และตรวจ:

```text
checkpoint..HEAD
staged changes
unstaged changes
untracked files
base-branch divergence
```

ให้ถือว่าทุกการเปลี่ยนแปลงหลัง checkpoint เป็น user-owned หรือ external-owned ห้าม reset, overwrite, stage หรือ commit อัตโนมัติ หากแก้คนละ path ให้รักษาไว้และทำงานต่อภายใน scope เดิม หากทับซ้อนหรือเปลี่ยน behavior/design ต้องขอ baseline หรือ proposal ใหม่ก่อนแก้ไฟล์

### หลายงานพร้อมกัน

งานที่เขียนไฟล์พร้อมกันต้องใช้หนึ่ง task branch, หนึ่ง `git worktree` และหนึ่ง handoff ต่อ task โดยมี writer เพียงหนึ่งตัวในแต่ละ worktree:

```text
Task auth    -> branch task/auth    -> worktree/auth
Task billing -> branch task/billing -> worktree/billing
```

งานที่แก้ไฟล์, schema, public contract หรือ shared state เดียวกันต้องทำตามลำดับ การรวม branch เป็น integration task แยกต่างหากและต้องได้รับอนุมัติใหม่

### ใช้กับ Claude Code โดยไม่เพิ่ม wrapper

Repo นี้ไม่เพิ่ม `CLAUDE.md` หรือ `.claude/skills` ให้เริ่ม Claude Code ใน repository เดียวกันแล้วส่ง prompt:

```text
Read and follow ./AGENTS.md.
Then read ./.agents/skills/agent-checkpoint/SKILL.md completely and use its
resume operation for task <task-id>.
Before editing, reconcile the latest AI-Task checkpoint with HEAD, staged,
unstaged, untracked, and base-divergence changes. Treat all post-checkpoint
changes as user-owned or external-owned. Do not overwrite, revert, stage, or
commit them without the required baseline approval.
```

แทน `<task-id>` ด้วย task จริง เช่น `auth`
````

- [ ] **Step 5: Add the checkpoint skill to usage principles**

Add these bullets under `## หลักการใช้งาน`:

```markdown
- ใช้ `$agent-checkpoint` เป็น workflow เสริมสำหรับ persistence และ handoff ไม่ใช้แทน debugging, planning, TDD, verification หรือ review
- การอนุมัติ checkpoint commits ครอบคลุมเฉพาะ local commits ใน task scope; integration และ history rewriting ต้องขออนุมัติแยก
- Agent ที่ resume ต้องทำ read-only reconciliation ก่อนเขียนไฟล์เสมอ และต้องรักษา manual/external changes ไว้
```

- [ ] **Step 6: Run the README and path checks**

Run:

```powershell
$readme = Get-Content -Raw -Encoding utf8 'README.md'
$required = @(
    '$agent-checkpoint',
    'AI-Task:',
    '.ai/handoffs/',
    'git worktree',
    '.agents/skills/agent-checkpoint/SKILL.md',
    'Claude Code',
    'user-owned',
    'ไม่ครอบคลุมการ push'
)
$missing = @($required | Where-Object { -not $readme.Contains($_) })
if ($missing.Count -gt 0) {
    Write-Error "Missing README coverage: $($missing -join ', ')"
    exit 1
}
if ($readme.Contains('.codex/AGENTS.md')) {
    Write-Error 'README still references the stale .codex/AGENTS.md path'
    exit 1
}
```

Expected: exit code `0`.

- [ ] **Step 7: Validate and review the README diff**

Run:

```powershell
git diff --check
git diff -- README.md
git status --short
```

Expected:

- Thai text remains UTF-8 and readable.
- Documentation names only repository-local files.
- No `CLAUDE.md`, `.claude/`, hook, or global-configuration change is introduced.

- [ ] **Step 8: Create the documentation checkpoint commit**

Run:

```powershell
git add -- 'README.md'
git diff --cached --check
git diff --cached --name-status
git commit -m "docs: explain cross-agent checkpoints" -m "AI-Task: agent-checkpoint`nAI-Checkpoint: 5`nCheckpoint-State: green`nValidation: README contract and path checks; git diff --cached --check"
```

Expected: one local commit containing only `README.md`.

### Task 4: Verify the Complete Workflow

**Files:**
- Verify: `AGENTS.md`
- Verify: `.agents/skills/agent-checkpoint/SKILL.md`
- Verify: `.agents/skills/agent-checkpoint/assets/handoff-template.md`
- Verify: `.agents/skills/agent-checkpoint/agents/openai.yaml`
- Verify: `README.md`
- Reference: `docs/superpowers/specs/2026-07-01-agent-checkpoint-design.md`

- [ ] **Step 1: Create an isolated scratch Git repository**

Run:

```powershell
$workspace = [System.IO.Path]::GetFullPath((Get-Location).Path)
$tmpRoot = [System.IO.Path]::GetFullPath((Join-Path $workspace '.tmp'))
$scratch = [System.IO.Path]::GetFullPath((Join-Path $tmpRoot 'agent-checkpoint-validation'))
$billing = [System.IO.Path]::GetFullPath((Join-Path $tmpRoot 'agent-checkpoint-billing'))
foreach ($path in @($scratch, $billing)) {
    if (-not $path.StartsWith($tmpRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Scratch path escaped .tmp: $path"
    }
    if (Test-Path -LiteralPath $path) {
        throw "Scratch path already exists: $path"
    }
}
New-Item -ItemType Directory -Path $scratch | Out-Null
git -C $scratch init -b main
git -C $scratch config user.name 'Agent Checkpoint Test'
git -C $scratch config user.email 'agent-checkpoint@example.invalid'
```

Expected: a new repository exists only at
`.tmp/agent-checkpoint-validation`, with no modification to tracked project
files.

- [ ] **Step 2: Create and commit the scratch baseline**

Use `apply_patch`:

```diff
*** Begin Patch
*** Add File: .tmp/agent-checkpoint-validation/app.txt
+base
*** End Patch
```

Then run:

```powershell
git -C '.tmp/agent-checkpoint-validation' add -- 'app.txt'
git -C '.tmp/agent-checkpoint-validation' commit -m 'chore: create baseline'
git -C '.tmp/agent-checkpoint-validation' rev-parse HEAD
```

Expected: one baseline commit on scratch `main`.

- [ ] **Step 3: Create a task checkpoint in the scratch repository**

Run:

```powershell
git -C '.tmp/agent-checkpoint-validation' switch -c task/auth
```

Use `apply_patch`:

```diff
*** Begin Patch
*** Update File: .tmp/agent-checkpoint-validation/app.txt
@@
-base
+agent checkpoint
*** Add File: .tmp/agent-checkpoint-validation/.ai/handoffs/auth.md
+# Agent Handoff: auth
+
+Status: partial
*** End Patch
```

Then run:

```powershell
git -C '.tmp/agent-checkpoint-validation' add -- 'app.txt' '.ai/handoffs/auth.md'
git -C '.tmp/agent-checkpoint-validation' commit -m 'checkpoint(auth): create recoverable state' -m "AI-Task: auth`nAI-Checkpoint: 1`nCheckpoint-State: partial`nValidation: fixture only`nHandoff: .ai/handoffs/auth.md"
$checkpoint = git -C '.tmp/agent-checkpoint-validation' log --grep='^AI-Task: auth$' --format='%H' -1
if ([string]::IsNullOrWhiteSpace($checkpoint)) {
    throw 'Scratch checkpoint was not discoverable by trailer'
}
"Checkpoint: $checkpoint"
```

Expected: the checkpoint is discoverable from its `AI-Task` trailer.

- [ ] **Step 4: Add a later manual commit**

Use `apply_patch`:

```diff
*** Begin Patch
*** Add File: .tmp/agent-checkpoint-validation/manual-commit.md
+manual committed change
*** End Patch
```

Then run:

```powershell
git -C '.tmp/agent-checkpoint-validation' add -- 'manual-commit.md'
git -C '.tmp/agent-checkpoint-validation' commit -m 'docs: add manual change'
$checkpoint = git -C '.tmp/agent-checkpoint-validation' log --grep='^AI-Task: auth$' --format='%H' -1
$after = @(git -C '.tmp/agent-checkpoint-validation' log --oneline "$checkpoint..HEAD")
if ($after.Count -ne 1) {
    throw "Expected one commit after checkpoint, found $($after.Count)"
}
$after
```

Expected: reconciliation can identify exactly one later commit without relying
on its author.

- [ ] **Step 5: Add staged, unstaged, and untracked manual changes**

Use `apply_patch`:

```diff
*** Begin Patch
*** Update File: .tmp/agent-checkpoint-validation/app.txt
@@
-agent checkpoint
+manual overlapping edit
*** Add File: .tmp/agent-checkpoint-validation/staged.md
+manual staged change
*** Add File: .tmp/agent-checkpoint-validation/untracked.md
+manual untracked change
*** End Patch
```

Then run:

```powershell
git -C '.tmp/agent-checkpoint-validation' add -- 'staged.md'
$status = @(git -C '.tmp/agent-checkpoint-validation' status --short)
if (-not ($status -match '^ M app\.txt$')) {
    throw 'Missing unstaged overlapping change'
}
if (-not ($status -match '^A  staged\.md$')) {
    throw 'Missing staged change'
}
if (-not ($status -match '^\?\? untracked\.md$')) {
    throw 'Missing untracked change'
}
$status
```

Expected: Git exposes all three working-state classes that `resume` must
reconcile, including an overlapping edit to `app.txt`.

- [ ] **Step 6: Verify parallel worktree isolation**

Run:

```powershell
$workspace = [System.IO.Path]::GetFullPath((Get-Location).Path)
$billing = [System.IO.Path]::GetFullPath((Join-Path $workspace '.tmp/agent-checkpoint-billing'))
git -C '.tmp/agent-checkpoint-validation' branch task/billing main
git -C '.tmp/agent-checkpoint-validation' worktree add $billing task/billing
$worktrees = @(git -C '.tmp/agent-checkpoint-validation' worktree list --porcelain | Select-String '^worktree ')
if ($worktrees.Count -ne 2) {
    throw "Expected two isolated worktrees, found $($worktrees.Count)"
}
$unreachable = git -C '.tmp/agent-checkpoint-validation' log main --grep='^AI-Task: auth$' --format='%H' -1
if (-not [string]::IsNullOrWhiteSpace($unreachable)) {
    throw 'Auth checkpoint should be unreachable from the scratch main baseline'
}
$worktrees
```

Expected: `task/auth` and `task/billing` have distinct working directories,
and the auth checkpoint is not incorrectly discoverable from the base branch.

- [ ] **Step 7: Remove validated scratch state safely**

Run:

```powershell
$workspace = [System.IO.Path]::GetFullPath((Get-Location).Path)
$tmpRoot = [System.IO.Path]::GetFullPath((Join-Path $workspace '.tmp'))
$scratch = [System.IO.Path]::GetFullPath((Join-Path $tmpRoot 'agent-checkpoint-validation'))
$billing = [System.IO.Path]::GetFullPath((Join-Path $tmpRoot 'agent-checkpoint-billing'))
foreach ($path in @($scratch, $billing)) {
    if (-not $path.StartsWith($tmpRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing cleanup outside .tmp: $path"
    }
}
if (Test-Path -LiteralPath $billing) {
    git -C $scratch worktree remove --force $billing
}
if (Test-Path -LiteralPath $scratch) {
    Remove-Item -Recurse -Force -LiteralPath $scratch
}
if ((Test-Path -LiteralPath $tmpRoot) -and -not (Get-ChildItem -Force -LiteralPath $tmpRoot)) {
    Remove-Item -Force -LiteralPath $tmpRoot
}
git status --short
```

Expected: both verified absolute targets are removed, `.tmp` is removed when
empty, and no scratch path appears in project status.

- [ ] **Step 8: Run the complete static contract**

Run:

```powershell
$files = @{
    agents = Get-Content -Raw -Encoding utf8 'AGENTS.md'
    skill = Get-Content -Raw -Encoding utf8 '.agents/skills/agent-checkpoint/SKILL.md'
    template = Get-Content -Raw -Encoding utf8 '.agents/skills/agent-checkpoint/assets/handoff-template.md'
    metadata = Get-Content -Raw -Encoding utf8 '.agents/skills/agent-checkpoint/agents/openai.yaml'
    readme = Get-Content -Raw -Encoding utf8 'README.md'
}
$checks = @(
    @('agents', '## Checkpoint authorization'),
    @('agents', '## Resume reconciliation'),
    @('agents', '## Parallel task isolation'),
    @('skill', '## Operation: Start'),
    @('skill', '## Operation: Checkpoint'),
    @('skill', '## Operation: Resume'),
    @('skill', '## Operation: Complete'),
    @('skill', 'staged, unstaged, and untracked'),
    @('skill', 'missing or unreachable'),
    @('skill', 'Parallel Tasks'),
    @('skill', 'push, merge, rebase, reset'),
    @('template', '## Ownership and Reconciliation'),
    @('template', '## Failed Attempts'),
    @('template', '## Risks and Unverified Behavior'),
    @('metadata', 'display_name: "Agent Checkpoint"'),
    @('readme', 'ใช้กับ Claude Code โดยไม่เพิ่ม wrapper'),
    @('readme', '.agents/skills/agent-checkpoint/SKILL.md'),
    @('readme', 'git worktree')
)
$missing = [System.Collections.Generic.List[string]]::new()
foreach ($check in $checks) {
    if (-not $files[$check[0]].Contains($check[1])) {
        $missing.Add("$($check[0]) -> $($check[1])")
    }
}
if ($missing.Count -gt 0) {
    Write-Error "Contract failures:`n$($missing -join [Environment]::NewLine)"
    exit 1
}
```

Expected: exit code `0`.

- [ ] **Step 9: Verify forbidden scope was not added**

Run:

```powershell
$forbidden = @(
    'CLAUDE.md',
    '.claude',
    '.codex/hooks.json',
    '.agents/skills/agent-checkpoint/scripts'
)
$present = @($forbidden | Where-Object { Test-Path -LiteralPath $_ })
if ($present.Count -gt 0) {
    Write-Error "Forbidden paths added: $($present -join ', ')"
    exit 1
}
git diff 'origin/main...HEAD' --name-only
```

Expected:

- exit code `0`;
- no forbidden path exists;
- changed paths are limited to the approved spec, plan, policy, skill, template, metadata, and README files.

- [ ] **Step 10: Verify real checkpoint trailer discovery**

Run:

```powershell
$latest = git log --all --grep='^AI-Task: agent-checkpoint$' --format='%H' -1
if ([string]::IsNullOrWhiteSpace($latest)) {
    Write-Error 'No reachable agent-checkpoint trailer was found'
    exit 1
}
$task = @(git show -s --format='%(trailers:key=AI-Task,valueonly)' $latest | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
$state = @(git show -s --format='%(trailers:key=Checkpoint-State,valueonly)' $latest | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
if ($task.Count -ne 1 -or $task[0].Trim() -ne 'agent-checkpoint') {
    Write-Error "Unexpected AI-Task trailer: $task"
    exit 1
}
if ($state.Count -ne 1 -or $state[0].Trim() -notin @('red', 'partial', 'green', 'verified')) {
    Write-Error "Unexpected checkpoint state: $state"
    exit 1
}
"Latest checkpoint: $latest ($($state[0].Trim()))"
```

Expected: exit code `0` and the latest reachable `agent-checkpoint` commit SHA with an allowed state.

- [ ] **Step 11: Review scenario coverage against the specification**

Run:

```powershell
$skill = Get-Content -Raw -Encoding utf8 '.agents/skills/agent-checkpoint/SKILL.md'
$scenarioTerms = @(
    'staged, unstaged, and untracked',
    'every post-checkpoint change',
    'non-overlapping changes',
    'overlapping changes',
    'missing or unreachable',
    'history',
    'one task branch, one worktree, and one handoff',
    'one writer',
    'share a file, schema, public contract, generated artifact, or mutable shared state',
    'push, merge, rebase, reset'
)
$missing = @($scenarioTerms | Where-Object { -not $skill.Contains($_) })
if ($missing.Count -gt 0) {
    Write-Error "Missing scenario coverage: $($missing -join ', ')"
    exit 1
}
```

Expected: exit code `0`, covering clean resume, manual working changes, later commits, missing history, overlap decisions, parallel isolation, shared-state serialization, and prohibited integration actions.

- [ ] **Step 12: Run final repository checks**

Run:

```powershell
git diff --check 'origin/main...HEAD'
git status --short
git log --oneline --decorate 'origin/main..HEAD'
git diff --stat 'origin/main...HEAD'
git diff 'origin/main...HEAD' -- AGENTS.md README.md '.agents/skills/agent-checkpoint'
```

Expected:

- no whitespace errors;
- no unexpected uncommitted files;
- checkpoint commits appear in order;
- only approved paths changed;
- the final diff matches the design and does not weaken the approval gate.

- [ ] **Step 13: Self-review the complete change**

Review the final diff against:

- the approved design and every success criterion;
- authorization expiration and re-approval boundaries;
- preservation of manual and external changes;
- one-writer worktree isolation;
- staged-file scope and secret/conflict rejection;
- exact validation reporting;
- provider neutrality;
- absence of global and Claude-specific files;
- README accuracy and UTF-8 preservation; and
- unintended changes outside the task.

If corrections are required, use `apply_patch`, rerun the affected task contract and all final checks, then create a focused local commit:

```powershell
git add -- `
    'AGENTS.md' `
    'README.md' `
    '.agents/skills/agent-checkpoint/SKILL.md' `
    '.agents/skills/agent-checkpoint/assets/handoff-template.md' `
    '.agents/skills/agent-checkpoint/agents/openai.yaml'
git diff --cached --check
git diff --cached --name-status
git commit -m "fix: align agent checkpoint workflow" -m "AI-Task: agent-checkpoint`nAI-Checkpoint: 6`nCheckpoint-State: verified`nValidation: full static contract; scenario coverage; git diff --cached --check"
```

If no correction is required, do not create an empty commit.

## Execution Boundary

This plan authorizes only repository-local implementation and local checkpoint
commits after the user chooses an execution approach. It does not authorize
push, merge, rebase, reset, squash, tag creation, branch deletion, history
rewriting, hooks, dependencies, `CLAUDE.md`, `.claude/`, or global
configuration changes.
