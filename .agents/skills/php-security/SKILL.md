---
name: pond-php-security
description: Secure-by-default guardrails for creating, modifying, debugging, and reviewing PHP applications across pure PHP, Laravel, Symfony, WordPress, CMS, API, CLI, and mixed-stack repositories. Use when explicitly invoked as $pond-php-security, when the user identifies the target as PHP, or when the task touches first-party PHP code, configuration, runtime behavior, dependencies, tests, or review/debug paths in a target with PHP indicators such as composer.json with PHP requirements, project-owned .php entry points, artisan, bin/console, wp-config.php, or public/index.php. Keep active throughout that PHP work. Do not activate solely for PHP found under vendor, caches, generated output, fixtures, examples, backups, or unrelated files in the same repository.
---

# PHP Security

Write PHP code to remain safe under malicious, malformed, duplicated, oversized, concurrent, expired, replayed, and unexpected input, not only the happy path.

This skill defines PHP security policy for PHP implementation, modification, debugging, and review work.

## Activation

Activate when any condition is true:

1. The user invokes `$pond-php-security`.
2. The user identifies the target as PHP, Laravel, Symfony, WordPress, or another PHP system.
3. The task touches PHP code, configuration, runtime behavior, dependencies, tests, or a review/debug path in a target root with first-party PHP indicators:
   - `composer.json` requiring PHP or PHP packages
   - project-owned `.php` entry points
   - `artisan`
   - `bin/console`
   - `wp-config.php`
   - `public/index.php`
4. The edited or reviewed path is clearly part of a PHP service in a mixed repository.

PHP indicators are detectors for the relevant target, not sufficient reason to activate this skill for unrelated documentation, JavaScript, CSS, build tooling, or non-PHP packages in the same repository unless the change affects PHP runtime or security behavior.

Ignore PHP found only in dependencies, generated files, caches, fixtures, examples, backups, or build output. In a monorepo, apply this skill only to the affected PHP package.

## Combining with other skills

- If `$pond-debug-mantra` also applies, use it as the primary workflow for reproduction, fail-path tracing, and root-cause evidence. Apply this skill to the security boundaries and attacker-controlled inputs on the traced PHP path.
- If `$pond-scrutinize` also applies, use it for the final change review and verdict. Fold PHP-specific risks, controls, and residual assumptions into that review instead of producing a second standalone report.
- Reuse one trace across active skills. Do not repeat the same route, controller, job, query, or output path in multiple sections unless the distinction changes the conclusion.

## Mandatory security stance

For every activated PHP change:

- Treat data crossing a trust boundary as untrusted.
- Deny access by default.
- Authenticate the actor, then authorize the action and target object.
- Validate before side effects.
- Escape or encode for the exact output context.
- Use framework security APIs rather than custom security mechanisms.
- Keep secrets out of source, responses, logs, URLs, and client-controlled storage.
- Fail closed for authorization, signature, integrity, and tenant checks.
- Bound input size, work, memory, queries, redirects, retries, and external calls.
- Preserve security controls unless an explicitly approved replacement is stronger.
- Do not claim that an application is secure beyond what was verified.

Client-side checks, hidden fields, disabled controls, obscured URLs, and UI visibility are not security boundaries.

## Establish context before editing

1. Read applicable `AGENTS.md` and repository documentation.
2. Inspect:
   - `composer.json` and `composer.lock`
   - runtime and framework configuration
   - routes, controllers, middleware, commands, jobs, hooks, and entry points
   - authentication, authorization, sessions, persistence, storage, queues, and external services
   - tests and configured security tooling
3. Determine:
   - supported PHP and framework versions
   - actors, roles, tenants, ownership, and privilege levels
   - sensitive data and irreversible side effects
   - public and internal entry points
4. Trace the affected path:

```text
entry point
-> authentication
-> authorization
-> validation and canonicalization
-> business rules
-> persistence or external side effect
-> output encoding
-> logging and error handling
```

5. Identify attacker-controlled values and security boundaries on that path.

Scale context gathering to the risk and affected surface. For a small isolated change, inspect the affected entry point, local call path, relevant configuration, and tests; broaden to every subsystem above when the change crosses boundaries or the security impact is unclear.

Do not infer safety from comments, naming, an "internal" label, or UI restrictions.

## Non-negotiable implementation rules

### Input and type safety

- Prefer allowlists.
- Validate type, format, range, length, count, nesting, and allowed values.
- Reject unexpected fields when the contract is strict.
- Use strict comparisons for tokens, roles, identifiers, flags, and security decisions.
- Distinguish absent, `null`, empty string, zero, `"0"`, `false`, and empty collections when meanings differ.
- Do not rely on PHP truthiness, loose equality, implicit conversion, or sanitization alone.

### Injection prevention

- Use parameterized database queries or maintained query builders.
- Never interpolate untrusted values into SQL.
- Allowlist dynamic identifiers, operators, sort columns, and directions.
- Avoid shells; use process APIs with fixed executables and separated arguments.
- Never execute untrusted content through `eval()`, dynamic includes, templates, expressions, callbacks, or generated PHP.
- Use framework APIs for headers, mail, logs, redirects, CSV, and downstream protocols.

### Output safety

- Escape at the final sink for HTML text, attributes, URLs, JavaScript, CSS, JSON, XML, CSV, email, and other contexts.
- Use auto-escaping templates where available.
- Do not mark untrusted content as raw or safe.
- Encode JSON with a JSON encoder, not manual concatenation.
- Content Security Policy is defense in depth, not a replacement for correct encoding.

### Identity and access

- Use maintained framework authentication.
- Hash passwords with `password_hash()` or the framework password hasher.
- Generate security tokens with `random_bytes()` or an equivalent framework API.
- Authorize every protected action and object server-side.
- Scope records by tenant or owner before access or mutation.
- Allowlist mass-assignable fields.
- Derive roles, ownership, tenant, prices, status, and system fields from trusted server state.

### Browser requests and sessions

- Use CSRF protection for cookie-authenticated state changes.
- Do not perform state changes through safe HTTP methods.
- Do not disable CSRF globally to make a request pass.
- Regenerate session IDs after login and privilege changes.
- Use secure, HTTP-only cookies with an appropriate SameSite policy.
- Rate-limit login, reset, verification, token issuance, search, and expensive actions.

### Secrets and cryptography

- Store secrets through approved environment or secret-management systems.
- Never commit or log credentials, tokens, private keys, session IDs, or password-equivalent data.
- Use maintained authenticated encryption and signature APIs.
- Do not invent cryptographic protocols or token formats.
- Do not use predictable randomness for secrets.
- Do not use MD5, SHA-1, or reversible encryption for password storage.

### State integrity

- Enforce business rules server-side at commit time.
- Use transactions, unique constraints, atomic updates, locking, or version checks as required.
- Make retryable jobs, webhooks, payments, and external side effects idempotent.
- Expect duplicate requests, queue redelivery, webhook replay, retries, and concurrency.

## Threat-specific references

Load only the references relevant to the task:

- Read `references/web-input-output.md` for validation, SQL/command injection, XSS, CSRF, CORS, redirects, headers, errors, and logging.
- Read `references/identity-data.md` for authentication, authorization, IDOR, tenant isolation, sessions, tokens, mass assignment, cryptography, sensitive data, and state integrity.
- Read `references/files-network-parsers.md` for uploads, downloads, path traversal, dynamic loading, SSRF, deserialization, XML, archives, parser safety, and resource exhaustion.
- Read `references/frameworks.md` for Laravel, Symfony, WordPress, and pure PHP enforcement.
- Read `references/verification.md` for security tests, dependency auditing, supply-chain checks, and completion reporting.

When a task touches multiple threat classes, load every applicable reference.

## Secure change workflow

Use this as the full workflow for security-sensitive, cross-boundary, or high-risk PHP changes. For a small isolated change, first apply the activation and risk checks above, then use only the steps relevant to the affected path.

1. Confirm activation and detect the stack.
2. Map actors, assets, trust boundaries, and side effects.
3. Trace authentication, authorization, validation, persistence, output, and logging.
4. Load the applicable threat and framework references.
5. Enumerate relevant attack classes before editing.
6. Reuse established security controls.
7. Make the smallest secure change.
8. Add rejection tests for applicable malicious or invalid states.
9. Run narrow checks first, then broaden according to risk.
10. Remove temporary secrets, payloads, fixtures, accounts, and instrumentation.
11. Report residual risks and unverified assumptions.

Do not weaken a security control merely to preserve unsafe existing behavior or make a test pass.

## Minimum verification

Use repository-defined commands and installed tooling first.

As applicable, verify:

- PHP syntax.
- Targeted and broader tests.
- Static analysis and coding standards.
- `composer validate`.
- `composer audit` when network access is available.
- Authentication and authorization rejection paths.
- Cross-user and cross-tenant access.
- Missing, malformed, expired, replayed, and duplicated tokens or requests.
- Empty, null, zero, `"0"`, oversized, deeply nested, and unexpected input.
- Concurrent execution and partial failure.
- Upload, path, redirect, outbound URL, parser, and resource limits.
- Responses and logs do not disclose secrets or internal errors.

Do not run intrusive scans, brute force, exploit attempts, or destructive security tests against production or third-party systems.

## Completion

Report:

- PHP stack and affected entry points.
- Security boundaries and attack classes considered.
- Controls added, preserved, or changed.
- Files changed.
- Tests and checks run.
- Checks not run.
- Remaining assumptions, compatibility concerns, and residual risk.

When this skill is combined with `$pond-debug-mantra` or `$pond-scrutinize`, include these completion details once in the final response or review output instead of creating duplicate sections.

Never claim the system is fully secure, vulnerability-free, compliant, or production-ready beyond the available evidence.
