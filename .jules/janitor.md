# Janitor's Journal

## 2026-01-19 - Initial Setup

**Issue:** Missing journal file.
**Root Cause:** First run of the Janitor agent.
**Solution:** Created `.jules/janitor.md`.
**Pattern:** Always check for required documentation files.

## 2026-01-19 - Improved `uv_jupyter_kernel.py` Structure

**Issue:** Module-level side effects (checking for `uv`) and abrupt assertions made the script hard to test and unfriendly to users.
**Root Cause:** Rapid scripting often puts logic at the top level.
**Solution:** Moved `uv` detection into a function with proper error handling, and extracted kernel config generation.
**Pattern:** Avoid module-level executable code; use `if __name__ == "__main__":` guards and helper functions.
