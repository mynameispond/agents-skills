# AGENTS.md

## Instruction scope

- Read and follow every applicable `AGENTS.md`, including more specific files in nested directories.
- Follow repository documentation, configuration, toolchain settings, and established project conventions.
- When instructions conflict, prefer the more specific repository or directory-level instruction unless it is unsafe or the user explicitly overrides it.
- Do not assume a programming language, framework, runtime, package manager, or test tool. Detect them from the repository before acting.

## Skill delegation

- Use `$pond-debug-mantra` as the primary workflow for unresolved bugs, errors, exceptions, failing tests, intermittent failures, or incorrect runtime behavior.
- Use `$pond-scrutinize` for reviewing a plan, PR, diff, design, or proposed code change.
- Use `$pond-php-security` for activated PHP work; keep it active as a security constraint when another workflow is primary.
- Use `$pond-lean-mode` only when explicitly requested for lean, YAGNI, simplest safe solution, minimal implementation, shortest path, or over-engineering reduction.
- Use `$pond-concise-output` only when explicitly requested for terse, brief, compact, or summary-only responses.
- Use `$pond-debt-ledger` when asked to collect, audit, list, or write deliberate `debt:` markers.
- Use `$pond-skill-help` when asked what skills are available or how to invoke them.
- For a patch intended to fix a bug, gather debugging evidence first; use `$pond-scrutinize` for final review when the patch is non-trivial, security-sensitive, cross-module, user-facing, or explicitly requested.
- When multiple skills apply, choose one primary workflow, treat the others as constraints or checklists, and do not duplicate trace or report sections. `$pond-lean-mode` and `$pond-concise-output` never replace debugging evidence, security controls, required validation, or review verdicts.
- Do not duplicate the full debugging or review workflows in this file.

## Project conventions

- Match the existing project structure, formatting, language idioms, and reusable components unless a rule in this file explicitly requires otherwise.
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
- For inspection-only work, reviews, audits, investigations, status checks, or read-only exploration, proceed directly without requiring an implementation plan.
- Before making code, file, configuration, dependency, generated artifact, or other state changes, present a concise implementation plan and obtain the user's explicit review and approval.

## Safety boundaries

- Do not run destructive commands, mutate production data, change production configuration, expose secrets, or trigger external side effects without explicit permission.
- Do not weaken authentication, authorization, validation, escaping, secret handling, permission checks, or other existing security boundaries.
- Use the least-privileged and least-destructive option available.
- When changing persistence behavior, inspect the current schema, migrations, data contracts, and compatibility requirements first.
- Do not install dependencies, modify lockfiles, or change toolchain versions unless required by the task or explicitly approved.

## Validation

- Use repository-provided tests, build commands, type checks, static analysis, linters, formatters, and validation scripts when available.
- Run checks relevant to the changed area and broaden validation when the change has wider impact.
- Add or update tests when behavior changes and the repository has an established testing pattern.
- If a relevant check cannot be run, state which check was skipped and why.

## Cleanup and completion

- Remove temporary diagnostics, generated scratch files, one-off scripts, and debug instrumentation before finishing unless the user explicitly asks to keep them.
- Ensure the final change set contains only intended files and modifications.
- In the final response, summarize what changed, what was validated, and any remaining risks, assumptions, or unverified behavior.
- If `$pond-scrutinize` was used to review the change, include its required findings and verdict once in the final summary; do not suppress them or repeat a duplicate block.
