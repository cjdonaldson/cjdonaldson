# Data Model: Update Resume Summary Identity Statement

**Feature**: `001-update-resume-summary`
**Phase**: 1 — Design & Contracts
**Source of truth**: `Charles_Donaldson_Resume-data.yaml`

---

## YAML Schema Change

### `summary` object — before

```yaml
summary:
  titles:             # list<string> — 3 short keyword labels
    - Senior Software Engineer
    - Scala Functional
    - Software Architect
  bullets:            # unchanged
    - ...
```

### `summary` object — after

```yaml
summary:
  statement: >-       # string — single full-width prose identity statement
    A software engineer using functional paradigms and data type construction
    that prevents illegal states and boolean blindness. Architecting solutions
    across the business domain.
  bullets:            # unchanged — not touched by this feature
    - ...
```

---

## Field Specifications

### `summary.statement` (new)

| Property | Value |
|----------|-------|
| **Type** | Scalar string (YAML block scalar `>-` recommended for readability) |
| **Replaces** | `summary.titles` (list of 3 strings) |
| **Generator access** | `summary["statement"]` |
| **HTML emission** | `<p class="summary-statement">{summary["statement"]}</p>` |
| **CSS class** | `.summary-statement` |
| **Validation** | Non-empty string; no Markdown links required; no HTML special characters |
| **Owner authority** | Content MUST be written or dictated by the repository owner; AI MUST NOT author |

### `summary.titles` (removed)

| Property | Value |
|----------|-------|
| **Status** | **Deleted** — field and all three values removed from YAML |
| **Reason** | Replaced by `summary.statement`; field name no longer semantically correct |
| **Migration** | No other file references `summary.titles`; deletion is safe |

### `summary.bullets` (unchanged)

| Property | Value |
|----------|-------|
| **Type** | List of strings (may contain Markdown `[text](url)` links) |
| **Status** | **Unchanged** — content, order, and rendering unaffected by this feature |
| **Generator access** | `summary["bullets"]` — unchanged |

---

## Generator Reference Change

| Location | Before | After |
|----------|--------|-------|
| `generate-resume.py` summary block | `for title in summary["titles"]:` loop emitting `<div>` per title inside `.summary-grid` | Single `<p class="summary-statement">` using `summary["statement"]` |

---

## CSS Rule Change

| Selector | Before | After |
|----------|--------|-------|
| `.summary-grid` | `display: grid; grid-template-columns: 1fr 1fr 1fr; font-size: 1.2em;` | **Deleted** |
| `div.summary-grid > div:nth-child(2)` | `text-align: center; padding-bottom: 0.5em;` | **Deleted** |
| `div.summary-grid > div:nth-child(3)` | `text-align: right;` | **Deleted** |
| `.summary-statement` | *(did not exist)* | `font-size: 1.2em; padding-bottom: 0.5em;` **(new)** |

---

## State / Lifecycle

This feature has no state machine or lifecycle transitions. The data model is static
content: authored in YAML → read by generator → emitted to HTML → rendered by browser /
converted to PDF. All transformations are pure and deterministic.

---

## Validation Rules

- `summary.statement` MUST be present in the YAML; generator MUST raise a `KeyError`
  naturally if missing (no defensive guard needed — PyYAML's `data["summary"]["statement"]`
  will fail loudly on a missing key, which is the correct behavior for a malformed data
  file).
- `summary.titles` MUST NOT appear in the YAML after this change (old key removed).
- The generated HTML MUST contain exactly one `<p class="summary-statement">` element.
- The generated HTML MUST NOT contain any element with `class="summary-grid"`.

---

## Impact Surface

| File | Change Type | Scope |
|------|-------------|-------|
| `Charles_Donaldson_Resume-data.yaml` | Content + field rename | `summary.titles` → `summary.statement`; value replaced |
| `generate-resume.py` | Logic — 4 lines replaced with 1 | Summary rendering block only |
| `resume.css` | Layout — 3 rules deleted, 1 added | Summary section only; no other selectors affected |
| `Charles_Donaldson_Resume.html` | Regenerated output | Summary section element changes; all other sections identical |
| `Charles_Donaldson_Resume.pdf` | Regenerated output | Summary section visual changes; all other sections identical |
