## 2026-01-19 - Path Traversal in CLI Arguments
**Vulnerability:** User-provided `version` arguments were used directly in file path construction without sanitization. This allowed path traversal (e.g., `3.13/../../../tmp`) which could enable writing files to arbitrary locations.
**Learning:** Command-line arguments that feed into file system operations must always be treated as untrusted input. `pathlib` does not automatically sanitize ".." components when joining paths.
**Prevention:** Implement strict input validation for all user-provided data used in file paths. Use whitelisting (regex) rather than blacklisting when possible.
