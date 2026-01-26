# Sentinel Journal

## 2026-01-26 - Path Traversal in uv_jupyter_kernel.py
**Vulnerability:** The `uv_jupyter_kernel.py` script accepted unvalidated version strings, allowing path traversal sequences (e.g., `../`) to manipulate the output directory for kernel configuration.
**Learning:** Always validate user input, especially when it is used to construct file paths. `pathlib` does not automatically sanitize `..` components when using `/` operator.
**Prevention:** Implement strict input validation using regex to ensure only expected characters (alphanumeric, dots, plus, minus) are allowed in version strings.
