# PHP Framework Enforcement

Load the section matching the detected stack. Follow the repository's supported versions and established patterns.

## Laravel

- Validate with Form Requests or established validators.
- Authorize through policies, gates, middleware, or explicit authorization calls.
- Preserve CSRF protection for browser-session routes.
- Allowlist mass-assignable fields.
- Protect system-controlled attributes.
- Prefer Eloquent or the query builder with bound values.
- Scope models and route binding by tenant or ownership where required.
- Use framework hashing, encryption, sessions, signed URLs, rate limiting, and password reset features.
- Keep debug mode and detailed exceptions disabled in production.
- Make jobs idempotent and account for retries, timeout, uniqueness, and transaction commit timing.
- Do not bypass the repository configuration model with ad hoc environment access.

## Symfony

- Use Validator and the project's typed request mapping.
- Use voters, access controls, and security attributes for authorization.
- Use CSRF protection for browser state changes.
- Use PasswordHasher.
- Use Doctrine parameters and QueryBuilder.
- Use Process instead of shell concatenation.
- Use HttpClient with destination, redirect, timeout, and size restrictions.
- Keep profiler and debug routes inaccessible in production.
- Use the configured secrets mechanism.

## WordPress

- Validate input, sanitize before storage, and escape at the final output context.
- Unslash request data where WordPress APIs require it.
- Verify nonce and capability separately for privileged state changes.
- A nonce is not authorization.
- Define a restrictive `permission_callback` for REST routes.
- Register authenticated and unauthenticated AJAX hooks deliberately.
- Use `$wpdb->prepare()` correctly for direct SQL.
- Use WordPress upload, filesystem, HTTP, authentication, and escaping APIs.
- Prefix or namespace project-owned global identifiers.
- Keep debug logs and PHP errors unavailable publicly.
- Keep portable business functionality out of presentation-only theme code where practical.

## Pure PHP

When no framework security layer exists:

- Centralize request parsing, validation, authentication, authorization, CSRF, output encoding, errors, and session configuration.
- Use PDO or a maintained database layer with parameterized queries.
- Configure secure session cookies before starting sessions.
- Use platform password hashing and secure random APIs.
- Keep web entry points small and route through a controlled application layer.
- Store configuration and secrets outside public directories.
- Avoid creating a custom framework unless required.

## Mixed applications

- Apply the control at the actual enforcement layer.
- Do not assume a JavaScript frontend, reverse proxy, API gateway, WAF, or upstream service replaces PHP authorization or validation.
- Preserve security context across queues, events, CLI commands, cron, and service boundaries.
