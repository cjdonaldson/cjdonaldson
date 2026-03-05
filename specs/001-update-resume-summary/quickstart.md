# Quickstart: Implementing & Validating the Summary Update

**Feature**: `001-update-resume-summary`
**Branch**: `001-update-resume-summary`
**Phase**: 1 — Design & Contracts

---

## Prerequisites

- Python 3 with PyYAML: `python3 -c "import yaml; print('OK')`
- Brave browser (for PDF): `ls /usr/bin/brave`
- Working directory: repository root (`/home/chuck/github/cjdonaldson` or wherever cloned)
- On branch `001-update-resume-summary`: `git branch --show-current`

---

## Step 1 — Update the YAML data source

Open `Charles_Donaldson_Resume-data.yaml`. In the `summary:` section:

**Remove**:
```yaml
  titles:
    - Senior Software Engineer
    - Scala Functional
    - Software Architect
```

**Add** (use YAML block scalar `>-` to keep the text on one logical line):
```yaml
  statement: >-
    A software engineer using functional paradigms and data type construction
    that prevents illegal states and boolean blindness. Architecting solutions
    across the business domain.
```

> ⚠️ The statement text MUST be exactly as dictated by the owner. Do not paraphrase,
> reorder, or rephrase any part of it.

---

## Step 2 — Update the CSS

Open `resume.css`. Locate and **delete** these three rule blocks (lines ~29–38):

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

**Replace** with:
```css
.summary-statement {
  font-size: 1.2em;
  padding-bottom: 0.5em;
}
```

---

## Step 3 — Update the generator

Open `generate-resume.py`. Locate the summary rendering block (lines ~65–69):

```python
    w('      <div class="summary-grid"> <!-- 2 - 3 targeted job titles -->')
    for title in summary["titles"]:
        w(f'        <div>{title}</div>')
    w('      </div>')
```

**Replace** with:
```python
    w(f'      <p class="summary-statement">{summary["statement"]}</p>')
```

---

## Step 4 — Regenerate output

```bash
python3 generate-resume.py Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html
```

Expected console output:
```
Generated: /path/to/Charles_Donaldson_Resume.html
Generated: /path/to/Charles_Donaldson_Resume.pdf
```

If the PDF line shows an error, confirm Brave is installed at `/usr/bin/brave` and retry.

---

## Step 5 — Validate HTML (automated checks)

Run these one-liners from the repository root:

```bash
# SC-002: Exact statement text present
grep -c "prevents illegal states and boolean blindness" Charles_Donaldson_Resume.html
# Expected: 1

# SC-003: Old keyword titles absent from summary element
# (Job titles legitimately appear in work history — count should be exactly 2, not 0)
grep -c "Senior Software Engineer" Charles_Donaldson_Resume.html
# Expected: 2  (TST and 1010data job titles only)

grep -c "Scala Functional\|Software Architect" Charles_Donaldson_Resume.html
# Expected: 0

# Confirm new class present and old class absent
grep -c 'class="summary-statement"' Charles_Donaldson_Resume.html
# Expected: 1

grep -c 'class="summary-grid"' Charles_Donaldson_Resume.html
# Expected: 0
```

---

## Step 6 — Validate HTML (visual inspection)

Open `Charles_Donaldson_Resume.html` in a browser:

```bash
xdg-open Charles_Donaldson_Resume.html
# or: brave Charles_Donaldson_Resume.html
```

Confirm:
- [ ] The identity statement appears prominently below the contact grid
- [ ] No keyword titles ("Senior Software Engineer", "Scala Functional", "Software Architect") appear in the summary area
- [ ] The statement text is fully visible at standard viewing width — no horizontal overflow or clipping
- [ ] The bullet list below the statement is intact and unchanged
- [ ] Skills, Work History, and Education sections look identical to the pre-change layout

---

## Step 7 — Validate PDF (visual inspection)

Open `Charles_Donaldson_Resume.pdf`:

```bash
xdg-open Charles_Donaldson_Resume.pdf
```

Confirm:
- [ ] The identity statement renders on no more than 2 lines in the top section
- [ ] Text does not overflow into the experience section
- [ ] The rest of the resume is identical to the pre-change PDF

---

## Acceptance Checklist

All items must be checked before the branch is considered implementation-complete:

- [ ] SC-001: Generator exits 0, both HTML and PDF produced
- [ ] SC-002: Exact statement text present in HTML (grep returns 1)
- [ ] SC-003: Old keyword titles absent from summary area
- [ ] SC-004: No horizontal overflow in browser view
- [ ] SC-005: PDF fits within top section (≤ 2 lines)
- [ ] FR-005: Bullet list content unchanged
- [ ] FR-006: All other resume sections visually unchanged
