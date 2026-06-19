---
name: pond-debt-ledger
description: Use when the user asks to list, audit, collect, summarize, or write a ledger of deliberate shortcuts, deferred work, debt markers, `debt:` comments, pond-lean-mode deferrals, or known ceilings in the repository. Reads and reports by default; writes a ledger file only when explicitly requested.
---

# Debt Ledger

Collect deliberate shortcut markers so a lean decision has a visible ceiling and revisit trigger.

## Marker Convention

Supported marker:

```text
// debt: <what is simplified>; ceiling: <limit>; revisit: <specific trigger>
```

Allowed comment prefixes depend on the language, for example `//`, `#`, `/*`, `<!--`, `--`, or `;`.

Use a marker only for a deliberate simplification with a known future trigger. Do not use it to normalize broken behavior, security gaps, missing validation, missing authorization, or data-loss risk.

## Scan

Search the repository for debt markers while skipping dependencies, generated output, caches, and VCS directories.

Prefer `rg`:

```powershell
rg -n --hidden --glob '!vendor/**' --glob '!node_modules/**' --glob '!dist/**' --glob '!build/**' --glob '!coverage/**' --glob '!.git/**' "(#|//|/\*|<!--|--|;)\s*debt:" .
```

If `rg` is unavailable, use the fastest local alternative.

## Report

Group results by file:

```text
<file>:<line> - <what is simplified>. ceiling: <limit>. revisit: <trigger>.
```

Flag markers that do not include both `ceiling:` and `revisit:` as `no-trigger`.

End with:

```text
<N> markers, <M> no-trigger.
```

If no markers exist, report `No debt markers found.`

## Writes

Do not create or update a ledger file unless the user asks for one. If asked, write the report to the requested path or default to `DEBT.md`.
