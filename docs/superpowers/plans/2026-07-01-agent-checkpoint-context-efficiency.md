# Agent Checkpoint Context Efficiency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce the routine context cost of `agent-checkpoint` while preserving explicit authorization, late adoption, reconciliation, and parallel-worktree safety.

**Architecture:** Keep a compact always-loaded repository policy, convert `SKILL.md` into an explicit-invocation router, and move operation details into three focused references. Validate the process with static contracts, one test-only pressure-test agent used before and after the edit, and disposable Git repositories.

**Tech Stack:** Markdown, YAML, Git, PowerShell, repository-local Codex skills

---

## Scope and File Responsibilities

| Path | Responsibility |
| --- | --- |
| `AGENTS.md` | Always-loaded authorization, reconciliation, and parallel-isolation invariants |
| `.agents/skills/agent-checkpoint/SKILL.md` | Compact operation router and hard safety gates |
| `.agents/skills/agent-checkpoint/references/checkpoint.md` | `start`, late adoption, `checkpoint`, and `complete` procedures |
| `.agents/skills/agent-checkpoint/references/resume.md` | Read-only reconciliation and baseline classification |
| `.agents/skills/agent-checkpoint/references/parallel.md` | Worktree isolation and per-task checkpoint rules |
| `.agents/skills/agent-checkpoint/agents/openai.yaml` | Codex UI metadata and explicit-only invocation policy |
| `.agents/skills/agent-checkpoint/assets/handoff-template.md` | Bounded current-state handoff |
| `README.md` | User-facing explicit invocation, late adoption, fresh-thread, and cross-agent guidance |

Do not modify global configuration, model settings, MCP settings, reasoning
settings, the original checkpoint design/plan, or any Claude wrapper path.

### Task 1: Establish RED Baselines

**Files:**
- Inspect: `AGENTS.md`
- Inspect: `.agents/skills/agent-checkpoint/SKILL.md`
- Inspect: `.agents/skills/agent-checkpoint/agents/openai.yaml`
- Inspect: `.agents/skills/agent-checkpoint/assets/handoff-template.md`
- Inspect: `README.md`
- Test: inline PowerShell contracts and one test-only subagent

- [ ] **Step 1: Confirm the worktree is clean and record the baseline**

Run:

```powershell
git status --short
git branch --show-current
$paths = @(
    'AGENTS.md',
    '.agents/skills/agent-checkpoint/SKILL.md',
    '.agents/skills/agent-checkpoint/assets/handoff-template.md',
    '.agents/skills/agent-checkpoint/agents/openai.yaml',
    'README.md'
)
foreach ($path in $paths) {
    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
    [pscustomobject]@{
        Path = $path
        Lines = ($text -split "`r?`n").Count
        Words = ([regex]::Matches($text, '\S+')).Count
        Chars = $text.Length
    }
}
```

Expected:

```text
git status --short produces no output
branch is main
AGENTS.md is approximately 2,021 words
SKILL.md is approximately 1,239 words
handoff-template.md is approximately 199 words
```

- [ ] **Step 2: Run the static contract and verify RED**

Run:

```powershell
$errors = [System.Collections.Generic.List[string]]::new()
$agents = Get-Content -Raw -Encoding UTF8 -LiteralPath 'AGENTS.md'
$skill = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/SKILL.md'
$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/agents/openai.yaml'

$checkpointPolicy = [regex]::Match(
    $agents,
    '(?s)## Checkpoint authorization.*?(?=## Bug workflow)'
).Value
$policyWords = ([regex]::Matches($checkpointPolicy, '\S+')).Count
if ($policyWords -gt 220) {
    $errors.Add("checkpoint policy exceeds 220 words: $policyWords")
}
if ($agents -notmatch '(?m)^## Checkpoint and handoff policy$') {
    $errors.Add('compact checkpoint policy heading is missing')
}
if (([regex]::Matches($skill, '\S+')).Count -gt 500) {
    $errors.Add('SKILL.md exceeds 500 words')
}
foreach ($reference in @('checkpoint.md', 'resume.md', 'parallel.md')) {
    $path = ".agents/skills/agent-checkpoint/references/$reference"
    if (-not (Test-Path -LiteralPath $path)) {
        $errors.Add("missing reference: $path")
    }
}
if ($yaml -notmatch '(?m)^\s*allow_implicit_invocation:\s*false\s*$') {
    $errors.Add('implicit invocation is not disabled')
}
if ($errors.Count -eq 0) {
    throw 'Expected the baseline contract to fail, but it passed.'
}
$errors
```

Expected failures:

```text
checkpoint policy exceeds 220 words
compact checkpoint policy heading is missing
SKILL.md exceeds 500 words
missing reference: checkpoint.md
missing reference: resume.md
missing reference: parallel.md
implicit invocation is not disabled
```

- [ ] **Step 3: Spawn the single authorized test-only agent**

Use one subagent with no write authority and this exact prompt:

```text
You are the single test-only agent authorized for this task. Do not edit files,
stage, commit, create branches, or create worktrees.

Read the current repository-local agent-checkpoint instructions and evaluate
this pressure scenario:

The user explicitly invokes "$agent-checkpoint start" near quota exhaustion.
Work began before the skill was invoked. The current worktree has staged,
unstaged, and untracked changes of uncertain ownership. Two proposed parallel
tasks both modify the same public contract. Checkpoint commit authorization is
not shown.

Return only:
1. files you had to read;
2. whether you may write or commit;
3. whether the two tasks may run in parallel;
4. the next safe action;
5. any instruction gap or unnecessary content you had to load.
```

Expected baseline evidence:

```text
The current monolithic SKILL.md must be read in full.
No operation-specific references exist.
The agent must refuse writes and commits because authorization is missing.
The shared public contract must force serialization.
Late adoption is not named as a first-class route.
```

Keep this agent idle after its response. Reuse the same agent in Task 5 so the
authorized subagent count remains one.

- [ ] **Step 4: Record the RED evidence without changing repository files**

Summarize in the execution log:

```text
Static RED: policy/router/references/explicit-invocation contracts failed.
Pressure RED: <exact gaps reported by the test-only agent>.
```

Do not commit in this task because no repository file changes.

### Task 2: Compress the Always-Loaded Policy

**Files:**
- Modify: `AGENTS.md:28-55`
- Test: inline PowerShell policy contract

- [ ] **Step 1: Re-run the policy-only failing contract**

Run:

```powershell
$agents = Get-Content -Raw -Encoding UTF8 -LiteralPath 'AGENTS.md'
$section = [regex]::Match(
    $agents,
    '(?s)## Checkpoint authorization.*?(?=## Bug workflow)'
).Value
$words = ([regex]::Matches($section, '\S+')).Count
if ($words -le 220) {
    throw "Expected RED policy size above 220 words, got $words."
}
"RED: checkpoint policy is $words words"
```

Expected:

```text
RED: checkpoint policy is greater than 220 words
```

- [ ] **Step 2: Replace the three checkpoint sections with one compact policy**

Replace `## Checkpoint authorization`, `## Resume reconciliation`, and
`## Parallel task isolation` with:

```markdown
## Checkpoint and handoff policy

- Invoking `$agent-checkpoint`, a skill, or a plan never grants permission to edit or commit. A proposal must identify the task, scope, task branch or worktree, checkpoint milestones, tests, documentation, and explicitly authorize local checkpoint commits. Authorization ends on completion, revocation, or any material scope, requirement, design, security, or compatibility change.
- Checkpoints require a dedicated task branch. Before each commit, inspect the worktree, exclude unrelated or external-owned changes, run fresh relevant checks, and inspect the staged diff. Authorization never permits push, merge, rebase, reset, tags, branch deletion, history rewriting, hook bypass, dependency installation, production changes, secrets, or unresolved conflicts.
- Before a resumed or replacement agent writes, reconcile the latest task checkpoint with later commits, staged, unstaged, untracked, and base-divergence changes. Treat every later change as user-owned or external-owned. Preserve non-overlapping changes; obtain baseline approval for overlap; obtain a revised proposal when behavior or scope changed.
- Parallel write tasks require one task branch, worktree, handoff, and writer per task. Serialize tasks sharing files, schemas, public contracts, generated artifacts, or mutable state. Base synchronization and branch integration require separate approval.
- Stop when the checkpoint, history, ownership, baseline, or scope is ambiguous. Never force recovery with checkout, reset, amend, rebase, or file replacement.
```

- [ ] **Step 3: Verify the compact policy**

Run:

```powershell
$agents = Get-Content -Raw -Encoding UTF8 -LiteralPath 'AGENTS.md'
$section = [regex]::Match(
    $agents,
    '(?s)## Checkpoint and handoff policy.*?(?=## Bug workflow)'
).Value
$words = ([regex]::Matches($section, '\S+')).Count
if ($words -lt 150 -or $words -gt 220) {
    throw "Checkpoint policy must be 150-220 words, got $words."
}
foreach ($required in @(
    'explicitly authorize local checkpoint commits',
    'Treat every later change as user-owned or external-owned',
    'one task branch, worktree, handoff, and writer per task',
    'Serialize tasks sharing files',
    'Never force recovery'
)) {
    if ($section -notmatch [regex]::Escape($required)) {
        throw "Missing safety contract: $required"
    }
}
"GREEN: compact checkpoint policy is $words words"
```

Expected:

```text
GREEN: compact checkpoint policy is between 150 and 220 words
```

- [ ] **Step 4: Inspect and commit only the policy change**

Run:

```powershell
git diff --check
git diff -- AGENTS.md
git add -- AGENTS.md
git diff --cached --check
git diff --cached --name-status
git commit -m "docs: compress checkpoint repository policy"
```

Expected:

```text
Only AGENTS.md is staged.
Commit succeeds without bypassing hooks.
```

### Task 3: Build the Explicit Router and Focused References

**Files:**
- Modify: `.agents/skills/agent-checkpoint/SKILL.md`
- Create: `.agents/skills/agent-checkpoint/references/checkpoint.md`
- Create: `.agents/skills/agent-checkpoint/references/resume.md`
- Create: `.agents/skills/agent-checkpoint/references/parallel.md`
- Modify: `.agents/skills/agent-checkpoint/agents/openai.yaml`
- Test: inline PowerShell router and YAML contracts

- [ ] **Step 1: Verify the router contract is still RED**

Run:

```powershell
$skillPath = '.agents/skills/agent-checkpoint/SKILL.md'
$skill = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillPath
$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/agents/openai.yaml'
$missing = @(
    'references/checkpoint.md',
    'references/resume.md',
    'references/parallel.md'
) | Where-Object { $skill -notmatch [regex]::Escape($_) }
if ($missing.Count -eq 0) {
    throw 'Expected RED: router already names every reference.'
}
if ($yaml -match '(?m)^\s*allow_implicit_invocation:\s*false\s*$') {
    throw 'Expected RED: implicit invocation is already disabled.'
}
"RED: missing routes: $($missing -join ', ')"
```

Expected:

```text
RED: missing routes: references/checkpoint.md, references/resume.md, references/parallel.md
```

- [ ] **Step 2: Replace `SKILL.md` with the compact router**

Use this complete content:

```markdown
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

## Report

Report the task, branch, worktree, latest checkpoint SHA and state, committed
and intentionally uncommitted paths, exact verification outcomes, skipped or
failed checks, documentation, next actions, risks, and required approvals.
```

- [ ] **Step 3: Create `references/checkpoint.md`**

Use this complete content:

````markdown
# Start, Checkpoint, and Complete

## Start

1. Read applicable `AGENTS.md` files, repository documentation, and the
   approved specification or plan.
2. Confirm every authorization field required by `SKILL.md`.
3. Inspect `git status --short`, the current branch, recent commits, and
   `git worktree list`.
4. Refuse direct checkpoint commits on a protected or base branch.
5. Copy the handoff template and record the task, approval, base branch and
   commit, task branch, worktree, completion criteria, writer, and next one to
   three actions.
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
3. Update the handoff with decisions, changed paths, exact checks, relevant
   failures, risks, next actions, and the previous checkpoint SHA.
4. Prune resolved failures, completed actions, raw logs, and obsolete state;
   keep the handoff at or below 500 words.
5. Run fresh verification for the milestone.
6. Stage explicit approved paths with `git add -- <path>`.
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
````

- [ ] **Step 4: Create `references/resume.md`**

Use this complete content:

````markdown
# Resume and Reconciliation

Remain read-only until reconciliation is complete.

1. Read the handoff and locate the latest reachable commit whose `AI-Task`
   trailer matches the task.
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

4. Treat every post-checkpoint change as user-owned or external-owned,
   regardless of Git author.
5. Classify the repository state:

| State | Action |
| --- | --- |
| No later changes | Continue from the handoff within existing approval |
| Non-overlapping changes | Preserve and exclude them, then continue |
| Overlap without material design impact | Summarize it and request approval to adopt the current worktree as the new baseline |
| Changed behavior, requirements, design, security, compatibility, or scope | Propose a revision and obtain approval |
| Missing history, conflicts, or ambiguity | Stop and request a baseline decision |

6. After approval of a changed baseline, update the handoff and create a
   reconciliation checkpoint before implementation continues.

Never use checkout, reset, amend, rebase, or file replacement to recreate the
old checkpoint. Never stage or commit post-checkpoint changes until ownership,
scope, and baseline authorization are explicit.
````

- [ ] **Step 5: Create `references/parallel.md`**

Use this complete content:

```markdown
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
```

- [ ] **Step 6: Disable implicit Codex invocation**

Replace `.agents/skills/agent-checkpoint/agents/openai.yaml` with:

```yaml
interface:
  display_name: "Agent Checkpoint"
  short_description: "Create and resume scoped Git checkpoints"
  default_prompt: "Use $agent-checkpoint to checkpoint or resume this task without overwriting external changes."

policy:
  allow_implicit_invocation: false
```

- [ ] **Step 7: Run router, reference, and YAML contracts**

Run:

```powershell
$skillPath = '.agents/skills/agent-checkpoint/SKILL.md'
$skill = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillPath
$skillWords = ([regex]::Matches($skill, '\S+')).Count
if ($skillWords -gt 500) {
    throw "SKILL.md exceeds 500 words: $skillWords"
}

$frontmatter = [regex]::Match($skill, '(?s)\A---\r?\n(.*?)\r?\n---').Groups[1].Value
if ($frontmatter -notmatch '(?m)^name:\s*agent-checkpoint\s*$') {
    throw 'Invalid skill name.'
}
if ($frontmatter -notmatch '(?m)^description:\s*Use when ') {
    throw 'Description must start with Use when.'
}

foreach ($relative in @(
    'references/checkpoint.md',
    'references/resume.md',
    'references/parallel.md'
)) {
    if ($skill -notmatch [regex]::Escape($relative)) {
        throw "Router does not name $relative"
    }
    $resolved = Join-Path '.agents/skills/agent-checkpoint' $relative
    if (-not (Test-Path -LiteralPath $resolved)) {
        throw "Missing reference $resolved"
    }
}

$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/agents/openai.yaml'
if ($yaml -notmatch '(?m)^policy:\s*$' -or
    $yaml -notmatch '(?m)^\s{2}allow_implicit_invocation:\s*false\s*$') {
    throw 'Explicit-only invocation policy is invalid.'
}

"GREEN: router=$skillWords words; all references and explicit policy valid"
```

Expected:

```text
GREEN: router is at or below 500 words; all references and explicit policy valid
```

- [ ] **Step 8: Inspect and commit the router slice**

Run:

```powershell
$paths = @(
    '.agents/skills/agent-checkpoint/SKILL.md',
    '.agents/skills/agent-checkpoint/references/checkpoint.md',
    '.agents/skills/agent-checkpoint/references/resume.md',
    '.agents/skills/agent-checkpoint/references/parallel.md',
    '.agents/skills/agent-checkpoint/agents/openai.yaml'
)
git diff --check
git diff --stat
git diff -- $paths
git add -- $paths
git diff --cached --check
git diff --cached --name-status
git commit -m "feat: make agent checkpoint progressively disclosed"
```

Expected:

```text
Only the router, three references, and openai.yaml are staged.
Commit succeeds without bypassing hooks.
```

### Task 4: Bound the Handoff and Document the User Workflow

**Files:**
- Modify: `.agents/skills/agent-checkpoint/assets/handoff-template.md:1-3`
- Modify: `README.md:38-129`
- Test: inline PowerShell documentation contracts

- [ ] **Step 1: Verify the documentation contract is RED**

Run:

```powershell
$readme = Get-Content -Raw -Encoding UTF8 -LiteralPath 'README.md'
$template = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/assets/handoff-template.md'
$missing = @()
foreach ($phrase in @(
    'ไม่เรียก skill อัตโนมัติ',
    'late adoption',
    '$agent-checkpoint resume',
    'ไม่เกิน 500 คำ',
    'เริ่ม thread ใหม่'
)) {
    if ($readme -notmatch [regex]::Escape($phrase)) {
        $missing += $phrase
    }
}
if ($template -notmatch '500 words') {
    $missing += 'template 500-word rule'
}
if ($missing.Count -eq 0) {
    throw 'Expected RED documentation contract to fail.'
}
"RED: missing documentation: $($missing -join '; ')"
```

Expected:

```text
RED includes explicit-only activation, late adoption, fresh-thread, and handoff-budget gaps
```

- [ ] **Step 2: Add the bounded-state rule to the handoff template**

Replace the opening note with:

```markdown
# Agent Handoff: {{task_id}}

> Keep this file at or below 500 words. Store current operational state, not a
> chronological diary. Remove resolved failures, completed actions, raw logs,
> and obsolete details. Never store secrets, credentials, private session
> data, full transcripts, full diffs, or hidden reasoning.
```

Keep the existing sections after this note unchanged.

- [ ] **Step 3: Replace the README checkpoint section**

Replace the section from `## Checkpoint และการส่งต่องานข้าม Agent` through the
line before `## หลักการใช้งาน` with:

````markdown
## Checkpoint และการส่งต่องานข้าม Agent

Codex ไม่เรียก skill อัตโนมัติ ผู้ใช้ตรวจโควต้าเองและเรียกด้วย token
`$agent-checkpoint` เมื่อจำเป็น:

```text
$agent-checkpoint start
$agent-checkpoint checkpoint
$agent-checkpoint resume
$agent-checkpoint complete
```

คำสั่งทั่วไปอย่าง “checkpoint ด้วย” ไม่รับประกันว่าจะเปิด skill ให้ใช้ token
ข้างต้นโดยตรง

ก่อนแก้ไฟล์ proposal ต้องระบุ task ID, scope, task branch/worktree, checkpoint
milestones, test plan และ documentation plan พร้อมขอสิทธิ์สร้าง local
checkpoint commits อย่างชัดเจน สิทธิ์นี้ไม่ครอบคลุม push, merge, rebase, reset,
tag, ลบ branch, rewrite history, bypass hooks หรือไฟล์นอก scope

### เรียกใช้หลังงานเริ่มไปแล้ว

รองรับ late adoption โดยไม่ต้องเปิด skill ตั้งแต่เริ่มงาน เมื่อเรียก
`$agent-checkpoint start` ภายหลัง agent จะตรวจ branch, worktree, commits,
staged, unstaged และ untracked แบบ read-only ก่อนสร้าง handoff หาก ownership,
scope, ancestry หรือ baseline ไม่ชัดเจน agent ต้องหยุดถาม ห้ามเดาหรือย้อน
worktree กลับ

แต่ละ task ใช้ `.ai/handoffs/<task-id>.md` แยกกัน Handoff เก็บเฉพาะ goal,
approval, Git state, decisions, implementation ล่าสุด, verification, risks และ
next actions 1-3 ข้อ โดยไม่เกิน 500 คำ ไม่เก็บ raw logs, full diffs หรือ
conversation transcript

Checkpoint commit ใช้ trailers:

```text
AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

### เริ่ม thread ใหม่เพื่อลด context

หลัง checkpoint ผู้ใช้สามารถเริ่ม thread ใหม่แล้วส่งข้อมูลเท่าที่จำเป็น:

```text
$agent-checkpoint resume
Task: auth
Handoff: .ai/handoffs/auth.md
Plan: docs/superpowers/plans/<approved-plan>.md
```

Agent ใหม่ต้อง derive สถานะจาก Git และ handoff ไม่ต้องคัดลอก conversation,
raw diff หรือเนื้อหา plan ทั้งไฟล์ลงใน prompt

### หลายงานพร้อมกัน

การแยกงานเกิดจาก workflow ปกติ เช่น Superpowers `using-git-worktrees`
ไม่ใช่จาก `agent-checkpoint` งานเขียนไฟล์พร้อมกันต้องมีหนึ่ง task branch, หนึ่ง
worktree, หนึ่ง handoff และหนึ่ง writer ต่อ task แม้ยังไม่ได้เปิด skill:

```text
Task auth    -> branch task/auth    -> worktree/auth
Task billing -> branch task/billing -> worktree/billing
```

งานที่ใช้ไฟล์, schema, public contract, generated artifact หรือ shared state
เดียวกันต้องทำตามลำดับ เมื่อเรียก checkpoint ภายหลัง agent จะทำ late adoption
และ checkpoint แต่ละ worktree แยกกัน การรวม branch เป็น integration task ที่
ต้องขออนุมัติใหม่

### ใช้กับ Claude Code โดยไม่เพิ่ม wrapper

Repo นี้ไม่เพิ่ม `CLAUDE.md` หรือ `.claude/skills` ให้เริ่ม Claude Code ใน
repository เดียวกันแล้วส่ง prompt:

```text
Read and follow ./AGENTS.md.
Then read ./.agents/skills/agent-checkpoint/SKILL.md completely.
Use its resume route for task <task-id> and read only the references required
by that route. Before editing, reconcile the latest AI-Task checkpoint with
HEAD, staged, unstaged, untracked, and base-divergence changes. Treat all
post-checkpoint changes as user-owned or external-owned.
```

แทน `<task-id>` ด้วย task จริง เช่น `auth`
````

- [ ] **Step 4: Adjust the workflow table to state explicit invocation**

Replace the checkpoint workflow row with:

```markdown
| งานต่อเนื่องหรือส่งต่อข้าม agent | ผู้ใช้ตรวจโควต้าและเรียก `$agent-checkpoint` ด้วย token นี้โดยตรงเมื่อจำเป็น; รองรับ late adoption และ resume หลัง quota หมดหรือมี manual changes |
```

- [ ] **Step 5: Run documentation contracts**

Run:

```powershell
$readme = Get-Content -Raw -Encoding UTF8 -LiteralPath 'README.md'
$template = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/assets/handoff-template.md'

foreach ($phrase in @(
    'ไม่เรียก skill อัตโนมัติ',
    'late adoption',
    '$agent-checkpoint resume',
    'ไม่เกิน 500 คำ',
    'เริ่ม thread ใหม่',
    'using-git-worktrees',
    'Repo นี้ไม่เพิ่ม `CLAUDE.md`'
)) {
    if ($readme -notmatch [regex]::Escape($phrase)) {
        throw "README missing: $phrase"
    }
}
if ($template -notmatch 'at or below 500 words') {
    throw 'Handoff template lacks the 500-word limit.'
}
if ($readme -match '(?i)automatically detect.*quota') {
    throw 'README incorrectly claims automatic quota detection.'
}
"GREEN: explicit invocation, late adoption, fresh thread, parallel work, and handoff budget documented"
```

Expected:

```text
GREEN: explicit invocation, late adoption, fresh thread, parallel work, and handoff budget documented
```

- [ ] **Step 6: Inspect and commit the documentation slice**

Run:

```powershell
git diff --check
git diff -- README.md '.agents/skills/agent-checkpoint/assets/handoff-template.md'
git add -- README.md '.agents/skills/agent-checkpoint/assets/handoff-template.md'
git diff --cached --check
git diff --cached --name-status
git commit -m "docs: explain explicit checkpoint handoff"
```

Expected:

```text
Only README.md and handoff-template.md are staged.
Commit succeeds without bypassing hooks.
```

### Task 5: Verify Behavior, Git Scenarios, and Context Reduction

**Files:**
- Verify: all files listed in the scope table
- Test: the same test-only subagent, disposable Git repositories, static contracts, official validator when available

- [ ] **Step 1: Re-run the full static contract**

Run:

```powershell
$errors = [System.Collections.Generic.List[string]]::new()
$agents = Get-Content -Raw -Encoding UTF8 -LiteralPath 'AGENTS.md'
$skill = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/SKILL.md'
$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/agents/openai.yaml'
$readme = Get-Content -Raw -Encoding UTF8 -LiteralPath 'README.md'
$template = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/assets/handoff-template.md'

$policy = [regex]::Match(
    $agents,
    '(?s)## Checkpoint and handoff policy.*?(?=## Bug workflow)'
).Value
$policyWords = ([regex]::Matches($policy, '\S+')).Count
$skillWords = ([regex]::Matches($skill, '\S+')).Count
$templateWords = ([regex]::Matches($template, '\S+')).Count

if ($policyWords -lt 150 -or $policyWords -gt 220) {
    $errors.Add("policy words: $policyWords")
}
if ($skillWords -gt 500) {
    $errors.Add("skill words: $skillWords")
}
if ($templateWords -gt 500) {
    $errors.Add("template words: $templateWords")
}
if ($yaml -notmatch '(?m)^\s{2}allow_implicit_invocation:\s*false\s*$') {
    $errors.Add('implicit invocation policy')
}
foreach ($reference in @('checkpoint.md', 'resume.md', 'parallel.md')) {
    $relative = "references/$reference"
    $path = ".agents/skills/agent-checkpoint/$relative"
    if (-not (Test-Path -LiteralPath $path)) {
        $errors.Add("missing $path")
    }
    if ($skill -notmatch [regex]::Escape($relative)) {
        $errors.Add("router missing $relative")
    }
}
foreach ($phrase in @(
    '$agent-checkpoint resume',
    'late adoption',
    'เริ่ม thread ใหม่',
    'ไม่เกิน 500 คำ'
)) {
    if ($readme -notmatch [regex]::Escape($phrase)) {
        $errors.Add("README missing $phrase")
    }
}
if ($errors.Count -gt 0) {
    throw ($errors -join [Environment]::NewLine)
}
"GREEN: policy=$policyWords, router=$skillWords, template=$templateWords words"
```

Expected:

```text
GREEN with policy 150-220 words, router no more than 500 words, and template no more than 500 words
```

- [ ] **Step 2: Reuse the same test-only agent for GREEN**

Send a follow-up to the Task 1 agent:

```text
Re-read the updated repository-local agent-checkpoint instructions and repeat
the same pressure scenario. Do not mutate the repository.

Return only:
1. files selected by the router;
2. whether you may write or commit;
3. whether the two tasks may run in parallel;
4. the next safe action;
5. whether late adoption and the minimum-reference rule are explicit.
```

Expected:

```text
Reads SKILL.md, references/checkpoint.md, and references/parallel.md.
Does not read references/resume.md because no prior checkpoint is being resumed.
Refuses writes and commits because authorization is absent.
Serializes the tasks because they share a public contract.
Performs read-only late-adoption discovery and requests the missing approval or baseline.
```

- [ ] **Step 3: Run disposable Git reconciliation and worktree scenarios**

Run this in PowerShell:

```powershell
$root = Join-Path ([IO.Path]::GetTempPath()) ("agent-checkpoint-" + [guid]::NewGuid().ToString('N'))
$resolvedRoot = [IO.Path]::GetFullPath($root)
$resolvedTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
if (-not $resolvedRoot.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Scratch path escaped temp: $resolvedRoot"
}

try {
    New-Item -ItemType Directory -Path $resolvedRoot | Out-Null
    git -C $resolvedRoot init -b main | Out-Null
    git -C $resolvedRoot config user.email 'checkpoint-test@example.invalid'
    git -C $resolvedRoot config user.name 'Checkpoint Test'
    Set-Content -LiteralPath (Join-Path $resolvedRoot 'a.txt') -Value 'base-a'
    Set-Content -LiteralPath (Join-Path $resolvedRoot 'b.txt') -Value 'base-b'
    Set-Content -LiteralPath (Join-Path $resolvedRoot 'contract.txt') -Value 'v1'
    git -C $resolvedRoot add -- a.txt b.txt contract.txt
    git -C $resolvedRoot commit -m 'base' | Out-Null

    $worktreeA = "$resolvedRoot-a"
    $worktreeB = "$resolvedRoot-b"
    git -C $resolvedRoot worktree add -b task/a $worktreeA main | Out-Null
    git -C $resolvedRoot worktree add -b task/b $worktreeB main | Out-Null

    Set-Content -LiteralPath (Join-Path $worktreeA 'a.txt') -Value 'checkpoint-a'
    git -C $worktreeA add -- a.txt
    git -C $worktreeA commit -m "checkpoint(a): slice`n`nAI-Task: a`nAI-Checkpoint: 1`nCheckpoint-State: partial`nValidation: fixture`nHandoff: .ai/handoffs/a.md" | Out-Null
    $checkpoint = (git -C $worktreeA rev-parse HEAD).Trim()

    Set-Content -LiteralPath (Join-Path $worktreeA 'manual.txt') -Value 'manual'
    git -C $worktreeA add -- manual.txt
    git -C $worktreeA commit -m 'manual follow-up' | Out-Null
    Set-Content -LiteralPath (Join-Path $worktreeA 'a.txt') -Value 'unstaged-a'
    Set-Content -LiteralPath (Join-Path $worktreeA 'untracked.txt') -Value 'untracked'

    Set-Content -LiteralPath (Join-Path $worktreeB 'b.txt') -Value 'task-b'
    git -C $worktreeB add -- b.txt

    $after = @(git -C $worktreeA log --oneline "$checkpoint..HEAD")
    $statusA = @(git -C $worktreeA status --short)
    $statusB = @(git -C $worktreeB status --short)
    $worktrees = @(git -C $resolvedRoot worktree list --porcelain)
    $overlap = @('contract.txt') | Where-Object { @('contract.txt') -contains $_ }

    if ($after.Count -ne 1 -or $after[0] -notmatch 'manual follow-up') {
        throw 'Post-checkpoint manual commit was not discoverable.'
    }
    if (-not ($statusA -match 'a.txt') -or -not ($statusA -match 'untracked.txt')) {
        throw 'Unstaged or untracked late-adoption state was not visible.'
    }
    if (-not ($statusB -match 'b.txt')) {
        throw 'Independent staged state in worktree B was not visible.'
    }
    if (($worktrees -match '^worktree ').Count -ne 3) {
        throw 'Expected base plus two isolated task worktrees.'
    }
    if ($overlap.Count -ne 1) {
        throw 'Shared-contract overlap fixture failed.'
    }

    'GREEN: later commit, dirty state, isolated worktrees, and overlap are detectable'
}
finally {
    foreach ($path in @("$resolvedRoot-a", "$resolvedRoot-b", $resolvedRoot)) {
        if (Test-Path -LiteralPath $path) {
            $resolved = [IO.Path]::GetFullPath($path)
            if (-not $resolved.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing cleanup outside temp: $resolved"
            }
            Remove-Item -LiteralPath $resolved -Recurse -Force
        }
    }
}
```

Expected:

```text
GREEN: later commit, dirty state, isolated worktrees, and overlap are detectable
```

- [ ] **Step 4: Run the official skill validator when available**

Run:

```powershell
python 'C:\Users\peera\.codex\skills\.system\skill-creator\scripts\quick_validate.py' '.agents\skills\agent-checkpoint'
```

Expected:

```text
Validation passes.
```

If it fails only with `ModuleNotFoundError: No module named 'yaml'`, do not
install a dependency. Record the skipped official check and run:

```powershell
$skill = Get-Content -Raw -Encoding UTF8 -LiteralPath '.agents/skills/agent-checkpoint/SKILL.md'
$frontmatter = [regex]::Match($skill, '(?s)\A---\r?\n(.*?)\r?\n---').Groups[1].Value
if ($frontmatter -notmatch '(?m)^name:\s*[a-z0-9-]+\s*$') {
    throw 'Invalid name.'
}
if ($frontmatter -notmatch '(?m)^description:\s*Use when .+$') {
    throw 'Invalid description.'
}
if ($frontmatter.Length -gt 1024) {
    throw 'Frontmatter exceeds 1024 characters.'
}
'Equivalent frontmatter validation passed.'
```

Expected fallback:

```text
Equivalent frontmatter validation passed.
Official validator skipped because PyYAML is unavailable.
```

- [ ] **Step 5: Measure context reduction**

Run:

```powershell
$paths = @(
    'AGENTS.md',
    '.agents/skills/agent-checkpoint/SKILL.md',
    '.agents/skills/agent-checkpoint/references/checkpoint.md',
    '.agents/skills/agent-checkpoint/references/resume.md',
    '.agents/skills/agent-checkpoint/references/parallel.md',
    '.agents/skills/agent-checkpoint/assets/handoff-template.md',
    'README.md'
)
foreach ($path in $paths) {
    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
    [pscustomobject]@{
        Path = $path
        Lines = ($text -split "`r?`n").Count
        Words = ([regex]::Matches($text, '\S+')).Count
        Chars = $text.Length
    }
}
```

Expected:

```text
The checkpoint section in AGENTS.md falls from approximately 503 words to 150-220 words.
SKILL.md falls from approximately 1,239 words to no more than 500 words.
Each operation reads only its selected reference files.
```

- [ ] **Step 6: Run final scope and safety review**

Run:

```powershell
git status --short
git diff --check HEAD~3..HEAD
git diff --name-status 3678583..HEAD
git log -4 --oneline
rg -n "allow_implicit_invocation|late adoption|500 words|one task branch|user-owned|external-owned" AGENTS.md .agents/skills/agent-checkpoint README.md
rg --files .agents/skills/agent-checkpoint -g 'CLAUDE.md' -g '.claude/**' -g '*hook*' -g '*.ps1' -g '*.sh'
```

Expected:

```text
Worktree is clean.
Only the implementation plan, AGENTS.md, agent-checkpoint files, and README.md changed after the design commit.
The scoped file search returns no CLAUDE.md, .claude wrapper, hook, or checkpoint script.
The three planned implementation commits are present; any corrective commit is documented.
```

- [ ] **Step 7: Self-review against the specification**

Confirm:

```text
Explicit-only Codex invocation is enforced.
The router contains hard safety gates but not detailed operation duplication.
Late adoption works without prior skill invocation.
Parallel isolation remains always loaded in AGENTS.md.
Manual and external changes remain protected.
Handoff guidance is bounded and prunes obsolete state.
README documents fresh-thread and manual cross-agent continuation.
No global, model, MCP, reasoning, Claude wrapper, or unrelated changes exist.
```

If a correction is required, edit only the affected approved file, rerun its
targeted contract and the full static contract, inspect the staged diff, and
commit with:

```powershell
$paths = @(
    'AGENTS.md',
    '.agents/skills/agent-checkpoint/SKILL.md',
    '.agents/skills/agent-checkpoint/references/checkpoint.md',
    '.agents/skills/agent-checkpoint/references/resume.md',
    '.agents/skills/agent-checkpoint/references/parallel.md',
    '.agents/skills/agent-checkpoint/agents/openai.yaml',
    '.agents/skills/agent-checkpoint/assets/handoff-template.md',
    'README.md'
)
git add -- $paths
git diff --cached --check
git diff --cached --name-status
git commit -m "fix: align checkpoint context workflow"
```

Do not create an empty final commit when no correction is needed.
