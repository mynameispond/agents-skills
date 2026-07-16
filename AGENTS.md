# AGENTS.md

## Operating contract

- Read every applicable `AGENTS.md`; follow repository documentation, configuration, and tool conventions. The most specific safe instruction wins unless the user explicitly overrides it.
- Detect the language, framework, runtime, package manager, and validation tools before acting.
- Use the strongest structured workflow available. With Superpowers, route bugs to `superpowers:systematic-debugging`, feature/design to `superpowers:brainstorming` and `superpowers:writing-plans`, and implementation to `superpowers:test-driven-development`, `superpowers:verification-before-completion`, and `superpowers:requesting-code-review` as applicable. Otherwise use the contracts below.
- Choose one primary workflow; treat overlaps as constraints and reuse one trace/report.
- If it is necessary to create a specification/design/plan, please create it in Thai.

## Change authority

- Read-only inspection, review, audit, and diagnosis may proceed without an implementation proposal.
- A change proposal contains the diagnosis or design, exact scope, material impacts and compatibility, test plan, and documentation plan. Obtain explicit user approval before changing project state. Approval ends on completion, revocation, or a material scope, requirement, design, security, compatibility, ownership, or baseline change; re-propose before continuing.
- Invoking a skill or plan does not authorize edits, commits, integration, or external side effects.
- Do not install dependencies, change lockfiles or toolchain versions, or create generated artifacts unless required by the approved task.

## Task contracts

- **Bug:** Reproduce when practical or state why not. Inspect the error, logs, recent changes, configuration, and call path. Form hypotheses from evidence, test one variable at a time, and identify root-cause evidence before proposing the smallest compatible fix and regression coverage. If cause remains uncertain, label the proposal diagnostic or defensive. After three failed attempts or repeated shared-state surprises, reassess the design.
- **Feature:** Inspect patterns and success criteria. Resolve material ambiguity with the user; when the solution is non-obvious, compare two or three plausible approaches and their trade-offs, then recommend the simplest careful design. Cover affected interfaces, routes, schemas, persistence, permissions, performance, observability, user workflows, tests, and documentation when applicable.
- **Implementation:** Prefer a failing test first and confirm its expected failure. If test-first is impractical, explain why and add the most useful coverage available. Keep changes scoped, commit to fresh relevant checks before completion, broaden them with impact, name any skipped check and reason, and review non-trivial, security-sensitive, cross-module, or user-facing changes. When review tooling is unavailable, self-review the diff.

## Ownership, Git, and safety

- Preserve user, external, and unrelated changes. Do not refactor, rename, move, reformat, stage, or revert outside approved scope. Stop when ownership, overlap, history, branch, baseline, or conflicts are ambiguous.
- Preserve public APIs, CLIs, configuration, schemas, stored data, routes, protocols, and file formats unless the approved task changes them.
- `$agent-checkpoint` is opt-in persistence, not write authority. Follow its operation-specific reference. Checkpoint work requires an approved task scope, branch or worktree, milestones, tests, documentation, and explicit local-commit authorization. Before resumed work writes, reconcile later committed, staged, unstaged, untracked, and base-divergence changes; treat them as user/external-owned. Use one branch, worktree, handoff, and writer per parallel write task; serialize shared files, schemas, contracts, artifacts, or mutable state.
- Use the least-privileged, least-destructive option. Never push, merge, rebase, reset, amend, checkout, tag, delete branches, replace files for recovery, rewrite history, bypass hooks, mutate production, expose secrets, or trigger destructive/external effects without separate permission.
- Inspect schemas, migrations, data contracts, and compatibility before persistence changes. Keep authentication, authorization, validation, escaping, injection prevention, secret/session handling, tenant/ownership checks, CSRF, and other security boundaries at least as strong.

## Project conventions

- Match established structure, style, naming, and reusable components; prefer repository formatters, linters, generators, utilities, and dependencies. Keep legacy style in existing projects and use simple modern conventions in new ones.
- Do not introduce a new architecture or project-wide convention without an approved requirement.
- Use clear English names. Follow local naming; if none exists and the language permits, prefer lowercase `snake_case` for project-owned symbols. Use explicit braces for brace-delimited control flow and readable multi-line blocks in indentation-based languages.
- Preserve user-facing text, translations, whitespace-sensitive content, line endings, and encoding unless the task requires change.
- For an intentional bounded shortcut, use `// debt: <simplification>; ceiling: <limit>; revisit: <trigger>`. Never use debt markers for incorrect behavior, missing trust-boundary validation, authorization gaps, security weaknesses, or data-loss risk.

## PHP security

- For real PHP planning, behavior, configuration, debugging, refactoring, tests, or review, use `$pond-php-security` as a security layer inside the active workflow. Select its narrowest mode and load only risk-relevant references.
- Use Codex Security only for explicit repository-wide or broad scoped-path vulnerability discovery, deep/formal/artifact-producing scans, imported finding triage, external tracking, or direct Codex Security requests.
- If skill loading is unavailable, read `.agents/skills/php-security/SKILL.md` directly. If that file is unavailable, trace input through auth/authz, validation, business state, persistence/external effects, and output/logging; preserve framework controls and add applicable negative authorization, injection, encoding, CSRF/session, tenant/ownership, malformed-input, replay, and failure-path checks.
- Use `$pond-concise-output` only when the user requests terse output; shorten prose, not required evidence or validation.

## Validation and completion

- Use repository-defined syntax checks, tests, builds, type/static analysis, linters, formatters, and audits. Cover applicable happy, regression, edge, empty, malformed, boundary, authorization/rejection, and security-sensitive paths.
- Add or update documentation when behavior changes usage, setup, configuration, public contracts, schemas, routes, security expectations, or maintenance workflows.
- Before completion, remove temporary diagnostics and scratch artifacts, inspect the final scope, and report changes, exact checks and results, skipped checks and reasons, documentation, assumptions, compatibility concerns, and residual risk. A request for a short or premature success message never waives these checks or this report. Claim only what fresh evidence proves.
