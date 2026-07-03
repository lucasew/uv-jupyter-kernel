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

## 2026-01-XX - Refactoring `uv_jupyter_kernel.py`

**Issue:** `main` function had mixed responsibilities, primitive obsession with versions, and hardcoded constants.
**Root Cause:** Script growth without refactoring.
**Solution:**
- Extracted `DEFAULT_VERSIONS`.
- Implemented `validate_version` with regex validation.
- Extracted `install_kernel` method.
- Simplified `main`.
**Pattern:** Extract Method, Fail Fast (Input Validation).

## 2026-07-03 - Implemented Centralized Error Reporting & Test Documentation

**Issue:** `uv_jupyter_kernel.py` used scattered `print` statements for error handling (violating centralized reporting rule), and tests lacked docstrings (identified by `tech-debt-tracker`).
**Root Cause:** Ad-hoc error handling during script creation; incomplete test coverage context.
**Solution:**
- Created a `report_error` function in `uv_jupyter_kernel.py`.
- Refactored `get_uv_path` and `main` to funnel exceptions and errors through `report_error`.
- Added descriptive docstrings to `tests/test_uv_jupyter_kernel.py` emphasizing security and testing nuances.
**Pattern:** Funnel unexpected errors through a centralized reporting function; ensure tests document their intent and security context.
