---
name: pond-lean-mode
description: Use when the user explicitly asks for lean, YAGNI, simplest safe solution, minimal implementation, shortest path, do less, avoid over-engineering, avoid new dependencies, or a small pragmatic version first. Applies as an opt-in constraint for the current task only. Do not use to override debugging evidence, security requirements, accessibility basics, data-loss prevention, validation at trust boundaries, explicit user requirements, or required review/reporting workflows.
---

# Lean Mode

Build the simplest correct solution that actually handles the task in front of you.

## Priority

Use this as a constraint, not the primary workflow, when another skill owns the work:

- `$pond-debug-mantra` still owns unresolved failures and root-cause evidence.
- `$pond-php-security` still owns PHP security boundaries and rejection paths.
- `$pond-scrutinize` still owns reviews and verdicts.
- `AGENTS.md`, user instructions, tests, safety rules, and explicit requirements outrank this skill.

## Ladder

Stop at the first rung that safely works:

1. Do nothing if the requested behavior is speculative or already covered.
2. Use existing project code or configuration.
3. Use the standard library.
4. Use a native platform or framework feature.
5. Use an already-installed dependency.
6. Use the smallest local code change.
7. Add a new dependency, abstraction, config surface, or file only when the task genuinely needs it.

If two options are equally small, choose the one with better correctness and maintenance behavior.

## Rules

- Prefer deletion, reuse, and local edits over new layers.
- Do not add a factory, interface, base class, generic helper, feature flag, configuration option, or extension point for a single current use.
- Do not introduce a dependency for behavior that existing code, the platform, or a few clear lines can provide.
- Do not compress code into clever one-liners when it hides business rules, error handling, or security boundaries.
- Keep validation proportional: non-trivial branches, parsers, money/security paths, persistence, and user-visible behavior need a small runnable check when the repo has a testing pattern.
- If the lean solution has a known ceiling that matters later, either state it in the final response or add a `debt:` marker only when leaving a marker is useful for future maintenance.

## Debt Marker

Use this format inside an appropriate source-code comment only for deliberate shortcuts with a real ceiling:

```text
// debt: <what is simplified>; ceiling: <limit>; revisit: <specific trigger>
```

Do not add `debt:` to excuse unsafe behavior, broken correctness, missing authorization, missing validation at a trust boundary, or data-loss risk.

## Output

State the lean choice briefly:

```text
Lean choice: <what was kept simple>. Deferred: <what was not added and the trigger to add it>.
```

Skip that line when it would repeat obvious code changes or conflict with a required `$pond-debug-mantra`, `$pond-scrutinize`, or `$pond-php-security` report.
