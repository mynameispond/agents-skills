# Identity, Authorization, and Data Security

Load this reference for login, accounts, permissions, tenants, tokens, sessions, sensitive data, payments, workflows, queues, or persistent state.

## Authentication and credentials

- Prefer maintained framework authentication.
- Use `password_hash()`, `password_verify()`, and `password_needs_rehash()` or framework equivalents.
- Never store plaintext or reversibly encrypted passwords.
- Generate tokens with `random_bytes()` or an equivalent cryptographically secure framework API.
- Use timing-safe comparisons for secret values where applicable.
- Use generic login and recovery errors when account disclosure is unnecessary.
- Rate-limit authentication, recovery, verification, and token creation.
- Bind reset and verification tokens to one account, one purpose, an expiry, and one-time use.
- Invalidate relevant tokens and sessions after password, email, MFA, role, or account-security changes.
- Require re-authentication for high-risk actions where appropriate.

## Authorization, IDOR, and tenants

- Authenticate first, then authorize the action and target object.
- Enforce authorization at every entry point.
- Verify action-level and object-level access.
- Scope queries by owner or tenant before retrieving or changing records.
- Never trust client-provided owner, tenant, role, permission, status, balance, price, or approval fields.
- Deny when actor, role, owner, or tenant context is missing.
- Prevent horizontal and vertical privilege escalation.
- Recheck authorization in asynchronous jobs when actor context or permissions may change.
- Include security context in cache keys when data varies by user, role, tenant, or permission.
- Test another user's object ID and a lower-privileged actor.

## Mass assignment

- Allowlist writable fields.
- Do not pass entire request payloads to model create, update, hydrate, or persist operations.
- Protect ownership, tenant, role, permission, balance, status, approval, audit, and system fields.
- Derive sensitive fields from authenticated server context.
- Validate nested arrays and objects recursively.

## Sessions and cookies

- Use maintained session handling.
- Regenerate the session ID after login and privilege changes.
- Invalidate the server-side session on logout.
- Use `Secure`, `HttpOnly`, and an appropriate `SameSite` cookie policy.
- Scope cookie domain and path narrowly.
- Do not place session IDs or bearer tokens in URLs.
- Apply idle and absolute expiry appropriate to risk.
- Prevent fixation and reuse after authentication changes.

## Tokens and APIs

- Scope tokens by capability and resource.
- Support expiry and revocation.
- Store only a secure hash when plaintext retrieval is unnecessary.
- Show plaintext API tokens only at creation where practical.
- Never put bearer tokens in URLs.
- Do not expose internal model fields by default.
- Use explicit response resources or serializers.
- Set pagination, rate, and query-complexity limits.

## Webhooks

- Verify a signature over the exact raw body.
- Validate timestamp or freshness.
- Prevent replay using an event or idempotency identifier.
- Process effects idempotently.
- Do not trust account, amount, status, type, or ownership merely because the signature and JSON are valid.
- Retrieve critical state from the trusted provider when the protocol requires confirmation.

## Secrets and cryptography

- Keep secrets in approved environment or secret stores.
- Never commit or log live credentials, tokens, private keys, session IDs, or password-equivalent data.
- Use maintained authenticated encryption and signature APIs.
- Do not invent cryptographic algorithms, protocols, modes, token formats, or key derivation.
- Use cryptographic randomness.
- Do not use MD5 or SHA-1 for passwords.
- Separate keys by purpose and environment.
- Plan rotation and revocation.
- Minimize collection, retention, replication, and logging of sensitive data.

## Business logic and concurrency

- Recompute price, total, discount, quota, ownership, permission, and status server-side.
- Enforce valid state transitions.
- Prevent duplicate and replayed irreversible actions.
- Use idempotency for payments, provisioning, email, jobs, and external effects.
- Use transactions for related state changes.
- Use unique constraints and atomic updates for invariants.
- Use locking or optimistic version checks when concurrent updates can violate integrity.
- Revalidate inventory, balance, quota, approval, and authorization at commit time.
- Expect user double-clicks, retries, queue redelivery, webhook redelivery, and concurrent requests.
