---
name: pond-php-security
description: Secure-by-default PHP planning, implementation, debugging, refactoring, and review guardrails for first-party PHP code and PHP application configuration, runtime behavior, dependencies, and tests across pure PHP, Laravel, Symfony, WordPress, CMS, API, CLI, and mixed-stack repositories. Use when explicitly invoked as $pond-php-security, when the user identifies the target as PHP, or when the task touches real PHP behavior or security boundaries. Do not use for PHP-unrelated work or docs/formatting-only changes with no behavior or security impact. For explicit full-system, repository-wide, deep, formal security scans, imported finding triage, tracking, or Codex Security requests, prefer Codex Security if available.
---

# PHP Security

Write PHP code to remain safe under malicious, malformed, duplicated, oversized, concurrent, expired, replayed, and unexpected input.

## Coordination
- Apply this skill to every real PHP planning, coding, debugging, refactoring, and review task.
- Treat this skill as the PHP security layer inside the active workflow. It does not replace debugging, planning, TDD, verification, or code review workflows.
- Keep token use bounded: choose one mode, reuse one trace, and load only the references needed for the selected risk.
- Escalate to Codex Security only when the user asks for full-system, repository-wide, deep, formal, or artifact-producing security scans, imported finding triage, tracking, or the Codex Security workflow by name.

## Mode Router
Choose the narrowest mode that matches the task:

- **lite**: Default for ordinary PHP planning, implementation, debugging, refactoring, and review. Identify the stack and touched entry points, note input/auth/persistence/output boundaries, and do not load references unless risk or uncertainty requires them.
- **targeted**: Use when touching request input, auth/authz, validation, database queries, templates/output, files/uploads/paths, network calls, parsers/deserialization/XML, sessions/CSRF, tenant/ownership checks, secrets/crypto, queues/webhooks, dependency security, or security configuration. Load only the relevant threat/framework references.
- **diff-review**: Use when asked to review PHP diffs, PRs, commits, or working-tree changes without a formal Codex Security scan. Classify security candidates as reportable, suppressed, or deferred with concise evidence.
- **finding-fix**: Use when the user supplies a PHP vulnerability, advisory, scanner result, or plausible security finding to fix. Validate or mark the risk as plausible before changing behavior, then add focused regression coverage.
- **audit-lite**: Use when asked to inspect a PHP path, feature, route, module, or small scope for vulnerabilities without a formal full-system scan. Stay within the requested scope and do not claim exhaustive repository coverage.
- **escalate-to-codex-security**: Use Codex Security instead when the user asks to find vulnerabilities across the whole system, scan a repository or broad scope, run a deep/formal security scan, produce scan artifacts, triage imported findings at backlog scale, or track findings externally.

## Context Gathering
Before editing, scale context to risk:
1. Inspect `composer.json`, `composer.lock`, and security configs only when the task or selected mode makes them relevant.
2. Trace the in-scope path: Entry point -> Auth/Authz -> Validation -> Business logic -> Persistence -> Output/Logging.
3. Identify trust boundaries and attacker-controlled values.
4. For review, finding-fix, and audit-lite modes, keep a compact candidate lifecycle: candidate -> validated/reportable, suppressed, or deferred.

## Threat-Specific References
Load only the references relevant to the task (do not preload unselected references):
- **Web Input/Output**: [web-input-output.md](references/web-input-output.md) (validation, XSS, CSRF, CORS, SQL/command injection, headers, logging, errors).
- **Identity & Data**: [identity-data.md](references/identity-data.md) (auth, roles, tenant isolation/IDOR, mass assignment, sessions, crypto, webhooks, state integrity).
- **Files & Network**: [files-network-parsers.md](references/files-network-parsers.md) (uploads, path traversal, SSRF, serialization/XML, parser/resource limits).
- **Frameworks**: [frameworks.md](references/frameworks.md) (Laravel, Symfony, WordPress, Pure PHP).
- **Verification**: [verification.md](references/verification.md) (security tests, dependency audit, completion report contract).

## Secure Workflow
1. Select the mode and keep the scope explicit.
2. Map trust boundaries and relevant attack vectors for the in-scope PHP path.
3. Load relevant threat/framework references only when the selected mode or risk requires them.
4. For candidate findings, record the mini attack path: entry point -> missing or weak control -> sink/broken control -> impact.
5. Reuse existing security controls; make the smallest secure change.
6. Add focused negative/rejection tests for malicious, invalid, cross-user, cross-tenant, replayed, malformed, or boundary inputs when behavior changes.
7. Verify via repository tools and security checks proportionate to the selected mode (see [verification.md](references/verification.md)).
8. Report security reasoning once in the active final response or review, including checked scope, skipped/deferred areas, checks run, and residual risk. Do not generate heavy scan artifacts from this skill.
