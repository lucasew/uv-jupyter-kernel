# Critical Security Learnings

## Path Traversal in `uv_jupyter_kernel.py`
- **Vulnerability**: Path Traversal (CWE-22)
- **Description**: The `uv_jupyter_kernel.py` script accepted unfiltered user input via the `--versions` argument and used it directly to construct file paths for kernel configuration files. This allowed an attacker to write files to arbitrary locations on the file system by injecting path traversal sequences (e.g., `../../`) into the version string.
- **Fix**: Input sanitization was implemented using a whitelist regex `^[a-zA-Z0-9._+-]+$`. This ensures that only safe characters (alphanumeric, dot, underscore, plus, hyphen) are allowed in version strings, effectively blocking path separators.
- **Verification**: Verified using a test script that attempted to pass a malicious path (`foo/../../bar`), which was correctly rejected by the new validation logic.
