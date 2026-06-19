---
name: pond-concise-output
description: Use when the user explicitly asks for concise, terse, short, brief, compact, no long explanation, just the answer, summary only, or minimal prose. Compresses user-facing responses for ordinary work. Do not use to skip required investigation, validation, citations, safety caveats, debug evidence, security findings, review verdicts, or fields required by active skills.
---

# Concise Output

Reduce prose, not rigor.

## Priority

This skill controls presentation only. It does not reduce tool use, code quality, validation, or required reporting.

When combined with other skills:

- Keep `$pond-debug-mantra` evidence, reproduction status, and uncertainty labels.
- Keep `$pond-scrutinize` findings, evidence, suggested changes, and verdict.
- Keep `$pond-php-security` boundaries, controls, checks run, skipped checks, and residual risks.
- Keep citations or source links when browsing was required.

## Response Shape

Use the shortest shape that preserves the answer:

- One sentence for simple facts or confirmations.
- One short paragraph for small code changes.
- Up to five bullets for multi-part summaries.
- Tables only when they make comparison clearer.
- No feature tours, repeated rationale, or generic caveats.

## Required Detail

Do not compress away:

- exact file paths and commands that matter
- failed checks and why they failed
- security, legal, medical, financial, or data-loss caveats
- assumptions that affect correctness
- dates, versions, and source attribution when they are material

If the user asks for detail, provide detail even while keeping sections tight.
