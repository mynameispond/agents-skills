---
name: pond-php-security
description: Use when planning, changing, debugging, testing, or reviewing first-party PHP behavior, configuration, or security boundaries, or when explicitly invoked. Excludes docs/formatting-only work and formal or broad Codex Security scans and finding triage/tracking.
---

# PHP Security

Apply PHP security constraints inside the active workflow. Select one mode and merge evidence into the task report.

## Zero Trust at application boundaries

For affected PHP boundaries:

- Do not grant trust solely because a caller is on a private network, localhost, behind a gateway, already logged in, or an internal service. Verify the human or service identity and authorize the action and resource from verified context before protected operations.
- Grant only the capabilities, resources, and tenants needed for the task. Apply this to service accounts, worker tokens, and database credentials as well as human users.
- Deny protected operations when identity, ownership, tenant, or current authorization cannot be established. Authorization errors or timeouts must not become permission grants; cached decisions require an established freshness and revocation policy.
- Recheck relevant security context across queues and service boundaries, and before sensitive effects when permissions or business state may have changed. A valid token or signature alone does not authorize every object or state transition.

Use [identity-data.md](references/identity-data.md) for identity, token scope, revocation, and effect-time checks; [web-input-output.md](references/web-input-output.md) for untrusted data; and [frameworks.md](references/frameworks.md) for enforcement at the actual boundary.

## Mode router

| Mode | Use when |
| --- | --- |
| `lite` | Ordinary PHP changes; nearby code/callers show no affected risky boundary. |
| `targeted` | Affected input, auth/authz, validation, queries, output, files/paths, network, parsers, sessions/CSRF, tenant/ownership, secrets/crypto, queues/webhooks, dependencies, or security configuration; also explicit security emphasis. |
| `diff-review` | PHP diff/PR/commit/working-tree review without a formal scan. |
| `finding-fix` | Fixing a supplied vulnerability or plausible finding. |
| `audit-lite` | Vulnerability inspection of a narrow path or feature. |
| `escalate-to-codex-security` | Explicit repository-wide/broad discovery, deep/formal/artifact-producing scans, imported finding triage, external tracking, or direct Codex Security requests. |

Use the requested review/fix/audit mode; otherwise choose `lite` or `targeted`. For escalation, use the available Codex Security workflow. If unavailable, state the limitation and offer a bounded review without claiming the requested scan was completed.

## Lite

Inspect the change and nearby callers for boundary impact; use normal repository checks. Do not load security references or build a full trace/report for this mode. If a risky boundary or unresolved security question appears, switch to `targeted` and inspect it. Report the change and exact checks/results; include only material limitations.

## Boundary work and reviews

For `targeted`, `diff-review`, `finding-fix`, and `audit-lite`, trace relevant entry -> auth/authz -> validation -> business state -> persistence/external effects -> output/logging. Identify attacker control, actor/tenant/ownership context, enforcement, sink, and impact. Inspect surrounding controls before classifying a finding as reportable, suppressed, or deferred. Validate supplied findings or label them plausible before changing behavior; claim a fix only after verification.

Preserve framework controls and make the smallest secure change. Test applicable rejection, cross-user/tenant, malformed, replay, concurrency, and failure paths at the enforcement point. A request for brevity does not waive security validation. Report checked/deferred scope, findings/controls, exact checks and skipped-check reasons, and material compatibility/assumptions/risks once. Do not claim exhaustive coverage or produce formal scan artifacts.

Load only relevant references; use verification before completing security-sensitive work:

- [web-input-output.md](references/web-input-output.md): validation, injection, encoding, CSRF/CORS, redirects, logs.
- [identity-data.md](references/identity-data.md): auth, tenants, sessions, secrets, webhooks, concurrency.
- [files-network-parsers.md](references/files-network-parsers.md): paths, SSRF, parsers, archives, resource limits.
- [frameworks.md](references/frameworks.md): the detected Laravel, Symfony, WordPress, pure PHP, or mixed stack.
- [verification.md](references/verification.md): negative tests, dependencies, tooling, security-sensitive reporting.
