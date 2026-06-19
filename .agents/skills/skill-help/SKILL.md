---
name: pond-skill-help
description: Use when the user asks what skills are available, how to invoke local skills, which skill to use, skill help, commands, modes, or a quick reference for this repository's Codex skills. One-shot display only; do not change modes, edit files, or run workflows.
---

# Skill Help

Display a compact reference for the local skill set. Do not activate another skill, change mode, or edit files unless the user asks.

## Skills

| Skill | Use For |
| --- | --- |
| `$pond-debug-mantra` | Debugging unresolved bugs, failures, exceptions, failing tests, intermittent behavior, and root-cause investigation. |
| `$pond-scrutinize` | Reviewing plans, PRs, diffs, designs, and proposed code changes with findings and a ship verdict. |
| `$pond-php-security` | PHP, Laravel, Symfony, WordPress, or mixed PHP work where security boundaries matter. |
| `$pond-lean-mode` | Opt-in lean/YAGNI implementation: simplest safe solution, stdlib/native first, no speculative abstractions. |
| `$pond-concise-output` | Opt-in terse responses for ordinary work without dropping required evidence or safety details. |
| `$pond-debt-ledger` | List or write a ledger of `debt:` markers and pond-lean-mode deferrals. |
| `$pond-skill-help` | Show this reference. |

## Composition

- Use one primary workflow for the task.
- Treat `$pond-lean-mode` and `$pond-concise-output` as constraints, never as replacements for debugging, security, or review requirements.
- Use `$pond-php-security` alongside `$pond-debug-mantra` or `$pond-scrutinize` when the affected path is PHP and security-relevant.
- Use `$pond-debt-ledger` as a read-only report unless the user explicitly asks to write a ledger file.

## Debt Marker

```text
// debt: <what is simplified>; ceiling: <limit>; revisit: <specific trigger>
```

Use only for deliberate, acceptable shortcuts with a real revisit trigger.
