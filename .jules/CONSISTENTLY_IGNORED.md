# Consistently Ignored Changes

This file lists patterns of changes that have been consistently rejected by human reviewers. All agents MUST consult this file before proposing a new change. If a planned change matches any pattern described below, it MUST be abandoned.

---

## IGNORE: Input Validation in uv_jupyter_kernel.py

**- Pattern:** Adding input validation or sanitization (specifically for path traversal) to the `versions` argument in `uv_jupyter_kernel.py`.
**- Justification:** Multiple PRs (#19, #21, #25, #27, #29) attempting to fix "path traversal" by validating the version string have been closed without merge. This indicates the logic is either unnecessary (trusted input) or the proposed fixes are not desired.
**- Files Affected:** uv_jupyter_kernel.py

## IGNORE: Automated Dependency Updates

**- Pattern:** Bumping versions of tools in `mise.toml` or actions in `.github/workflows/*.yml` without explicit request.
**- Justification:** Automated dependency update PRs (#4, #6, #8) are consistently closed/autoclosed. Versions should probably remain pinned or updated manually when needed.
**- Files Affected:** mise.toml, .github/workflows/*.yml
