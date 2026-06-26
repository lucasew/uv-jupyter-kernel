# Consistently Ignored Changes

This file lists patterns of changes that have been consistently rejected by human reviewers. All agents MUST consult this file before proposing a new change. If a planned change matches any pattern described below, it MUST be abandoned.

---

## IGNORE: Input Validation in uv_jupyter_kernel.py

**- Pattern:** Adding input validation, sanitization, or regex checks (specifically for path traversal) to the `versions` argument in `uv_jupyter_kernel.py`.
**- Justification:** Multiple Sentinel PRs (#19, #21, #25, #27, #29) attempting to fix "path traversal" by validating the version string have been closed without merge. This indicates the logic is either unnecessary (trusted input) or the proposed fixes are not desired.
**- Files Affected:** uv_jupyter_kernel.py

## IGNORE: Automated Dependency Updates

**- Pattern:** Bumping versions of tools in `mise.toml` or actions in `.github/workflows/*.yml` without an explicit request.
**- Justification:** Automated dependency update PRs (#8, #34) are consistently closed or autoclosed. Versions should probably remain pinned or updated manually when needed.
**- Files Affected:** mise.toml, .github/workflows/*.yml

## IGNORE: Downgrading or Unpinning GitHub Actions

**- Pattern:** Downgrading GitHub Action versions (e.g., `actions/checkout` to v4, `mise-action` to v2) or replacing exact commit SHAs with major version tags.
**- Justification:** PR #30 attempted to unpin and downgrade action versions and was closed. Action versions should remain pinned to their specific exact versions/SHAs unless explicitly requested otherwise.
**- Files Affected:** .github/workflows/*.yml
