# Quickstart: Resume Generation

**Feature**: `001-fix-resume-args`
**Branch**: `001-fix-resume-args`

This guide documents the authoritative way to generate the HTML and PDF resume after
the calling-convention fix is implemented.

---

## Prerequisites

- Unix-like shell (Linux or macOS)
- `python3` installed (the shell script will attempt auto-install if missing)
- `PyYAML` Python package (auto-installed by the shell script if missing)
- `brave` browser in PATH for PDF generation (optional — HTML-only output if absent)

---

## Primary Workflow: Shell Script (Recommended)

```bash
cd /home/chuck/github/cjdonaldson

./generate-resume.sh Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html
```

**Expected output**:

```
Generated: /home/chuck/github/cjdonaldson/Charles_Donaldson_Resume.html
Generated: /home/chuck/github/cjdonaldson/Charles_Donaldson_Resume.pdf
```

**Exit code**: `0` on success.

### What the shell script does

1. Validates that exactly two arguments are provided (exits with usage message if not).
2. Installs any missing dependencies (`python3`, `pip`, `pyyaml`, `fonts-liberation`).
3. Delegates to `generate-resume.py` with both arguments passed through.

---

## Direct Python Invocation (Developer Workflow)

After the fix, the Python script requires both arguments explicitly — no silent defaults.

```bash
python3 generate-resume.py Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html
```

**Expected output**: same as above.

### Error cases

```bash
# Missing both arguments — prints usage and exits non-zero
python3 generate-resume.py

# Missing output argument — prints usage and exits non-zero
python3 generate-resume.py Charles_Donaldson_Resume-data.yaml
```

**Expected output** (both cases):

```
usage: generate-resume.py resume_data.yaml output.html
```

Exit code: `1`.

---

## Output Files

| File | Description |
|------|-------------|
| `Charles_Donaldson_Resume.html` | Generated HTML resume (the `output_html` argument) |
| `Charles_Donaldson_Resume.pdf` | PDF derived from the HTML (same directory, same stem) |

The PDF path is always derived automatically from the HTML output path — no separate
argument is needed or accepted.

---

## Validation After Implementation

Run the following checks manually to confirm the feature is working correctly:

```bash
# SC-001 + SC-002: no-args must fail with usage, no files written
python3 generate-resume.py
echo "Exit: $?"   # must be non-zero

# SC-003 + SC-004: happy path must produce HTML and PDF
./generate-resume.sh Charles_Donaldson_Resume-data.yaml Charles_Donaldson_Resume.html
echo "Exit: $?"   # must be 0
ls -l Charles_Donaldson_Resume.html Charles_Donaldson_Resume.pdf

# SC-005: no hardcoded paths remain in main()
grep -n 'resume_data.yaml\|Charles_Donaldson_Resume.html' generate-resume.py
# Should match ONLY lines outside main() (e.g., module docstring), not inside main()
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `usage: generate-resume.py ...` printed | Fewer than 2 args passed | Provide both `data_file` and `output_html` |
| `FileNotFoundError: resume_data.yaml` | Wrong path to data file | Verify the first argument path is correct |
| `Warning: 'brave' not found` | Brave browser not installed | Install Brave or use another Chromium-based browser at `/usr/bin/brave` |
| PDF not generated | Brave headless failed | Check `brave --version`; HTML is still written successfully |
