# AGENTS.md

## Operating contract

- Read every applicable `AGENTS.md`; follow repository documentation, configuration, and tool conventions. The most specific safe instruction wins unless the user explicitly overrides it.
- Identify the stack and repository validation tools relevant to the task.
- Choose one primary workflow proportional to scope and risk. With Superpowers, use debugging for bugs, brainstorming for design, writing-plans for work needing a written plan, and TDD, verification, and review for applicable implementation work. Otherwise use the contracts below. Load only relevant skills/references and reuse one report.
- For a small, clear change, keep the proposal in chat and checks focused. Use written plans for complex or multi-part work and deeper review for security, persistence, or public-contract changes. Write necessary specifications/designs/plans in Thai.

## Change authority

- Read-only inspection, review, audit, and diagnosis may proceed without an implementation proposal.
- Before changing project state, propose the diagnosis/design, scope, material impacts, checks, and documentation needs; obtain explicit user approval. A short proposal suffices for a small change. Continue within that approval without asking again. Approval ends on completion, revocation, or a material change to scope, requirements, design, security, compatibility, ownership, or baseline; re-propose then.
- Invoking a skill or plan does not authorize edits, commits, integration, or external side effects.
- Do not install dependencies, change lockfiles or toolchain versions, or create generated artifacts unless required by the approved task.

## Task contracts

- **Bug:** Reproduce or explain why not. Inspect relevant errors, logs, changes, configuration, and call paths. Test evidence-based hypotheses one variable at a time; establish root cause before proposing the smallest compatible fix and regression coverage. Label uncertain fixes diagnostic or defensive. Reassess after three failed attempts or repeated shared-state surprises.
- **Feature:** Inspect patterns and success criteria. Resolve material ambiguity; compare alternatives when the solution is non-obvious and recommend the simplest careful design. Cover affected contracts, persistence, permissions, performance, observability, user workflows, tests, and documentation.
- **Implementation:** Prefer a failing test first; confirm the expected failure. If impractical, explain and use meaningful coverage. Run fresh relevant checks, broadening with impact. Review non-trivial, security-sensitive, cross-module, or user-facing changes; self-review the diff when review tooling is unavailable.

## Ownership, Git, and safety

- Preserve user, external, and unrelated changes. Do not refactor, rename, move, reformat, stage, or revert outside approved scope. Stop when ownership, overlap, history, branch, baseline, or conflicts are ambiguous.
- Preserve public APIs, CLIs, configuration, schemas, stored data, routes, protocols, and file formats unless the approved task changes them.
- `$agent-checkpoint` is opt-in persistence; its skill defines checkpoint authorization and operations. Before resumed work writes, reconcile later committed, staged, unstaged, untracked, and base-divergence changes as user/external-owned. Use one branch, worktree, handoff, and writer per parallel write task; serialize shared files, schemas, contracts, artifacts, or mutable state.
- Use the least-privileged, least-destructive option. Never push, merge, rebase, reset, amend, checkout, tag, delete branches, replace files for recovery, rewrite history, bypass hooks, mutate production, expose secrets, or trigger destructive/external effects without separate permission.
- Inspect schemas, migrations, data contracts, and compatibility before persistence changes. Keep authentication, authorization, validation, escaping, injection prevention, secret/session handling, tenant/ownership checks, CSRF, and other security boundaries at least as strong.

## Project conventions

- Match established structure, style, naming, and components; prefer repository tooling and dependencies. Preserve legacy style; use simple modern conventions in new projects.
- Do not introduce a new architecture or project-wide convention without an approved requirement.
- Use clear English names. Follow local naming; if none exists and the language permits, prefer lowercase `snake_case` for project-owned symbols. Use explicit braces for brace-delimited control flow and readable multi-line blocks in indentation-based languages.
- Preserve user-facing text, translations, whitespace-sensitive content, line endings, and encoding unless the task requires change.
- For an intentional bounded shortcut, use `// debt: <simplification>; ceiling: <limit>; revisit: <trigger>`. Never use debt markers for incorrect behavior, missing trust-boundary validation, authorization gaps, security weaknesses, or data-loss risk.

## PHP security

- For real PHP planning, behavior, configuration, debugging, refactoring, tests, or review, use `$pond-php-security` as a security layer inside the active workflow. Select its narrowest mode and load only risk-relevant references.
- Use Codex Security only for explicit repository-wide or broad scoped-path vulnerability discovery, deep/formal/artifact-producing scans, imported finding triage, external tracking, or direct Codex Security requests.
- If skill loading is unavailable, read `.agents/skills/pond-php-security/SKILL.md`. If the file is unavailable, trace relevant input through auth/authz, validation, business state, persistence/external effects, and output/logging. Preserve framework controls; verify applicable authorization, injection/encoding, CSRF/session, tenant/ownership, malformed-input, replay, and failure paths. Do not claim review beyond inspected evidence.

## Validation and completion

- Select repository-defined syntax, test, build, static-analysis, lint, format, and audit checks relevant to the change. Cover applicable happy, regression, edge, malformed, boundary, and authorization/rejection paths.
- Update documentation when usage, setup, contracts, security expectations, or maintenance workflows change.
- Remove your temporary diagnostics and scratch artifacts; inspect the final scope. Report the result, exact checks/outcomes, and required checks skipped with reasons. Include documentation changes, material assumptions, compatibility concerns, and residual risks when present; omit empty sections. Claim only what fresh evidence proves.
- When the user requests brevity, shorten prose while preserving findings, verification evidence, and material limitations. This does not waive investigation or validation.
