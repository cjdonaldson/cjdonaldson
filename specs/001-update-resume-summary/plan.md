# Implementation Plan: Update Resume Summary Identity Statement

**Branch**: `001-update-resume-summary` | **Date**: 2025-07-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-update-resume-summary/spec.md`

## Summary

Replace the three-column keyword title grid in the resume summary section with a single
full-width prose paragraph expressing a professional identity statement. The statement —
dictated by the owner — communicates an engineering philosophy centred on functional
paradigms, expressive data type construction, and business-domain architecture.

The change touches four files: the YAML data source (content change), the Python
generator (rendering logic), the CSS stylesheet (layout rule), and the two regenerated
output artifacts (HTML and PDF).

**Approach**: Rename `summary.titles` to `summary.statement` (scalar string) in the YAML;
update the generator to emit a `<p class="summary-statement">` instead of a grid of
`<div>` elements; replace the `.summary-grid` CSS rule with a simple block-level style.
No new dependencies. No other resume sections touched.

---

## Technical Context

**Language/Version**: Python 3 (system default; `#!/usr/bin/env python3`)
**Primary Dependencies**: PyYAML (already required), Brave browser headless (PDF generation)
**Storage**: Flat files — `Charles_Donaldson_Resume-data.yaml` (source), `Charles_Donaldson_Resume.html` and `Charles_Donaldson_Resume.pdf` (outputs)
**Testing**: Manual visual inspection of generated HTML (browser) and PDF; string-presence assertions via `grep` or `python -c`
**Target Platform**: Linux desktop (generation); any browser / PDF viewer (consumption)
**Project Type**: CLI script + static file generation
**Performance Goals**: N/A — single-user local generation; completes in seconds
**Constraints**: Output must render correctly at standard resume viewing width; PDF must fit within letter-page top section on no more than 2 lines at current font size
**Scale/Scope**: 3 source files modified; 2 output artifacts regenerated; no architectural change

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Data-Driven Resume** — content MUST reside in YAML; generator and HTML MUST NOT hardcode resume content | ✅ PASS | The identity statement will live in `summary.statement` in the YAML. The generator reads and emits it dynamically. No content hardcoded in scripts or templates. |
| **II. Authentic Presentation** — AI MUST NOT generate, draft, suggest, or insert any personal, biographical, or historical content | ✅ PASS | The statement text was dictated verbatim by the owner in the feature spec input. AI role here is limited to structural/scripting changes (YAML field rename, generator logic, CSS rule). |
| **III. Specification-First Development** — spec.md MUST exist before implementation; plan.md MUST exist before code is written | ✅ PASS | `spec.md` is complete and approved. This `plan.md` is being produced before any code changes. |
| **IV. Output Quality** — HTML and PDF MUST render correctly; changes MUST be validated by producing and visually inspecting actual output | ✅ PASS (conditional) | Validation is required after implementation: generate HTML, open in browser, verify statement text and absence of old titles; generate PDF, confirm no overflow. This step is a mandatory acceptance gate. |
| **V. Simplicity** — fewest dependencies; no unnecessary complexity | ✅ PASS | Zero new dependencies. Changes are targeted: one YAML field rename, ~5 generator lines replaced, one CSS rule replaced. YAGNI applied — no backward-compatibility shim needed. |

**Post-Phase-1 re-check**: All five principles remain satisfied. The data model and
contracts sections confirm no new dependencies and no external interfaces introduced.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-update-resume-summary/
├── plan.md        ← this file
├── research.md    ← Phase 0 output
├── data-model.md  ← Phase 1 output
├── quickstart.md  ← Phase 1 output
└── tasks.md       ← Phase 2 output (speckit.tasks — NOT created here)
```

No `contracts/` directory — this project has no external interfaces; it is a personal,
single-user local tool. The generator is run by the owner and consumes no public API.

### Source Files Changed

```text
Charles_Donaldson_Resume-data.yaml   # content: rename titles → statement; replace values
generate-resume.py                   # logic: replace grid loop with <p> emission
resume.css                           # layout: replace .summary-grid with .summary-statement
```

### Regenerated Outputs

```text
Charles_Donaldson_Resume.html        # regenerated after source file changes
Charles_Donaldson_Resume.pdf         # regenerated via Brave headless after HTML
```

**Structure Decision**: Flat-file personal project — no src/, tests/, or package
directories. All changes are in the repository root alongside existing files. The spec
directory under `specs/001-update-resume-summary/` holds all planning artifacts.

---

## Complexity Tracking

No Constitution violations. Table omitted per instructions.

---

## Phase 0: Research

*Output*: [`research.md`](./research.md)

Three decisions required investigation before design could be locked:

1. **YAML field structure** — Keep `titles` as a list or rename to `statement` as a scalar?
2. **CSS approach** — Minimal class rename or repurpose the existing class name in-place?
3. **Generator rendering** — Inline `<p>` or a wrapper `<div>`? Escape/sanitisation needed?

Findings are consolidated in `research.md`. All NEEDS CLARIFICATION items resolved.

---

## Phase 1: Design & Contracts

*Outputs*: [`data-model.md`](./data-model.md), [`quickstart.md`](./quickstart.md)

### Data Model

See [`data-model.md`](./data-model.md) for the complete YAML schema diff and field
specifications. Summary of decisions:

- `summary.titles` (list of 3 strings) → `summary.statement` (scalar string)
- All other `summary.*` fields (`bullets`, `bullets_comments`, `bullets_other`, `philosophy`) unchanged
- Generator field access changes from `summary["titles"]` to `summary["statement"]`

### Interface Contracts

**Skipped** — this is a purely internal personal tool with no external API, library
interface, CLI contract, or public schema. The YAML file is owner-maintained and not
consumed by any external system.

### Generator Logic Change

**Before** (`generate-resume.py` lines 65–69):
```python
w('      <div class="summary-grid"> <!-- 2 - 3 targeted job titles -->')
for title in summary["titles"]:
    w(f'        <div>{title}</div>')
w('      </div>')
```

**After**:
```python
w(f'      <p class="summary-statement">{summary["statement"]}</p>')
```

### CSS Layout Change

**Before** (`resume.css` lines 29–38):
```css
.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  font-size: 1.2em;
}
div.summary-grid > div:nth-child(2) {
  text-align: center;
  padding-bottom: 0.5em;
}
div.summary-grid > div:nth-child(3) {
  text-align: right;
}
```

**After** (replace all three rules with):
```css
.summary-statement {
  font-size: 1.2em;
  padding-bottom: 0.5em;
}
```

The `display: grid` and column child-selectors are removed entirely. The new rule is a
simple block-level paragraph — no alignment overrides, no grid track sizing.

### Quickstart

See [`quickstart.md`](./quickstart.md) for the step-by-step validation workflow an
implementer follows after making the changes.

---

## Acceptance Gate (post-implementation)

Before this branch may be merged, ALL of the following must be confirmed:

| Check | How to Verify |
|-------|---------------|
| SC-001: Generator runs without errors | `python3 generate-resume.py Charles_Donaldson_Resume-data.yaml` exits 0, produces HTML and PDF |
| SC-002: Exact statement text present in HTML | `grep -c "prevents illegal states and boolean blindness" Charles_Donaldson_Resume.html` returns `1` |
| SC-003: Old keyword titles absent from summary element | `grep -c "Senior Software Engineer\|Scala Functional\|Software Architect" Charles_Donaldson_Resume.html` returns `2` (job titles only, not summary) |
| SC-004: No horizontal overflow visible | Open HTML in browser at standard width; statement fully visible |
| SC-005: PDF fits within top section | Open PDF; identity statement renders on ≤ 2 lines, no overflow into experience section |
| FR-005: Bullet list unchanged | Bullet content in HTML matches current YAML `summary.bullets` verbatim |
| FR-006: No other sections altered | Skills, Work History, Education sections visually identical to pre-change output |
