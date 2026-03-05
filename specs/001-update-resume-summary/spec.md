# Feature Specification: Update Resume Summary Identity Statement

**Feature Branch**: `001-update-resume-summary`
**Created**: 2025-07-25
**Status**: Ready
**Input**: User description: "I am considering changing the summary section and grid in Charles_Donaldson_Resume-data.yaml and generate-resume.py which generates Charles_Donaldson_Resume.html and Charles_Donaldson_Resume.pdf from the 3 key words to be 'A software engineer using functional paradigms and data type construction that prevents illegal states and boolean blindness. Architecting solutions across the business domain.'"

## Overview

Replace the three short keyword titles in the resume summary grid ("Senior Software Engineer", "Scala Functional", "Software Architect") with a crafted professional identity statement that communicates Charles's engineering philosophy: *"A software engineer using functional paradigms and data type construction that prevents illegal states and boolean blindness. Architecting solutions across the business domain."*

This change affects the data source (`Charles_Donaldson_Resume-data.yaml`), the rendering layout (summary grid in CSS and generator), and both output artifacts (`Charles_Donaldson_Resume.html` and `Charles_Donaldson_Resume.pdf`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resume Viewer Sees Updated Identity Statement (Priority: P1)

A hiring manager or recruiter opens the resume and immediately reads the updated summary identity statement rather than the 3 generic keyword titles. The statement communicates a clear, distinctive professional philosophy.

**Why this priority**: This is the core outcome of the feature. Everything else flows from this visual and conceptual change.

**Independent Test**: Open the generated HTML in a browser. The summary area beneath the contact grid shows the new statement text. No keyword titles ("Senior Software Engineer", "Scala Functional", "Software Architect") appear.

**Acceptance Scenarios**:

1. **Given** the resume is generated from the updated YAML, **When** a viewer opens `Charles_Donaldson_Resume.html`, **Then** the summary identity area displays the text "A software engineer using functional paradigms and data type construction that prevents illegal states and boolean blindness. Architecting solutions across the business domain."
2. **Given** the resume is generated from the updated YAML, **When** a viewer opens `Charles_Donaldson_Resume.pdf`, **Then** the same statement is visible in the summary section, fully readable without truncation.
3. **Given** the previous 3 keyword titles existed, **When** the resume is regenerated, **Then** none of the old titles ("Senior Software Engineer", "Scala Functional", "Software Architect") appear anywhere in the summary grid area.

---

### User Story 2 - Data Source Accurately Reflects New Content (Priority: P2)

Charles opens `Charles_Donaldson_Resume-data.yaml` to maintain or iterate on the resume content. The YAML clearly expresses the new identity statement in a way that is easy to read and edit.

**Why this priority**: The YAML is the single source of truth. Correctness and maintainability of the data file is prerequisite to correct output generation.

**Independent Test**: Open `Charles_Donaldson_Resume-data.yaml` and read the `summary` section. The new statement text is present. Running `generate-resume.py` produces an HTML that renders the statement correctly.

**Acceptance Scenarios**:

1. **Given** `Charles_Donaldson_Resume-data.yaml` is opened, **When** the `summary` section is read, **Then** the new statement text is present and the 3 old keyword titles are absent.
2. **Given** the YAML is edited to adjust wording, **When** `generate-resume.py` is run, **Then** the updated wording appears in the HTML output without any other changes to the generator.

---

### User Story 3 - Summary Grid Layout Renders Appropriately (Priority: P3)

The layout of the summary identity area adapts to the new content so the statement is visually clear — neither crammed into a column fragment nor broken in an awkward way.

**Why this priority**: Visual layout is secondary to content correctness but still matters for a professional resume impression.

**Independent Test**: View the HTML in a browser and the PDF. The statement text fills the summary identity area in a visually balanced, readable way consistent with the overall resume typography.

**Acceptance Scenarios**:

1. **Given** the new statement replaces 3 short titles, **When** the HTML is viewed, **Then** the statement is displayed at the same prominent font size as before (1.2em relative to body) without visual breakage or empty grid columns.
2. **Given** the layout is updated, **When** the PDF is printed on letter paper, **Then** the statement fits within the top section and does not overflow into the experience section.

---

### Edge Cases

- What if the new statement text wraps to two lines in the summary grid area — does the layout accommodate this gracefully without overlapping the bullet list below?
- What if only the YAML is updated but the generator or CSS is not updated — does the output degrade in an obvious way rather than silently producing a broken layout?
- What if future titles are added back (e.g., returning to keyword format) — is the data structure flexible enough to accommodate both one statement and multiple short titles?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `summary.titles` field in `Charles_Donaldson_Resume-data.yaml` MUST be renamed to `summary.statement` (scalar string) expressing the new professional identity statement, replacing the prior list of 3 keyword titles.
- **FR-002**: Running `generate-resume.py` MUST produce `Charles_Donaldson_Resume.html` where the summary identity area renders the new statement at the same visual prominence as the previous 3-column keyword grid.
- **FR-003**: The summary grid MUST be replaced with a simple styled paragraph block. The statement MUST render as a single full-width paragraph — no column grid, no split segments. The `.summary-grid` CSS rule MUST be replaced with a block-level style appropriate for a prose paragraph.
- **FR-004**: Running `generate-resume.py` MUST produce `Charles_Donaldson_Resume.pdf` where the updated statement is legible and does not overflow its section.
- **FR-005**: The existing summary bullet points below the identity area MUST remain unchanged in content and layout.
- **FR-006**: No other sections of the resume (Skills, Work History, Education) MUST be altered by this change.

### Key Entities

- **Summary Identity Statement**: The top-of-resume professional declaration replacing keyword titles. Carries the author's engineering philosophy and differentiating positioning. Stored in the YAML data source and rendered by the generator into both HTML and PDF outputs.
- **Summary Grid**: The visual layout container for the identity statement. Currently a 3-column CSS grid aligning left / center / right. Will be replaced with a simple full-width block paragraph — no grid, no column alignment.
- **YAML Data Source** (`Charles_Donaldson_Resume-data.yaml`): The single source of truth for all resume content. The `summary.titles` list MUST be replaced by `summary.statement` (scalar string).
- **Resume Generator** (`generate-resume.py`): Reads the YAML and emits HTML. MUST be updated to read `summary["statement"]` (scalar) and emit a single `<p class="summary-statement">` in place of the loop over `summary["titles"]` that wraps each in a `<div>` inside the grid.

## Assumptions

- The existing bullet list under the summary (professional accomplishments and philosophy) is intentionally **not changed** by this feature.
- The `generate-resume.py` script continues to be the sole mechanism for regenerating output files; no other build step is required.
- The CSS file (`resume.css`) may require a targeted update to the `.summary-grid` rule if the grid column structure changes, but no other CSS sections are affected.
- The intent of the new statement is to communicate a technical philosophy to technically-literate evaluators (engineering managers, technical recruiters) rather than to be broadly accessible to non-technical audiences.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `generate-resume.py` completes without errors and produces both `Charles_Donaldson_Resume.html` and `Charles_Donaldson_Resume.pdf`.
- **SC-002**: The exact text "A software engineer using functional paradigms and data type construction that prevents illegal states and boolean blindness. Architecting solutions across the business domain." appears verbatim in the generated HTML.
- **SC-003**: None of the strings "Senior Software Engineer", "Scala Functional", or "Software Architect" appear inside the summary grid element of the generated HTML.
- **SC-004**: When the HTML is viewed in a browser at standard resume viewing width, the new statement text is fully visible without horizontal overflow or clipping.
- **SC-005**: The PDF summary section renders the statement on no more than 2 lines at the current font size and page margins, keeping it within the top identity block.
