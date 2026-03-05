# cjdonaldson Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-04

## Active Technologies
- Python 3 (system python3) + Bash + PyYAML (existing; no new dependencies added) (001-fix-resume-args)
- Files — YAML input, HTML + PDF output (001-fix-resume-args)

- Python 3 (system default; `#!/usr/bin/env python3`) + PyYAML (already required), Brave browser headless (PDF generation) (001-update-resume-summary)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3 (system default; `#!/usr/bin/env python3`): Follow standard conventions

## Recent Changes
- 001-fix-resume-args: Added Python 3 (system python3) + Bash + PyYAML (existing; no new dependencies added)

- 001-update-resume-summary: Added Python 3 (system default; `#!/usr/bin/env python3`) + PyYAML (already required), Brave browser headless (PDF generation)

<!-- MANUAL ADDITIONS START -->
## Output Quality

When writing any file:
- remove trailing whitespace from every line before saving.
<!-- MANUAL ADDITIONS END -->
