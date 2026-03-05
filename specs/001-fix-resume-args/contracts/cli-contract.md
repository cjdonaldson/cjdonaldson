# CLI Contract: Resume Generation Scripts

**Phase**: 1 — Design & Contracts
**Feature**: `001-fix-resume-args`

These contracts define the authoritative calling convention for both resume generation
scripts after this feature is implemented. They are the ground truth for task
implementation and manual validation.

---

## generate-resume.sh

### Synopsis

```
generate-resume.sh <data_file> <output_html>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `data_file` | ✅ Yes | Path to the YAML resume data file (e.g., `Charles_Donaldson_Resume-data.yaml`) |
| `output_html` | ✅ Yes | Destination path for the generated HTML file (e.g., `Charles_Donaldson_Resume.html`) |

### Behavior

- Validates that exactly two arguments are provided; exits non-zero with a usage message
  if not (pre-existing behavior, must not regress).
- Installs missing runtime dependencies (`python3`, `pip`, `pyyaml`, `fonts-liberation`)
  if a supported system package manager is detected.
- Delegates to `generate-resume.py` by passing both arguments through via `"$@"`.

### Exit Codes

| Code | Condition |
|------|-----------|
| `0` | HTML and PDF generated successfully |
| `1` | Missing arguments (usage error) |
| `1` | Dependency installation failed |
| non-zero | Python script failure (propagated) |

### Usage Message

```
usage: generate-resume.sh resume_data.yaml ./Charles_Donaldson_Resume.html
```

---

## generate-resume.py

### Synopsis

```
python3 generate-resume.py <data_file> <output_html>
```

### Arguments

| Argument | Position | Required | Description |
|----------|----------|----------|-------------|
| `data_file` | `sys.argv[1]` | ✅ Yes | Path to the YAML resume data file |
| `output_html` | `sys.argv[2]` | ✅ Yes | Destination path for the HTML output file |

> **Note**: The PDF output path is derived automatically from `output_html` by replacing
> the extension with `.pdf`. No third argument is accepted or required.

### Behavior

1. **Argument validation** (NEW — this feature): If fewer than two positional arguments
   are provided, or if either argument is an empty string, print a usage message to
   stderr and exit with code `1`. No files are written.
2. Load YAML data from `data_file`.
3. Render HTML using the template logic in `build_html()`.
4. Write HTML to `output_html`.
5. Derive `pdf_path = output_html.with_suffix(".pdf")`.
6. Invoke Brave headless to render the PDF. If Brave is not found, emit a warning to
   stderr but do not fail (pre-existing behavior).

### Exit Codes

| Code | Condition |
|------|-----------|
| `0` | HTML written successfully (PDF is best-effort) |
| `1` | Fewer than 2 arguments provided **(NEW)** |
| `1` | Either argument is an empty string **(NEW)** |
| `1` | `data_file` cannot be opened (pre-existing) |
| `1` | `output_html` directory does not exist (pre-existing) |

### Usage Message (NEW)

```
usage: generate-resume.py resume_data.yaml output.html
```

Printed to stderr. Format mirrors the existing shell script usage message style.

### Hardcoded Defaults Removed (this feature)

The following hardcoded fallback assignments are **removed** from `main()`:

```python
# REMOVED:
data_file  = script_dir / "resume_data.yaml"
output_file = script_dir / "Charles_Donaldson_Resume.html"
```

After this change, both arguments are always taken from `sys.argv`.

---

## Contract Consistency Matrix

| Scenario | generate-resume.sh | generate-resume.py | Expected outcome |
|----------|-------------------|--------------------|-----------------|
| 0 args | ❌ exits(1) + usage | ❌ exits(1) + usage | Fail loudly at first point of entry |
| 1 arg | ❌ exits(1) + usage | ❌ exits(1) + usage | Fail loudly at first point of entry |
| 2 valid args via shell script | ✅ delegates to py | ✅ generates HTML+PDF | Success |
| 2 valid args directly to py | N/A | ✅ generates HTML+PDF | Success (same output) |
| 2 args, one empty string | ❌ exits(1) + usage | ❌ exits(1) + usage | Fail with clear error |
