# Tasks: Fix Resume Script Calling Convention

**Feature Branch**: `001-fix-resume-args`
**Input**: Design documents from `specs/001-fix-resume-args/`
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Contract**: [contracts/cli-contract.md](contracts/cli-contract.md)

**Scope**: Single file change — `generate-resume.py` `main()` only. `generate-resume.sh` is read-only (already correct).
**Tests**: Manual shell invocations only (no test framework in repo — see quickstart.md).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (no dependency on an incomplete task, different invocations/concerns)
- **[Story]**: User story this task belongs to (US1–US4 from spec.md)
- Exact file paths and line references included throughout

---

## Phase 1: Setup — Audit Current State

**Purpose**: Confirm the exact code to be replaced before touching anything. This phase takes under 2 minutes.

- [ ] T001 Audit `generate-resume.py` `main()` lines 140–151 to confirm the two hardcoded defaults (`script_dir / "resume_data.yaml"` on line 142, `script_dir / "Charles_Donaldson_Resume.html"` on line 143) and the two conditional overrides (`if len(sys.argv) > 1` on line 145, `if len(sys.argv) > 2` on line 147) that will be replaced in Phase 2

**Checkpoint**: You can see the six lines (142–148) that constitute the entire broken contract before writing a single character of new code.

---

## Phase 2: User Story 4 — Python Script Rejects Missing Arguments (Priority: P1) 🎯 Core Change

**Goal**: Remove hardcoded fallback paths and add upfront validation so `generate-resume.py` fails loudly with a usage message when fewer than two args are supplied or either is an empty string.

**Why first**: This is the only code change in the entire feature. All other user stories are validations of behavior that either already exists (US3) or becomes correct once this phase is complete (US1, US2).

**Independent Test**: `python3 generate-resume.py` → prints `usage: generate-resume.py resume_data.yaml output.html` to stderr and exits non-zero. No files written.

### Implementation for User Story 4

- [ ] T002 [US4] Add argc guard at the top of `main()` in `generate-resume.py` (insert before line 141): `if len(sys.argv) < 3: print("usage: generate-resume.py resume_data.yaml output.html", file=sys.stderr); sys.exit(1)` — mirrors the shell script's bare print-and-exit style (research.md Finding 1); boundary is `< 3` not `!= 3` (research.md Finding 2)

- [ ] T003 [US4] Add empty-string guard immediately after the argc guard in `generate-resume.py` `main()`: check `sys.argv[1].strip() == ""` or `sys.argv[2].strip() == ""` — if either is empty, print the same usage message to stderr and `sys.exit(1)` (spec.md Edge Cases; data-model.md Validation Rules)

- [ ] T004 [US4] Replace the six-line hardcoded-defaults + conditional-override block (lines 141–148 of `generate-resume.py`) with two direct assignments: `data_file = Path(sys.argv[1]).resolve()` and `output_file = Path(sys.argv[2]).resolve()` — delete `script_dir`, the two default `Path(...)` lines, and both `if len(sys.argv) >` guards; the `.resolve()` calls on lines 150–151 fold into these assignments (data-model.md AFTER block; contracts/cli-contract.md "Hardcoded Defaults Removed")

**Checkpoint**: `generate-resume.py` `main()` now starts with two guards (argc, empty string) followed by two direct `Path(sys.argv[N]).resolve()` assignments. No hardcoded path strings exist in `main()`. Running `python3 generate-resume.py` exits non-zero with a usage message. Running it with two valid args still produces HTML and PDF.

---

## Phase 3: User Story 1 — Shell Script Happy Path (Priority: P1)

**Goal**: Confirm the primary end-to-end workflow through `generate-resume.sh` is completely unaffected by the Phase 2 change.

**Independent Test**: `./generate-resume.sh Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html` → both `.html` and `.pdf` written, exit code `0`.

### Validation for User Story 1

- [ ] T005 [US1] Run `./generate-resume.sh Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html` from the repo root and verify: exit code is `0`, `Charles_Donaldson_Resume.html` is written, `Charles_Donaldson_Resume.pdf` is written alongside it (SC-003, SC-004; quickstart.md Primary Workflow)

- [ ] T006 [US1] Inspect `Charles_Donaldson_Resume.html` to confirm the generated content is substantively identical to pre-change output — name, contact, experience sections present and correctly formatted (FR-006: happy-path behavior must be identical)

**Checkpoint**: Shell-script invocation succeeds end-to-end. SC-003 and SC-004 pass.

---

## Phase 4: User Story 3 — Shell Script Rejects Missing Arguments (Priority: P1)

**Goal**: Confirm the shell script's existing argument-validation behavior has not regressed. No code change was made to `generate-resume.sh`; this phase is a regression gate.

**Independent Test**: `./generate-resume.sh` with 0 or 1 arg → usage message printed, exit code non-zero.

### Validation for User Story 3

- [ ] T007 [P] [US3] Run `./generate-resume.sh` (zero args) and verify: a usage message showing the expected syntax is printed, exit code is non-zero (spec.md US3 Acceptance Scenario 1; contracts/cli-contract.md exit code table)

- [ ] T008 [P] [US3] Run `./generate-resume.sh Charles_Donaldson_Resume-data.yaml` (one arg) and verify: a usage message is printed, exit code is non-zero, no HTML or PDF files are written (spec.md US3 Acceptance Scenario 2)

**Checkpoint**: Shell script regression gate passes. T007 and T008 can be run together (parallel invocations, independent).

---

## Phase 5: User Story 2 — Direct Python Invocation (Priority: P2)

**Goal**: Confirm that invoking `generate-resume.py` directly with both required arguments produces the same output as shell-script invocation — no silent defaults, no divergent behavior.

**Independent Test**: `python3 generate-resume.py Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html` → HTML and PDF produced, exit code `0`.

### Validation for User Story 2

- [ ] T009 [US2] Run `python3 generate-resume.py Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html` directly (bypassing the shell script) and verify: exit code is `0`, `Charles_Donaldson_Resume.html` is written, `Charles_Donaldson_Resume.pdf` is written alongside it (spec.md US2 Acceptance Scenario 1; quickstart.md Direct Python Invocation)

- [ ] T010 [P] [US2] Run `python3 generate-resume.py` (zero args) and verify: usage message printed to stderr, exit code `1`, no output files written (SC-001, SC-002)

- [ ] T011 [P] [US2] Run `python3 generate-resume.py Charles_Donaldson_Resume-data.yaml` (one arg) and verify: usage message printed to stderr, exit code `1`, no output files written (spec.md US4 Acceptance Scenario 2 — same Python guard covers US2 error cases)

- [ ] T012 [P] [US2] Run `python3 generate-resume.py "" Charles_Donaldson_Resume.html` (empty-string first arg) and verify: usage message printed, exit code `1`, no files written (spec.md Edge Cases; data-model.md Validation Rules)

**Checkpoint**: Direct Python invocation works identically to shell-script invocation for the happy path. All error cases exit loudly. US2 complete.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final acceptance checks across all success criteria; confirm no residue of the old contract remains.

- [ ] T013 Run SC-005 grep check: `grep -n 'resume_data\.yaml\|Charles_Donaldson_Resume\.html' generate-resume.py` — the strings must appear **only** outside `main()` (e.g., module docstring line 2); zero matches inside `main()` are required (spec.md SC-005; contracts/cli-contract.md "Hardcoded Defaults Removed")

- [ ] T014 [P] Run the full quickstart.md validation checklist from `specs/001-fix-resume-args/quickstart.md` (all four `bash` code blocks in "Validation After Implementation") and confirm all assertions pass: SC-001+SC-002 (no-args fails), SC-003+SC-004 (happy path succeeds), SC-005 (grep clean)

- [ ] T015 [P] Review `generate-resume.py` `main()` inline comments for accuracy — remove or update any comment that referenced the old optional-override logic; add a brief comment above the argc guard explaining that both args are required (code clarity; no behavioral change)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup/Audit)
    └── Phase 2 (US4 — Core Implementation)   ← BLOCKS everything below
            ├── Phase 3 (US1 — Shell Happy Path)
            ├── Phase 4 (US3 — Shell Regression Gate)   ← can run concurrently with Phase 3
            └── Phase 5 (US2 — Direct Python)            ← can run concurrently with Phases 3–4
                    └── Phase 6 (Polish)
```

### Task Dependencies Within Phase 2

```
T002 (argc guard)
    └── T003 (empty-string guard)   ← sequential: builds on same guard block
            └── T004 (remove old defaults + consolidate assignments)
```

### User Story Dependencies

| Story | Priority | Depends On | Independently Testable |
|-------|----------|------------|------------------------|
| US4 | P1 | Phase 1 audit | ✅ Yes — `python3 generate-resume.py` exits non-zero |
| US1 | P1 | US4 complete | ✅ Yes — shell script end-to-end |
| US3 | P1 | Nothing (shell unchanged) | ✅ Yes — shell exits non-zero with missing args |
| US2 | P2 | US4 complete | ✅ Yes — direct Python invocation |

---

## Parallel Opportunities

### Phase 4 + Phase 5 (after Phase 2 complete)

```bash
# Can validate concurrently — independent shell invocations:
./generate-resume.sh                                        # T007
./generate-resume.sh Charles_Donaldson_Resume-data.yaml    # T008
python3 generate-resume.py ""  Charles_Donaldson_Resume.html  # T012
```

### Within Phase 5

```bash
# T010, T011, T012 are all [P] — launch together:
python3 generate-resume.py                                                           # T010
python3 generate-resume.py Charles_Donaldson_Resume-data.yaml                       # T011
python3 generate-resume.py "" Charles_Donaldson_Resume.html                         # T012
```

### Within Phase 6

```bash
# T013, T014, T015 are all [P] — independent checks:
grep -n 'resume_data\.yaml\|Charles_Donaldson_Resume\.html' generate-resume.py      # T013
# run quickstart.md checklist                                                        # T014
# review/update main() comments                                                      # T015
```

---

## Implementation Strategy

### MVP (US4 + US1 only — minimum to ship)

1. Complete Phase 1: Audit `main()` (T001)
2. Complete Phase 2: US4 implementation (T002 → T003 → T004, sequential)
3. Complete Phase 3: US1 validation (T005, T006)
4. **STOP and VALIDATE**: Happy path works, failure path works. Ship.

### Full Delivery (all stories)

1. Phase 1 → Phase 2 (sequential — US4 blocks everything)
2. Phases 3 + 4 in parallel (US1 + US3, independent validations)
3. Phase 5 (US2, parallel sub-tasks T010/T011/T012)
4. Phase 6 (polish, all parallel)

### Total Scope

- **1 file modified**: `generate-resume.py` (≈ 8 lines changed in `main()`)
- **1 file read-only**: `generate-resume.sh` (regression gate only)
- **No new dependencies**, no new flags, no new files

---

## Notes

- [P] tasks = independent shell invocations or concerns — safe to run concurrently
- [Story] label maps each task to spec.md user story for traceability
- T002–T004 are the **only** code-writing tasks in this feature
- T005–T015 are all validation/acceptance tasks
- Usage message format (from contracts/cli-contract.md): `usage: generate-resume.py resume_data.yaml output.html` — print to **stderr**, not stdout
- Arg count boundary: `len(sys.argv) < 3` (not `!= 3`) — see research.md Finding 2
- No argparse; no `--help` flag — see research.md Finding 1 and FR-007
