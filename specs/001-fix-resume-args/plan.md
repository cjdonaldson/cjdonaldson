# Implementation Plan: Fix Resume Script Calling Convention

**Branch**: `001-fix-resume-args` | **Date**: 2026-03-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-fix-resume-args/spec.md`

## Summary

`generate-resume.py` currently has hardcoded fallback file paths (`resume_data.yaml` and
`Charles_Donaldson_Resume.html`) that are silently applied when arguments are omitted.
This creates a mismatched contract with `generate-resume.sh`, which already enforces two
required positional arguments. The fix removes the hardcoded defaults and adds an
upfront argument-count check to `main()` that prints a usage message and exits non-zero
when fewer than two arguments are supplied. No new dependencies, no new flags, no
behavioral change on the happy path.

## Technical Context

**Language/Version**: Python 3 (system python3) + Bash
**Primary Dependencies**: PyYAML (existing; no new dependencies added)
**Storage**: Files — YAML input, HTML + PDF output
**Testing**: Manual shell invocations (no test framework present in repo)
**Target Platform**: Linux / Unix-like (macOS compatible via Homebrew path in shell script)
**Project Type**: CLI script pair
**Performance Goals**: N/A — single-run, single-user script
**Constraints**: No new runtime dependencies (Constitution Principle V); no new flags (FR-007)
**Scale/Scope**: Single user, personal resume generator

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Data-Driven Resume | ✅ PASS | No change to data layer or YAML structure |
| II. Authentic Presentation | ✅ PASS | No biographical content generated or modified |
| III. Specification-First | ✅ PASS | spec.md exists; plan.md produced before any code change |
| IV. Output Quality | ✅ PASS | Happy-path behavior identical; must validate HTML+PDF output after implementation |
| V. Simplicity | ✅ PASS | Fix is a minimal `sys.argv` guard — no new dependency, no argparse |

**Post-Phase 1 re-check**: All gates remain green. The design adds zero dependencies and
touches exactly one function (`main()` in `generate-resume.py`). FR-007 is honored: no
flags, options, or arguments are added or removed.

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-resume-args/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── cli-contract.md  # Phase 1 output
└── tasks.md             # Phase 2 output (speckit.tasks — not created by speckit.plan)
```

### Source Code (repository root)

```text
generate-resume.sh       # Shell entry point — argument validation preserved, unchanged
generate-resume.py       # Python generator — main() updated to require 2 positional args
```

**Structure Decision**: Flat single-project layout matching the existing repo root
structure. No src/ hierarchy warranted for a two-file script pair.
