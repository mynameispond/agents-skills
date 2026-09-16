# Web Input and Output Security

Load this reference for HTTP requests, APIs, forms, rendering, database access, commands, redirects, CORS, errors, or logs.

## Validation and canonicalization

Potentially untrusted data includes request parameters, JSON, XML, multipart data, headers, cookies, routes, uploads, database values originating externally, sessions, caches, queues, webhooks, third-party responses, CLI arguments, environment variables, and plugin callbacks.

- Validate at the boundary.
- Prefer allowlists to blocklists.
- Validate structure recursively.
- Limit body size, field length, collection count, JSON depth, pagination, and query complexity.
- Reject duplicate or ambiguous values when the contract expects one value.
- Normalize only when a single canonical representation is defined.
- Perform security decisions after canonicalization.
- Validate decoded or decrypted structures again when they cross another boundary.
- Do not silently coerce malformed input into a privileged or valid value.

## SQL injection

- Use prepared statements or a maintained query builder.
- Never concatenate or interpolate untrusted data into SQL.
- Placeholders protect values, not identifiers or SQL syntax.
- Map sort columns, directions, table names, field names, and operators through fixed allowlists.
- Parameterize every element of dynamic value lists.
- Keep database privileges minimal.
- Use schema constraints to enforce integrity.
- Do not expose database errors.

## Command injection

- Avoid shell execution where a PHP or framework API exists.
- Use a process API that passes the executable and arguments separately.
- Use a fixed executable path.
- Allowlist the operation and argument grammar.
- Reject attacker-controlled option names and shell metacharacter semantics.
- Do not treat shell escaping as sufficient business validation.

## Code and template injection

Never execute untrusted content through:

- `eval()`
- dynamic `assert()`
- user-controlled `include` or `require`
- generated PHP
- dynamic template source
- expression evaluators
- user-selected callbacks, classes, or methods without an allowlist

## XSS and context encoding

Escape for the exact destination:

- HTML text
- HTML attributes
- URL
- JavaScript data
- CSS
- JSON
- XML
- CSV or spreadsheet
- email HTML and headers

Rules:

- Use framework auto-escaping.
- In plain PHP templates, encode with a declared character set and correct flags.
- Do not concatenate untrusted strings into HTML, JavaScript, CSS, or JSON.
- Do not mark untrusted data as raw.
- Sanitize rich HTML through a strict allowlist only when required.
- Escape stored values again at output.
- Set response content types correctly.
- Do not use CSP as a substitute for encoding.

## CSRF

For cookie-authenticated state changes:

- Use the framework CSRF mechanism.
- Verify a request-intent token.
- Do not use `GET` or `HEAD` for state changes.
- Do not rely only on SameSite cookies.
- Do not disable protection broadly.
- Scope exemptions narrowly and document the non-cookie authentication model.

## CORS

- Allow only required origins, methods, and headers.
- Do not reflect arbitrary origins.
- Do not use wildcard origins with credentials.
- Keep administrative endpoints unavailable cross-origin unless required.
- CORS does not replace authentication or authorization.

## Redirect and header safety

- Prefer fixed named routes or relative internal redirects.
- Allowlist redirect destinations.
- Reject protocol-relative and unexpected-scheme URLs.
- Never redirect directly to an untrusted URL.
- Reject CR and LF in values used for headers, email metadata, or line-based protocols.
- Do not place sensitive values in query strings.

## Error handling and logging

- Disable detailed error display in production.
- Return generic client-safe errors.
- Preserve exception context internally.
- Do not leak stack traces, SQL, paths, environment values, source, versions, or credentials.
- Use correlation IDs.
- Protect logs from injection and unauthorized access.
- Redact tokens, passwords, session IDs, private data, and request bodies on sensitive endpoints.
- Record meaningful authentication, privilege, export, and administrative events where appropriate.
