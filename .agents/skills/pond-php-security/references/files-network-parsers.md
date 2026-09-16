# Files, Network, Parsers, and Resource Safety

Load this reference for uploads, downloads, filesystems, archives, images, external URLs, HTTP clients, XML, serialization, imports, or expensive processing.

## File uploads

Treat content, metadata, names, extensions, and paths as untrusted.

- Allowlist required extensions and content types.
- Validate upload status, size, dimensions, and count.
- Detect MIME from server-side file content; do not trust browser metadata.
- Generate a new server-side filename.
- Store outside the executable web root where practical.
- Prevent execution in upload storage.
- Do not preserve attacker-controlled path components.
- Check archive extraction for traversal, symlinks, nested archives, and decompression bombs.
- Apply image parsing or re-encoding only through maintained libraries with memory and dimension limits.
- Scan files when the risk model and infrastructure require it.

## Downloads and filesystem access

- Authorize before resolving or streaming.
- Map a validated identifier to a server-side file record.
- Prevent path traversal, symlink escape, and arbitrary reads.
- Canonicalize and verify containment inside an approved base directory.
- Consider time-of-check/time-of-use races.
- Set safe content type and disposition headers.
- Do not reflect an untrusted filename directly into headers.
- Avoid user-controlled include, require, locale, template, or configuration paths.
- Keep secrets, backups, dumps, logs, and source archives outside public directories.

## SSRF and outbound requests

- Prefer fixed service endpoints.
- Allowlist scheme, host, port, and path when targets must vary.
- Normally permit only HTTPS.
- Block loopback, private, link-local, multicast, reserved, and cloud metadata destinations as applicable.
- Revalidate every redirect.
- Limit redirects, connection time, read time, total time, and response size.
- Defend against DNS rebinding and alternate IP representations.
- Do not forward client-controlled authentication headers or internal credentials.
- Use egress controls or a controlled proxy where available.
- Do not render fetched content as trusted HTML.

## Serialization and XML

- Prefer JSON with a validated schema.
- Never call `unserialize()` on untrusted or integrity-unverified input.
- Do not treat `allowed_classes` as sufficient protection for hostile data.
- Disable XML external entities and network access.
- Limit document size, nesting, entity expansion, and parsing time.
- Do not instantiate classes or call methods based on parsed type names.

## Parser and archive limits

Apply size, depth, time, memory, and count limits to:

- JSON and XML
- CSV and spreadsheets
- archives and compressed streams
- images and documents
- regular expressions
- imports and exports

Prevent catastrophic regex behavior, archive expansion, excessive image dimensions, and whole-file loading when streaming is possible.

## Abuse and availability

Bound attacker-controlled work:

- request and response bodies
- upload size and count
- strings, arrays, nesting, and pagination
- database result counts
- regex input and complexity
- parser depth and archive expansion
- network requests, redirects, and retries
- queue attempts and job runtime
- expensive endpoint frequency

Use streaming, chunking, backpressure, concurrency limits, and rate limiting where appropriate. Ensure cache keys preserve authorization and tenant boundaries.
