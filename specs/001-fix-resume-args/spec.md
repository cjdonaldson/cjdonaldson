# Feature Specification: Fix Resume Script Calling Convention

**Feature Branch**: `001-fix-resume-args`
**Created**: 2026-03-05
**Status**: Draft
**Input**: User description: "Resolve calling convention between generate-resume.sh and generate-resume.py so the Python script requires explicit positional arguments instead of using hardcoded fallback file paths"

## Overview

`generate-resume.sh` is the primary, authoritative entry point for building the resume. It enforces a strict argument contract and delegates to `generate-resume.py` by passing arguments through. Currently, `generate-resume.py` has hardcoded fallback file paths that are silently used when arguments are omitted — this creates a mismatched contract where the Python script behaves differently when invoked directly versus through the shell script. This feature removes that inconsistency: both scripts enforce the same two-argument requirement and fail loudly with a usage message if arguments are missing.

## Clarifications

### Session 2026-03-05

- Q: What argument parsing mechanism should `generate-resume.py` use to read and validate its positional arguments? → A: `sys.argv` raw access — no implicit flags, consistent with current code.
- Q: Where should usage/error messages be written when `generate-resume.py` (and `generate-resume.sh`) rejects missing or invalid arguments? → A: `stderr` only — standard Unix convention, keeps stdout clean.
- Q: What exit code should `generate-resume.py` use when it rejects missing or invalid arguments? → A: Exit code `1` — conventional general error, consistent with `generate-resume.sh`.
- Q: When exactly two arguments are supplied but one is an empty string `""`, how should `generate-resume.py` handle it? → A: Explicit check — validate that neither argument is an empty string before any file I/O; write a message to **stderr** and exit with code `1`.
- Q: How should `generate-resume.py` handle arguments that are whitespace-only (e.g., `"   "`)? → A: Strip then check — apply `.strip()` to each argument; if the result is empty, treat it as invalid: write a message to **stderr** and exit with code `1`. Catches both `""` and `"   "`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Invoke via Shell Script with Correct Args (Priority: P1)

A developer runs `generate-resume.sh resume_data.yaml Charles_Donaldson_Resume.html` to produce the HTML and PDF resume outputs. This is the primary supported workflow. The shell script validates the arguments and passes them to the Python script, which processes them without any fallback behavior.

**Why this priority**: This is the normal happy-path invocation. Everything downstream depends on this working correctly.

**Independent Test**: Run `./generate-resume.sh resume_data.yaml Charles_Donaldson_Resume.html` — both the `.html` and the corresponding `.pdf` files are produced with no errors.

**Acceptance Scenarios**:

1. **Given** valid `resume_data.yaml` and a target `.html` output path are supplied, **When** `generate-resume.sh` is invoked with those two arguments, **Then** the HTML file is written to the specified output path, the PDF is written alongside it with the same stem and `.pdf` extension, and the exit code is `0`.
2. **Given** the Python script receives the two positional arguments from the shell script, **When** it runs, **Then** it does not apply any hardcoded default file paths — it uses exactly the paths provided.

---

### User Story 2 - Invoke Python Script Directly with Correct Args (Priority: P2)

A developer invokes `generate-resume.py resume_data.yaml output.html` directly (bypassing the shell script), supplying both required arguments explicitly. The script runs successfully and produces the same outputs as when invoked through the shell script.

**Why this priority**: Direct invocation is a legitimate workflow for developers debugging or testing the Python layer in isolation. It should work the same way as shell-script invocation, not silently apply different defaults.

**Independent Test**: Run `python generate-resume.py resume_data.yaml output.html` — both `output.html` and `output.pdf` are produced, exit code is `0`.

**Acceptance Scenarios**:

1. **Given** two valid positional arguments are passed directly to `generate-resume.py`, **When** the script runs, **Then** the HTML is written to the path given as the second argument, the PDF is written alongside it, and the exit code is `0`.

---

### User Story 3 - Shell Script Rejects Missing Arguments (Priority: P1)

A developer runs `generate-resume.sh` with fewer than two arguments. The shell script immediately writes a usage message to **stderr** and exits with a non-zero code. This behavior already exists and must be preserved.

**Why this priority**: Argument enforcement at the shell layer is the first line of defense and is already in place. It must not regress.

**Independent Test**: Run `./generate-resume.sh` with zero or one argument — a usage message is written to **stderr** and the exit code is non-zero.

**Acceptance Scenarios**:

1. **Given** `generate-resume.sh` is invoked with no arguments, **When** it runs, **Then** a usage message showing the expected syntax is written to **stderr** and the exit code is non-zero.
2. **Given** `generate-resume.sh` is invoked with only one argument, **When** it runs, **Then** a usage message is written to **stderr** and the exit code is non-zero.

---

### User Story 4 - Python Script Rejects Missing Arguments (Priority: P1)

A developer invokes `generate-resume.py` directly with zero or one argument (perhaps forgetting the contract). Instead of silently falling back to hardcoded file paths and possibly overwriting unintended files, the script writes a usage message to **stderr** and exits with a non-zero code.

**Why this priority**: This is the core behavioral change of the feature. Without it, the hardcoded fallback remains and the calling convention is still mismatched.

**Independent Test**: Run `python generate-resume.py` with no arguments — a usage message is written to **stderr** and the exit code is `1`. No files are written.

**Acceptance Scenarios**:

1. **Given** `generate-resume.py` is invoked with no arguments, **When** it runs, **Then** a usage message showing the expected positional arguments is written to **stderr** and the exit code is `1`. No output files are created.
2. **Given** `generate-resume.py` is invoked with only one argument, **When** it runs, **Then** a usage message is written to **stderr** and the exit code is `1`. No output files are created.

---

### Edge Cases

- What happens when the input YAML file path argument is valid syntactically but the file does not exist? The script should report a clear error (this is pre-existing behavior and must not regress).
- What happens when the output HTML path argument points to a directory that does not exist? The script should report a meaningful error (pre-existing behavior, must not regress).
- What happens when exactly two arguments are provided but one is an empty string `""` or a whitespace-only string (e.g., `"   "`)? `generate-resume.py` MUST apply `.strip()` to each argument and treat the result as invalid if it is empty; it MUST write a message to **stderr** and exit with code `1` before any file I/O. No output files may be written. This single check covers both `""` and purely-whitespace values.
- PDF output path derivation: if the HTML output path is `./out/resume.html`, the PDF must be written to `./out/resume.pdf` — same directory, same stem, `.pdf` suffix. This behavior is unchanged.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `generate-resume.py` MUST accept exactly two required positional arguments: the data input file path and the HTML output file path.
- **FR-002**: `generate-resume.py` MUST NOT contain hardcoded fallback file paths for either the input data file or the HTML output file.
- **FR-003**: When invoked with fewer than two arguments, `generate-resume.py` MUST write a usage message that names both required positional arguments to **stderr** and exit with exit code `1`. No output files may be written. Nothing is written to stdout. Argument count is checked via `sys.argv` (i.e., `len(sys.argv) < 3`); no argument-parsing library (e.g., `argparse`) is used.
- **FR-004**: `generate-resume.sh` MUST continue to enforce exactly two required positional arguments and pass them through to `generate-resume.py`, preserving its existing validation behavior.
- **FR-005**: The PDF output path MUST continue to be derived from the HTML output path: same directory and file stem, with the extension changed to `.pdf`. No argument is added for the PDF path.
- **FR-006**: When both arguments are provided correctly, the end-to-end behavior of producing the HTML and PDF resume outputs MUST be identical to the current behavior.
- **FR-007**: No other flags, options, or arguments are added or removed from either script as part of this change.
- **FR-008**: When exactly two positional arguments are supplied but either is blank — defined as an empty string `""` or a whitespace-only string — `generate-resume.py` MUST apply `.strip()` to each argument, treat any result that is empty as invalid, write a message to **stderr**, and exit with code `1` before any file I/O. No output files may be written. This single strip-then-check covers both `""` and values such as `"   "`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `generate-resume.py` with no arguments exits with exit code `1` and writes a usage message to **stderr** in 100% of invocations — verified by automated test or manual check. Nothing is written to stdout.
- **SC-002**: Running `generate-resume.py` with no arguments creates zero output files.
- **SC-003**: Running `generate-resume.py` with both required arguments produces the same HTML and PDF files as the current implementation in 100% of test cases with valid inputs.
- **SC-004**: Running `generate-resume.sh` with both required arguments continues to succeed end-to-end with exit code `0` and correct output files.
- **SC-005**: No hardcoded file path strings for `resume_data.yaml` or `Charles_Donaldson_Resume.html` remain in the `main()` function of `generate-resume.py`.
- **SC-006**: Running `generate-resume.py` with exactly two arguments where at least one is blank (empty string `""` or whitespace-only, e.g., `"   "`) exits with code `1`, writes a message to **stderr**, and creates zero output files — verified by automated test or manual check. The strip-then-check logic must catch both cases.

## Assumptions

- The shell script (`generate-resume.sh`) already correctly enforces two required arguments; its argument-validation logic is not modified by this feature.
- The PDF output path derivation logic (same stem, `.pdf` suffix, same directory as HTML output) is implemented inside `generate-resume.py` and is not driven by an argument — this contract is unchanged.
- Both scripts are invoked in a Unix-like shell environment. Windows compatibility is out of scope.
- No new CLI flags (e.g., `--help`, `--verbose`) are introduced as part of this change; usage messages use a simple write-to-stderr-and-exit pattern consistent with the existing shell script style.
- Argument parsing in `generate-resume.py` uses `sys.argv` directly — no argument-parsing library (e.g., `argparse`, `click`) is used, consistent with the current codebase style and the requirement for no implicit flags.
