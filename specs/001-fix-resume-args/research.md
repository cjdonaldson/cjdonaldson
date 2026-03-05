# Research: Fix Resume Script Calling Convention

**Phase**: 0 — Outline & Research
**Feature**: `001-fix-resume-args`

## Research Questions

Two questions were evaluated before committing to a design:

1. Should `generate-resume.py` use `argparse` or a manual `sys.argv` guard?
2. Should the script error on exactly `< 2` args, or exactly `!= 2` args?

---

## Finding 1 — Argument Parsing Approach

**Decision**: Manual `sys.argv` guard (no `argparse`)

**Rationale**:

- `argparse` is the idiomatic Python stdlib choice for argument parsing but brings
  auto-generated `--help` flags and formatted usage output that are inconsistent with the
  existing shell script's style.
- The spec explicitly states: *"usage messages use a simple print-and-exit pattern
  consistent with the existing shell script style"* (Assumptions section).
- The shell script uses a bare `echo` + `exit 1` pattern; the Python script should mirror
  it with a `print()` + `sys.exit(1)`.
- Principle V (Simplicity) reinforces using the least mechanism that satisfies the
  requirement. A three-line guard in `main()` is sufficient.

**Alternatives Considered**:

| Option | Verdict | Reason Rejected |
|--------|---------|-----------------|
| `argparse` with `nargs=2` | Rejected | Adds `--help` flag (violates FR-007 "no new flags"); inconsistent style with shell script |
| `click` third-party library | Rejected | New runtime dependency (violates Principle V) |
| Manual `sys.argv` check | **Selected** | Zero new deps, mirrors shell script style, three lines of code |

---

## Finding 2 — Argument Count Boundary

**Decision**: Error when `len(sys.argv) < 3` (i.e., fewer than 2 positional args provided)

**Rationale**:

- FR-001 says the script MUST accept "exactly two required positional arguments."
- FR-007 says no arguments are added or removed — it does not say extra args must cause
  an error. Unix convention (and the existing shell script) is to error on *missing*
  required args, not on *extra* args.
- Checking `< 3` (rather than `!= 3`) is the minimal change that satisfies all
  acceptance scenarios in User Stories 3 and 4 without introducing new restrictions.

**Alternatives Considered**:

| Boundary | Verdict | Reason Rejected |
|----------|---------|-----------------|
| `len(sys.argv) != 3` | Rejected | Breaks potential future wrapper scripts that append debug flags; unnecessarily strict |
| `len(sys.argv) < 3` | **Selected** | Enforces the required minimum; consistent with shell script guard |

---

## Finding 3 — Empty String Argument Handling

**Decision**: Validate that neither argument is an empty string; error with usage message
and exit non-zero. No output files written.

**Rationale**:

- The spec edge-case section calls this out explicitly: *"if one is an empty string, the
  script should surface an error rather than silently writing to an unexpected location."*
- A two-line guard (`if not data_file_str.strip() or not output_file_str.strip()`) added
  immediately after the argc check satisfies this without additional dependencies.

---

## Summary of Decisions

| Question | Decision |
|----------|----------|
| Arg parsing mechanism | Manual `sys.argv` guard — no `argparse` |
| Arg count boundary | Error on `len(sys.argv) < 3` |
| Empty string handling | Explicit guard; print usage and exit non-zero |
| Hardcoded fallback removal | Delete the two default `Path(...)` assignments in `main()` |

All NEEDS CLARIFICATION items from Technical Context: **none** — the codebase and spec
together provided sufficient context for all decisions.
