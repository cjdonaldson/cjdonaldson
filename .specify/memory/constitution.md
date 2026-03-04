<!--
Sync Impact Report
==================
Version change:      1.0.0 → 1.1.0
Modified principles: II. Authentic Presentation — rule strengthened:
                     previous: AI-generated biographical content allowed with explicit
                               owner approval before commit.
                     amended:  AI MUST NOT generate any personal, biographical, or
                               historical content; prohibition is unconditional.
Added sections:      None
Removed sections:    None
Templates requiring updates:
  ✅ .specify/templates/plan-template.md — No change required; Constitution Check
     filled dynamically at plan time
  ✅ .specify/templates/spec-template.md — No change required
  ✅ .specify/templates/tasks-template.md — No change required
  ✅ .specify/templates/agent-file-template.md — No change required
Deferred TODOs:      None
-->

# cjdonaldson Constitution

## Core Principles

### I. Data-Driven Resume

Resume content MUST reside in structured YAML data files
(`Charles_Donaldson_Resume-data.yaml`). Generation scripts and HTML templates MUST NOT
hardcode resume content. Every content change MUST originate in the data layer; the
presentation layer derives from it automatically.

**Rationale**: Decoupling data from presentation ensures all output formats (HTML, PDF)
stay consistent and that content edits never require touching rendering logic.

### II. Authentic Presentation

All biographical and historical content (career history, hardware origins, personal
narrative) MUST be factually accurate and personally reviewed by the repository owner
before merge. AI MUST NOT generate, draft, suggest, or insert any personal, biographical,
or historical content for this repository. AI tools have no knowledge of the owner's
identity, lived experience, or history and therefore cannot produce authentic content.
The profile MUST reflect only what the owner has written or explicitly dictated; AI's
role is limited to structural, scripting, and tooling assistance.

**Rationale**: This repository is a professional and personal representation. No AI
system has sufficient context to authentically represent the owner's identity, history,
or voice. Any AI-generated personal content would be fabricated, regardless of how
plausible it appears.

### III. Specification-First Development

Every non-trivial change MUST begin with a feature specification (`spec.md`) before any
implementation work starts. Planning artifacts (`plan.md`, `tasks.md`) MUST exist before
code is written. Ad-hoc coding without a spec is prohibited for features. Minor typo
corrections, content-only YAML edits, and hotfixes to broken generation scripts are
exempt.

**Rationale**: Spec-first discipline reduces rework and creates a traceable record of
why decisions were made, which matters across long gaps between resume updates.

### IV. Output Quality

Generated artifacts (HTML resume, PDF) MUST render correctly in standard browsers and
PDF viewers without layout errors. HTML output MUST be valid. CSS MUST produce no
visible regressions. The PDF MUST be print-ready with correct pagination for letter-size
paper. Any change to generation scripts or CSS MUST be validated by producing and
visually inspecting actual output before merging.

**Rationale**: The resume is a professional-facing artifact. Rendering defects directly
impact the owner's professional image with potential employers.

### V. Simplicity

Solutions MUST use the fewest dependencies that satisfy requirements. New runtime
dependencies MUST be justified in the implementation plan. Scripts and templates MUST
remain readable without deep tooling knowledge. Complexity MUST be earned, not assumed;
YAGNI applies.

**Rationale**: This is a personal repository maintained by one person across potentially
long intervals. Unnecessary complexity raises the maintenance burden with no benefit.

## Content Standards

The following content rules apply to all profile and resume updates:

- The **GitHub profile README** (`README.md`) represents the owner's public identity;
  tone MUST be professional yet personal.
- The **historical context sections** (TRS-80, Amiga, etc.) document the owner's genuine
  computing history and MUST be updated only with content written or dictated by the
  owner; AI MUST NOT generate or paraphrase this content.
- **Technology badges and icons** MUST reflect technologies the owner actively uses or
  has substantive experience with; aspirational or unverified items MUST be excluded.
- **Resume data** (`Charles_Donaldson_Resume-data.yaml`) is the single source of truth
  for all professional experience, education, and skills; it MUST be kept current.

## Development Workflow

Feature development follows the speckit workflow:

1. `speckit.specify` — Write the feature specification
2. `speckit.clarify` — Resolve ambiguities (optional; run before planning)
3. `speckit.plan` — Produce the implementation plan and design artifacts
4. `speckit.tasks` — Generate the task list
5. `speckit.analyze` — Validate consistency across artifacts (recommended)
6. `speckit.implement` — Execute the implementation

All feature work MUST occur on a dedicated branch (format: `NNN-short-name`). Branches
MUST NOT be merged without a reviewed spec and passing output validation per Principle IV.

## Governance

This constitution supersedes all other development practices for this repository.

Amendments MUST be made via the `speckit.constitution` agent. Amendments that remove or
redefine an existing principle require a MAJOR version bump and MUST include a migration
note explaining the rationale. New principles or materially expanded guidance require a
MINOR bump. Clarifications, wording fixes, and non-semantic refinements use a PATCH bump.

All feature implementation plans MUST include a Constitution Check section verifying
compliance with Principles I–V before Phase 0 research begins and again after Phase 1
design is complete.

**Version**: 1.0.0 | **Ratified**: 2026-03-04 | **Last Amended**: 2026-03-04
