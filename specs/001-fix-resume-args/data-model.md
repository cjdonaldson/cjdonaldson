# Data Model: Fix Resume Script Calling Convention

**Phase**: 1 — Design & Contracts
**Feature**: `001-fix-resume-args`

## Overview

This feature has no database or structured data schema change. The "data model" for this
fix is the **invocation contract** — the required inputs and outputs of each script. This
document captures the before/after state of `main()` in `generate-resume.py` and the
unchanged state of `generate-resume.sh`.

---

## Script Invocation Model

### generate-resume.py — BEFORE (current, broken)

```
main()
  data_file  = <script_dir>/resume_data.yaml        ← hardcoded default (REMOVED)
  output_file = <script_dir>/Charles_Donaldson_Resume.html  ← hardcoded default (REMOVED)

  if len(sys.argv) > 1: data_file  = Path(sys.argv[1])  ← optional override
  if len(sys.argv) > 2: output_file = Path(sys.argv[2])  ← optional override
```

**Problem**: Zero or one argument succeeds silently, using hardcoded paths. The script
behaves differently depending on whether it is invoked directly or through the shell
script.

---

### generate-resume.py — AFTER (this feature)

```
main()
  Guard: if len(sys.argv) < 3  →  print usage, sys.exit(1)      ← NEW
  Guard: if empty string arg   →  print usage, sys.exit(1)      ← NEW

  data_file   = Path(sys.argv[1]).resolve()   ← required positional arg 1
  output_file = Path(sys.argv[2]).resolve()   ← required positional arg 2

  pdf_file = output_file.with_suffix(".pdf")  ← derived (unchanged)
```

**Result**: Behavior when called with two valid arguments is identical to current
behavior. Behavior when called with fewer than two arguments is an explicit error.

---

### generate-resume.sh — UNCHANGED

The shell script already enforces the two-argument contract:

```bash
if [ "$#" -lt 2 ]; then
  echo
  echo "usage: $0 resume_data.yaml ./Charles_Donaldson_Resume.html"
  echo
  exit 1
fi
# ...
python3 "$SCRIPT_DIR/generate-resume.py" "$@"   ← passes both args through
```

No changes required here. This file is read-only for this feature.

---

## Argument Definitions

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| `sys.argv[1]` | `data_file` | Path string | ✅ Yes | Path to YAML resume data file |
| `sys.argv[2]` | `output_file` | Path string | ✅ Yes | Path for HTML output file |
| *(derived)* | `pdf_file` | Path | N/A | Same dir + stem as `output_file`, `.pdf` extension |

---

## Validation Rules

| Rule | Condition | Response |
|------|-----------|----------|
| Argc check | `len(sys.argv) < 3` | Print usage to stderr, `sys.exit(1)` |
| Empty string | `sys.argv[1].strip() == ""` or `sys.argv[2].strip() == ""` | Print usage to stderr, `sys.exit(1)` |
| File existence | `data_file` does not exist | Pre-existing `FileNotFoundError` from `open()` — must not regress |
| Output dir | Parent of `output_file` does not exist | Pre-existing `FileNotFoundError` from `open()` — must not regress |

---

## State Transitions

```
Invocation
    │
    ├─ argc < 2  ──→  print usage  →  exit(1)   [no files written]
    ├─ empty arg ──→  print usage  →  exit(1)   [no files written]
    └─ argc ≥ 2, non-empty
            │
            ├─ data_file unreadable  ──→  FileNotFoundError / exit(1)  [no HTML/PDF written]
            ├─ output_dir missing    ──→  FileNotFoundError / exit(1)  [no HTML/PDF written]
            └─ all valid
                    │
                    ├─ write HTML  →  exit(0) if ok
                    └─ write PDF   →  exit(0) if Brave succeeds; stderr warning if not
```
