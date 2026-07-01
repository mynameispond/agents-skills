---
name: pond-php-security
description: Secure-by-default guardrails for creating, modifying, debugging, and reviewing PHP applications across pure PHP, Laravel, Symfony, WordPress, CMS, API, CLI, and mixed-stack repositories. Use when explicitly invoked as $pond-php-security, when the user identifies the target as PHP, or when the task touches first-party PHP code, configuration, runtime behavior, dependencies, tests, or review/debug paths in a target with PHP indicators.
---

# PHP Security

Write PHP code to remain safe under malicious, malformed, duplicated, oversized, concurrent, expired, replayed, and unexpected input.

## Coordination
- Apply this skill to all PHP changes.
- Reuse one trace across active workflows. Do not repeat identical logic paths across sections.

## Context Gathering
Before editing, scale context to risk:
1. Inspect `composer.json`, `composer.lock`, and security configs.
2. Trace path: Entry point -> Auth/Authz -> Validation -> Business logic -> Persistence -> Output/Logging.
3. Identify trust boundaries and attacker-controlled values.

## Threat-Specific References
Load only the references relevant to the task (do not preload unselected references):
- **Web Input/Output**: [web-input-output.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/web-input-output.md) (validation, XSS, CSRF, CORS, SQL/command injection, headers, logging, errors).
- **Identity & Data**: [identity-data.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/identity-data.md) (auth, roles, tenant isolation/IDOR, mass assignment, sessions, crypto, webhooks, state integrity).
- **Files & Network**: [files-network-parsers.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/files-network-parsers.md) (uploads, path traversal, SSRF, serialization/XML, parser/resource limits).
- **Frameworks**: [frameworks.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/frameworks.md) (Laravel, Symfony, WordPress, Pure PHP).
- **Verification**: [verification.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/verification.md) (security tests, dependency audit, completion report contract).

## Secure Workflow
1. Map trust boundaries and identify attack vectors.
2. Load relevant threat/framework references above.
3. Reuse existing security controls; make the smallest secure change.
4. Add negative/rejection tests for malicious/invalid inputs.
5. Verify via repository tools and security checks (see [verification.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/references/verification.md)).
6. Report findings using the completion format in `verification.md`.