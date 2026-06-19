# Security Verification and Supply Chain

Load this reference before completing a security-sensitive PHP task.

## Dependency and supply-chain safety

- Preserve `composer.lock` for applications.
- Prefer established packages from trusted sources.
- Inspect package ownership, maintenance, release history, permissions, plugins, scripts, and transitive dependencies before adding one.
- Prefer a small maintained platform API over an unnecessary dependency.
- Run the configured dependency audit, including `composer audit`, when applicable and network access exists.
- Do not ignore an advisory without documenting exposure, affected paths, compensating controls, and a removal plan.
- Avoid arbitrary Composer repositories and untrusted package sources.
- Treat Composer scripts and plugins as code execution.
- Review untrusted changes before running install or update scripts.
- Do not update unrelated packages merely to make an audit pass.
- Preserve supported PHP and framework versions unless the task includes raising them.

## Required negative testing

For security-sensitive paths, test applicable rejection states:

- unauthenticated request
- authenticated but unauthorized request
- another user's or tenant's object
- missing, malformed, expired, replayed, or duplicated token
- unexpected fields and type-confused values
- absent, `null`, empty, zero, `"0"`, false, oversized, and deeply nested input
- invalid state transition
- duplicate request and concurrent execution
- dangerous filename, path, redirect, URL, or outbound destination
- dependency timeout, partial failure, retry, and redelivery
- log and response redaction

Tests must exercise the real enforcement point rather than only a UI or mocked intermediate state.

## Tooling

Use repository-defined tooling first. As applicable:

- PHP syntax checks
- targeted and broader tests
- static analysis
- coding standards
- `composer validate`
- `composer audit`
- framework route, configuration, and container checks
- security regression tests

Do not install unapproved scanners merely to complete the task.

Do not run intrusive scans, brute force, exploit attempts, destructive tests, or production data mutations against production or third-party systems.

## Completion report

Use the parent skill's Completion section as the reporting contract. Include these fields once, merged into the final response or `$pond-scrutinize` report instead of creating a second standalone completion report:

- detected PHP stack and entry points
- security boundaries and attack classes considered
- controls added, preserved, or changed
- files changed
- checks run and results
- checks not run
- residual risk, assumptions, and compatibility concerns

Do not claim full security, compliance, or production readiness beyond verified evidence.
