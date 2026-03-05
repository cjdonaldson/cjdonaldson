# Research: Update Resume Summary Identity Statement

**Feature**: `001-update-resume-summary`
**Phase**: 0 — Outline & Research
**Status**: Complete — all unknowns resolved

---

## Research Questions

Three decisions needed resolution before the design could be locked.

---

### RQ-1: YAML Field Structure — Keep `titles` or rename?

**Question**: Should the `summary.titles` list be kept (with one item) or renamed to a
scalar field (e.g., `summary.statement`) with a different type?

**Evidence examined**:
- Current `Charles_Donaldson_Resume-data.yaml` `summary.titles` is a YAML list of 3
  strings used solely as display labels — not referenced anywhere else in the codebase.
- The generator iterates the list: `for title in summary["titles"]`. Replacing the list
  with a scalar removes iteration entirely and simplifies the logic.
- The spec Key Entities section names the target "Summary Identity Statement", not
  "Summary Titles". The old name `titles` is semantically incorrect for a prose sentence.
- Constitution Principle V (Simplicity) favours clean semantics over backward
  compatibility shims when there is only one consumer of the data.

**Decision**: Rename `summary.titles` → `summary.statement` (scalar string).

**Rationale**: The field name `titles` no longer describes its content once a single
prose sentence replaces three keyword labels. Renaming costs nothing (one generator
reference, zero external consumers) and improves readability of the YAML for the owner.

**Alternatives considered**:
- *Keep `titles` as a one-item list*: Valid but semantically misleading. The generator
  would need a special-case `if len == 1` branch or silently render one grid cell —
  neither is simpler than a clean rename.
- *Add a new `statement` field alongside `titles`*: Introduces dead data (`titles`
  remains but is ignored). Violates YAGNI and Constitution Principle I (single source
  of truth).

---

### RQ-2: CSS Approach — What replaces `.summary-grid`?

**Question**: Should `.summary-grid` be repurposed in-place (change its rules, keep the
class name), or replaced with a new class name?

**Evidence examined**:
- `.summary-grid` currently defines `display: grid; grid-template-columns: 1fr 1fr 1fr`
  with child-selector overrides for centering and right-aligning cells 2 and 3.
- The spec (FR-003) says "The `.summary-grid` CSS rule MUST be replaced with a
  block-level style appropriate for a prose paragraph."
- The HTML class attribute on the generated `<div>` will also be removed (replaced by
  `<p>`), so the old class name becomes unused.
- The generator will emit `<p class="summary-statement">`, so a new class name is
  required in CSS.

**Decision**: Delete all three `.summary-grid` rules; add a single `.summary-statement`
rule with `font-size: 1.2em; padding-bottom: 0.5em;`.

**Rationale**: The old class name is grid-specific; reusing it for a block paragraph
would be as confusing as the `titles` → `statement` rename was for the YAML. A new name
signals intent clearly. Three grid rules collapse to one block rule — net CSS reduction.

**Alternatives considered**:
- *Repurpose `.summary-grid` in-place*: Confusing name mismatch. Rejected.
- *Use an inline style on `<p>`*: Avoids CSS change but violates separation of concerns
  and makes the style invisible in the CSS file. Rejected.
- *Wrap in a `<div>` with a class instead of `<p>`*: `<p>` is semantically correct for
  a prose paragraph; `<div>` is generic. `<p>` chosen per semantic HTML best practice.

---

### RQ-3: Generator Rendering — How to emit the statement?

**Question**: Should the generator emit a `<p>` directly, or use a `<div>` wrapper?
Does the statement text need HTML-escaping or Markdown link processing?

**Evidence examined**:
- The existing `md_links()` helper converts `[text](url)` Markdown to `<a>` tags and is
  used for bullets and achievements. The identity statement contains no Markdown links.
- The statement text (dictated in the spec) contains no special HTML characters (`<`,
  `>`, `&`, `"`) that would require escaping.
- `<p>` is the semantically correct HTML element for a prose paragraph. The rest of the
  generator uses `<div>` for layout containers and `<p>` does not appear elsewhere, but
  semantic HTML is preferable.
- The bullet `<ul>` follows immediately after the identity statement in the DOM; a `<p>`
  will render with default block margin creating natural visual separation without
  additional CSS.

**Decision**: Emit `<p class="summary-statement">{summary["statement"]}</p>`. No
`md_links()` call needed. No HTML escaping needed for the dictated statement text.

**Rationale**: Single-line emit, no loop, no helper call. Cleaner than wrapping in a
`<div>`. The `<p>` default block margin replaces the `padding-bottom: 0.5em` that was
previously on `.summary-grid > div:nth-child(2)`.

**Alternatives considered**:
- *`<div class="summary-statement">`*: Functionally equivalent, semantically weaker. Rejected.
- *Apply `md_links()` defensively*: Unnecessary for this text; adds noise. Rejected. If
  future statement text ever contains Markdown links, `md_links()` can be added then.

---

## Summary of Decisions

| # | Question | Decision | Key Driver |
|---|----------|----------|------------|
| RQ-1 | YAML field name | Rename `titles` → `statement` (scalar) | Semantic correctness, Simplicity (Constitution V) |
| RQ-2 | CSS class | Delete `.summary-grid` rules; add `.summary-statement` block rule | Clean rename, fewer rules, spec FR-003 |
| RQ-3 | Generator emit | `<p class="summary-statement">` — no loop, no helpers | Semantic HTML, minimal code |

All NEEDS CLARIFICATION items resolved. Phase 1 design proceeds.
