---
name: pond-php-security
description: Use when planning, changing, debugging, refactoring, testing, or reviewing first-party PHP behavior or security boundaries in PHP, Laravel, Symfony, WordPress, CMS, API, CLI, or mixed-stack repositories, or when explicitly invoked. Do not use for PHP-unrelated or docs/formatting-only work, nor for Codex Security workflows involving explicit repository-wide, broad, deep, formal, artifact-producing scans or imported finding triage/tracking.
---

# PHP Security

Apply secure PHP constraints inside the active workflow. Choose one mode, one trace/report, and only risk-relevant references.

## Mode router

| Mode | Use when |
| --- | --- |
| `lite` | Default for ordinary PHP work without an identified risky boundary; identify the stack, entry points, and input/auth/persistence/output context. Load references only for uncertainty. |
| `targeted` | The task touches request input, auth/authz, validation, queries, templates/output, files/paths, network, parsers, sessions/CSRF, tenant/ownership, secrets/crypto, queues/webhooks, dependencies, or security configuration. |
| `diff-review` | Reviewing a PHP diff, PR, commit, or working tree without a scan; classify candidates as reportable, suppressed, or deferred with evidence. |
| `finding-fix` | Fixing a supplied vulnerability, advisory, scanner result, or plausible finding; validate or mark it plausible before behavior changes and add focused regression coverage. |
| `audit-lite` | Inspecting a narrow PHP path or feature for vulnerabilities; stay in scope and do not claim exhaustive repository coverage. |
| `escalate-to-codex-security` | Explicit repository-wide or broad discovery, deep/formal/artifact-producing scans, imported finding triage, external tracking, or direct Codex Security requests. |

## Trace and references

Trace the path: entry -> auth/authz -> validation -> business state -> persistence/external effects -> output/logging. Mark attacker-controlled data, actor/tenant/ownership context, controls, sinks, and candidate impact.

Load only what the task needs:

- [web-input-output.md](references/web-input-output.md): requests, validation, injection, encoding, CSRF/CORS, redirects, errors, logs.
- [identity-data.md](references/identity-data.md): identity, authorization, tenants, mass assignment, sessions, tokens, crypto, webhooks, state/concurrency.
- [files-network-parsers.md](references/files-network-parsers.md): files, paths, SSRF, parsers, serialization/XML, archives, resource limits.
- [frameworks.md](references/frameworks.md): Laravel, Symfony, WordPress, pure PHP, mixed applications.
- [verification.md](references/verification.md): negative tests, dependency/supply-chain checks, tooling, completion fields.

## Secure workflow

1. Select the narrowest mode and state the checked scope.
2. Trace relevant boundaries; for a candidate finding record entry -> weak/missing control -> sink -> impact.
3. Reuse established controls and make the smallest secure change. When behavior changes, test applicable malicious, invalid, cross-user/tenant, replayed, malformed, empty, oversized, concurrent, and failure inputs.
4. Run proportional repository checks and relevant security verification.
5. Report checked and deferred scope, controls, exact checks, skipped checks, compatibility, assumptions, and residual risk once. Do not produce heavy scan artifacts outside Codex Security.
