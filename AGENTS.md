# AGENTS.md

## Instruction scope

- Read and follow every applicable `AGENTS.md`, including more specific files in nested directories.
- Follow repository documentation, configuration, toolchain settings, and established project conventions.
- When instructions conflict, prefer the more specific repository or directory-level instruction unless it is unsafe or the user explicitly overrides it.
- Do not assume a programming language, framework, runtime, package manager, or test tool. Detect them from the repository before acting.

## Workflow routing

- Use the best structured workflow support available in the current AI environment.
- When Superpowers is available in the current environment, prefer:
  - `superpowers:systematic-debugging` for unresolved bugs, errors, exceptions, failing tests, intermittent failures, or incorrect runtime behavior.
  - `superpowers:brainstorming` and `superpowers:writing-plans` for new features, behavior changes, and multi-step implementation plans.
  - `superpowers:test-driven-development`, `superpowers:verification-before-completion`, and `superpowers:requesting-code-review` for implementation quality gates.
- If Superpowers or equivalent workflow tooling is unavailable, follow the fallback workflows in this file directly.
- Use `$pond-php-security` for activated PHP work when local skills are available. If local skills are unavailable, apply the PHP security section in this file as the minimum security policy.
- Use `$pond-concise-output` only when explicitly requested for terse, brief, compact, or summary-only responses. If local skills are unavailable, keep the response concise without dropping required evidence, validation, or caveats.
- When multiple workflows apply, choose one primary workflow and treat the others as constraints or checklists. Do not duplicate trace, review, validation, or report sections.
- Do not duplicate the full debugging, planning, security, testing, or review workflows in this file.

## Approval gate

- Before changing code, files, configuration, dependencies, generated artifacts, or other project state, present the relevant diagnosis, approach, impact analysis, test plan, and documentation plan, then obtain the user's explicit approval.
- Inspection-only work, reviews, audits, investigations, status checks, and read-only exploration may proceed without an implementation plan.

## Checkpoint and handoff policy

- Invoking `$agent-checkpoint`, a skill, or a plan never grants permission to edit or commit. A proposal must identify the task, scope, task branch or worktree, checkpoint milestones, tests, documentation, and explicitly authorize local checkpoint commits. Authorization ends on completion, revocation, or any material scope, requirement, design, security, or compatibility change.
- Checkpoints require a dedicated task branch. Before each commit, inspect the worktree, exclude unrelated or external-owned changes, run fresh relevant checks, and inspect the staged diff. Authorization never permits push, merge, rebase, reset, tags, branch deletion, history rewriting, hook bypass, dependency installation, production changes, secrets, or unresolved conflicts.
- Before a resumed or replacement agent writes, reconcile the latest task checkpoint with later commits, staged, unstaged, untracked, and base-divergence changes. Treat every later change as user-owned or external-owned. Preserve non-overlapping changes; obtain baseline approval for overlap; obtain a revised proposal when behavior or scope changed.
- Parallel write tasks require one task branch, worktree, handoff, and writer per task. Serialize tasks sharing files, schemas, public contracts, generated artifacts, or mutable state. Base synchronization and branch integration require separate approval.
- Stop when the checkpoint, history, ownership, baseline, or scope is ambiguous. Never force recovery with checkout, reset, amend, rebase, or file replacement.

## Bug workflow

- Follow the active debugging workflow before proposing production changes. If no dedicated debugging workflow is available, use this fallback.
- Establish reproduction when practical, or state why reproduction is not available.
- Inspect the reported error, logs, stack trace, recent changes, configuration, and relevant call path.
- Form a specific hypothesis only after inspecting evidence. Test one variable at a time and update the hypothesis when results contradict it.
- Identify root-cause evidence before proposing a production fix. If the cause is still uncertain, label the proposal as defensive or diagnostic rather than confirmed.
- If three fix attempts fail or each attempt exposes a different shared-state, coupling, or design problem, stop and reassess the underlying approach before trying another fix.
- The proposal must include root-cause evidence, affected areas, the smallest behavior-preserving fix, compatibility considerations, and regression coverage.

## Feature workflow

- Follow the active design and planning workflows before implementation. If no dedicated design or planning workflow is available, use this fallback.
- Inspect the existing project context, patterns, constraints, affected surfaces, and success criteria.
- Ask clarifying questions when requirements, success criteria, security boundaries, or compatibility expectations are unclear.
- Compare 2-3 plausible approaches when the solution is not obvious. State the recommended approach and the trade-offs.
- Prefer existing project patterns, utilities, framework features, and dependencies before adding new abstractions or packages.
- The proposal must favor the simplest careful design and cover affected public APIs, routes, schemas, persistence, permissions, performance, observability, existing user workflows, tests, and documentation.

## Implementation quality gates

- Prefer test-first implementation for bug fixes, features, refactors, and behavior changes. When practical, write or identify the failing test before implementation and confirm it fails for the expected reason.
- If test-first is impractical, state why and still add the most useful regression or coverage available.
- Before claiming work is complete, run fresh verification commands that prove the claim, read their output, and report failures or skipped checks accurately.
- For non-trivial, security-sensitive, cross-module, or user-facing changes, perform a code review. If no review tool or subagent is available, self-review the diff against requirements, affected paths, security boundaries, tests, documentation, backward compatibility, and unintended scope changes.

## Project conventions

- Match the existing project structure, formatting, language idioms, and reusable components unless a rule in this file explicitly requires otherwise.
- For an existing or legacy project, follow the project's established style and patterns even when a newer style is available, unless the task explicitly requires modernization.
- For a new project, use modern, maintainable conventions appropriate to the chosen stack, while keeping the design simple and avoiding unnecessary abstractions or dependencies.
- Prefer repository-provided formatters, linters, generators, and scripts over manual conventions.
- Prefer existing utilities and dependencies before adding new abstractions or packages.
- Keep existing symbols, public interfaces, and file organization stable unless the task requires changing them.
- Use clear, descriptive English names and avoid unnecessary abbreviations.
- Follow the repository's established naming style. If no style is detectable and the language permits it, prefer lowercase `snake_case` for newly introduced project-owned variables, functions, and methods. Preserve names required by the language, framework, external API, generated code, or an existing public contract.
- For application code in languages that support brace-delimited control blocks, use explicit braces for conditionals, loops, switches or matches, exception handling, and similar control structures, including single-statement bodies. Template files and framework-specific syntax may follow local conventions.
- For indentation-based languages, use clear multi-line control blocks and avoid compressed one-line control flow when it reduces readability or hides scope.
- Preserve user-facing text, translations, whitespace-sensitive content, line endings, and encoding unless the task requires a change.
- Do not introduce a new architecture, dependency, or project-wide convention without a clear task requirement or explicit approval.
- For deliberate shortcuts with a known ceiling, prefer a source-code comment marker such as `// debt: <what is simplified>; ceiling: <limit>; revisit: <specific trigger>`. Do not use debt markers to excuse broken correctness, missing validation at trust boundaries, missing authorization, security gaps, or data-loss risk.

## Change scope

- Make only changes required by the task.
- Do not refactor, rename, reformat, move, or restructure unrelated code.
- Preserve backward compatibility for public APIs, command-line interfaces, configuration, schemas, stored data, routes, protocols, and file or wire formats unless the requested change explicitly alters them.
- Do not overwrite or revert unrelated user changes. Leave unexpected modifications untouched and report them when relevant.

## Safety boundaries

- Do not run destructive commands, mutate production data, change production configuration, expose secrets, or trigger external side effects without explicit permission.
- Do not weaken authentication, authorization, validation, escaping, secret handling, permission checks, or other existing security boundaries.
- Use the least-privileged and least-destructive option available.
- When changing persistence behavior, inspect the current schema, migrations, data contracts, and compatibility requirements first.
- Do not install dependencies, modify lockfiles, or change toolchain versions unless required by the task or explicitly approved.

## PHP security

- Treat PHP security as a first-class concern for PHP, Laravel, Symfony, WordPress, CMS, API, CLI, and mixed PHP work.
- Keep `$pond-php-security` separate from the primary workflow: it adds security checks and constraints but does not replace debugging, planning, TDD, verification, or review.
- Do not weaken authentication, authorization, validation, escaping, secret handling, session safety, tenant or ownership checks, CSRF protection, injection prevention, or other security boundaries.
- Use the PHP security skill for detailed PHP threat modeling, implementation rules, negative tests, verification, and completion reporting.

## Validation

- Use repository-provided tests, build commands, type checks, static analysis, linters, formatters, and validation scripts when available.
- Run checks relevant to the changed area and broaden validation when the change has wider impact.
- Add or update tests when behavior changes and the repository has an established or practical testing pattern.
- Test coverage should include the relevant happy paths, regression cases, edge cases, invalid or malformed input, empty and boundary values, authorization or rejection paths, and security-sensitive failure modes.
- For PHP work, include tests or checks for applicable authentication, authorization, validation, injection prevention, output encoding, CSRF/session behavior, tenant or ownership boundaries, and error-handling paths.
- Before handing work to the user for review, run the most relevant targeted checks and any broader checks needed for confidence in the affected surface.
- If a relevant check cannot be run, state which check was skipped and why.

## Documentation

- Add or update documentation for new or changed behavior when it affects usage, setup, configuration, public APIs, commands, schemas, routes, security expectations, or maintenance workflows.
- Prefer the repository's existing documentation style and location, such as README sections, docs pages, inline docblocks, examples, changelog entries, or test documentation.
- Documentation should explain the behavior, important constraints, security assumptions, and how to verify or use the changed code. Keep it proportional to the size and risk of the change.

## Cleanup and completion

- Remove temporary diagnostics, generated scratch files, one-off scripts, and debug instrumentation before finishing unless the user explicitly asks to keep them.
- Ensure the final change set contains only intended files and modifications.
- In the final response, summarize what changed, what was validated, what documentation was added or updated, and any remaining risks, assumptions, or unverified behavior.
