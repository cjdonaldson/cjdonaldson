#!/usr/bin/env python3
"""Generate <resume_filename>.html, .pdf, and .txt from <resume_filename>-data.yaml."""

import argparse
import re
import subprocess
import sys
import textwrap
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

BRAVE = "/usr/bin/brave"


def md_links(text):
    """Convert markdown [text](url) links to HTML <a> tags."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def strip_md_links(text):
    """Strip markdown [text](url) links to plain title text only."""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)


def stack_html(stack):
    """Format pipe-separated stack string with non-breaking spaces."""
    return stack.replace(" | ", " &nbsp; | &nbsp; ")


def nbsp(text):
    """Replace a bare space before non-breaking space markers in jbrief."""
    return text.replace("\u00a0", "&nbsp;")


def build_html(data, company_details=False, show_stack=False):
    p = data["personal"]
    meta = data["meta"]
    summary = data["summary"]
    skills = data["skills"]
    experience = data["experience"]
    education = data["education"]

    lines = []
    w = lines.append

    w('<!DOCTYPE html>')
    w('<html>')
    w('')
    w('<head>')
    w('  <meta charset="UTF-8">')
    w(f'  <meta name="description" content="{meta["description"]}">')
    w(f'  <meta name="keywords" content="{meta["keywords"]}">')
    w(f'  <meta name="author" content="{p["name"]}">')
    w('')
    w(f'  <title>{p["name"]} Resume</title>')
    w('  <link rel="stylesheet" href="resume.css">')
    w('  <style>')
    w('    @media print { @page { size: letter; margin: 13mm 13mm; } body { margin: 0; } }')
    w('  </style>')
    w('</head>')
    w('')
    w('<body>')
    w(f'  <div class="resume-title">{p["name"]}</div>')
    w('  <hr />')
    w('  <div class="contact-grid">')
    w(f'    <div>{p["location"]}</div>')
    w(f'    <div><a href="mailto:{p["email"]}">{p["email"]}</a></div>')
    w(f'    <div>{p["phone"]}</div>')
    linkedin_display = p["linkedin"].replace("https://", "")
    w(f'    <div><a href="{p["linkedin"]}">{linkedin_display}</a></div>')
    w('  </div>')
    w('')

    # Summary
    w('  <div>')
    w('    <sectionName><!-- Summary --></sectionName>')
    w('    <div class="summary">')
    w(f'      <p class="summary-statement">{summary["statement"]}</p>')
    w('      <ul>')
    for bullet in summary["bullets"]:
        w(f'        <li>{md_links(bullet.strip())}</li>')
    w('      </ul>')
    w('    </div>')
    w('  </div>')
    w('')

    # Skills
    w('  <div>')
    w('    <sectionName><!-- Skills --></sectionName>')
    w('    <div class="skills-container">')
    w('      <div class="skills">')
    w('        <ul>')
    for skill in skills:
        w(f'          <li>{skill}</li>')
    w('        </ul>')
    w('      </div>')
    w('    </div>')
    w('  </div>')
    w('')

    w('  <sectionName class="tight-bottom"><!--Work History--></sectionName>')
    w('')

    # Experience
    for job in experience:
        css_class = 'job print-break' if job.get('print_break') else 'job'
        w(f'  <div class="{css_class}">')
        w(f'    <company>')
        w(f'      <a href="{job["url"]}">{job["company"]}</a>, {job["location"]}')
        w(f'      <jdate>{job["start"]} to {job["end"]}</jdate>')
        w(f'    </company>')
        if company_details:
            w(f'    <brief>')
            w(f'      {job["brief"].strip()}')
            w(f'    </brief>')
            if job.get("company_stack"):
                w(f'    <div class="company-stack">{stack_html(job["company_stack"])}</div>')
        w(f'    <jtitle>{job["title"]}</jtitle>')
        w(f'    <jbrief>')
        w(f'      {job["description"].strip()}')
        w(f'    </jbrief>')
        w(f'    <div class="achievements">')
        w(f'      <ul>')
        for achievement in job["achievements"]:
            w(f'        <li>{md_links(achievement.strip())}</li>')
        w(f'      </ul>')
        w(f'    </div>')
        if show_stack:
            w(f'    <div class="stack">{stack_html(job["stack"])}</div>')
        w(f'  </div>')
        w('')

    # Education
    w('  <sectionName>Education</sectionName>')
    for edu in education:
        w(f'  {edu["institution"]}, {edu["location"]}<br />')
        w(f'  {edu["degree"]}')

    w('')
    w('</body>')
    w('')
    w('</html>')

    return "\n".join(lines) + "\n"


TXT_WIDTH = 80
SECTION_RULE = "=" * TXT_WIDTH
JOB_RULE = "-" * TXT_WIDTH


def wrap(text, indent="", subsequent_indent=None):
    """Wrap text to TXT_WIDTH with optional indent and continuation indent."""
    return textwrap.fill(
        text.strip(),
        width=TXT_WIDTH,
        initial_indent=indent,
        subsequent_indent=indent if subsequent_indent is None else subsequent_indent,
    )


def join_items_no_break(items):
    """Join items with ', ', never breaking a single item across lines."""
    result_lines = []
    current_line = ""
    for item in items:
        candidate = item if not current_line else f"{current_line}, {item}"
        if len(candidate) <= TXT_WIDTH:
            current_line = candidate
        else:
            if current_line:
                result_lines.append(current_line)
            current_line = item
    if current_line:
        result_lines.append(current_line)
    return "\n".join(result_lines)


def stack_txt(stack):
    """Convert pipe-separated stack string to a comma-separated plain string."""
    return re.sub(r'\s*\|\s*', ', ', stack)


def build_formatted_txt(data, company_details=False, show_stack=False):
    """Build a plain-text ATS-parsable resume from the YAML data."""
    personal = data["personal"]
    summary = data["summary"]
    skills = data["skills"]
    experience = data["experience"]
    education = data["education"]

    lines = []
    w = lines.append

    # Header
    w(personal["name"])
    w(personal["location"])
    w(personal["phone"])
    w(personal["email"])
    linkedin_display = personal["linkedin"].replace("https://", "").replace("http://", "")
    w(f"LinkedIn: {linkedin_display}")
    w("")

    # Summary
    w(SECTION_RULE)
    w("SUMMARY")
    w(SECTION_RULE)
    w("")
    w(wrap(strip_md_links(summary["statement"])))
    w("")
    for bullet in summary["bullets"]:
        bullet_text = strip_md_links(bullet.strip())
        w(wrap(bullet_text, indent="- ", subsequent_indent="  "))
    w("")

    # Skills
    w(SECTION_RULE)
    w("SKILLS")
    w(SECTION_RULE)
    w("")
    skills_text = join_items_no_break(skills)
    w(skills_text)
    w("")

    # Experience
    w(SECTION_RULE)
    w("EXPERIENCE")
    w(SECTION_RULE)

    for job_index, job in enumerate(experience):
        w("")
        w(job["title"])
        w(f'{job["company"]} | {job["location"]}')
        w(f'{job["start"]} - {job["end"]}')
        w("")
        if company_details:
            w(wrap(strip_md_links(job["brief"])))
            if job.get("company_stack"):
                w(f'Company Stack: {stack_txt(job["company_stack"])}')
            w("")
        w(wrap(strip_md_links(job["description"])))
        if job.get("description_additional"):
            w("")
            w(wrap(strip_md_links(job["description_additional"])))
        w("")
        for achievement in job["achievements"]:
            achievement_text = strip_md_links(achievement.strip())
            w(wrap(achievement_text, indent="- ", subsequent_indent="  "))
        if show_stack:
            w(f'Stack: {stack_txt(job["stack"])}')
        if job_index < len(experience) - 1:
            w("")
            w(JOB_RULE)

    # Education
    w("")
    w(SECTION_RULE)
    w("EDUCATION")
    w(SECTION_RULE)
    w("")
    for edu in education:
        w(edu["degree"])
        w(f'{edu["institution"]} | {edu["location"]}')
        w(f'GPA: {edu["gpa"]}')
        if edu.get("curriculum"):
            w(f'Curriculum: {edu["curriculum"]}')

    return "\n".join(lines) + "\n"


def normalize(text):
    """Collapse all internal whitespace and newlines to single spaces."""
    return " ".join(text.split())


def build_ats_txt(data, company_details=False, show_stack=False):
    """Build an ATS-ingest txt resume: no line wrapping, no indented continuations."""
    personal = data["personal"]
    summary = data["summary"]
    skills = data["skills"]
    experience = data["experience"]
    education = data["education"]

    lines = []
    w = lines.append

    # Header
    w(personal["name"])
    w(personal["location"])
    w(personal["phone"])
    w(personal["email"])
    linkedin_display = personal["linkedin"].replace("https://", "").replace("http://", "")
    w(f"LinkedIn: {linkedin_display}")
    w("")

    # Summary
    w("SUMMARY")
    w("")
    w(normalize(strip_md_links(summary["statement"])))
    w("")
    for bullet in summary["bullets"]:
        w(f'- {normalize(strip_md_links(bullet))}')
    w("")

    # Skills
    w("SKILLS")
    w("")
    w(", ".join(skills))
    w("")

    # Experience
    w("EXPERIENCE")

    for job_index, job in enumerate(experience):
        w("")
        w(job["title"])
        w(f'{job["company"]} | {job["location"]}')
        w(f'{job["start"]} - {job["end"]}')
        w("")
        if company_details:
            w(normalize(strip_md_links(job["brief"])))
            if job.get("company_stack"):
                w(f'Company Stack: {stack_txt(job["company_stack"])}')
            w("")
        w(normalize(strip_md_links(job["description"])))
        if job.get("description_additional"):
            w("")
            w(normalize(strip_md_links(job["description_additional"])))
        w("")
        for achievement in job["achievements"]:
            w(f'- {normalize(strip_md_links(achievement))}')
        if show_stack:
            w(f'Stack: {stack_txt(job["stack"])}')
        if job_index < len(experience) - 1:
            w("")

    # Education
    w("")
    w("EDUCATION")
    w("")
    for edu in education:
        w(edu["degree"])
        w(f'{edu["institution"]} | {edu["location"]}')
        w(f'GPA: {edu["gpa"]}')
        if edu.get("curriculum"):
            w(f'Curriculum: {edu["curriculum"]}')

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate resume files from a YAML data file.",
    )
    parser.add_argument(
        "data_file",
        metavar="<resume_filename>-data.yaml",
        help="YAML source file; output files are derived by removing '-data.yaml'",
    )
    parser.add_argument(
        "--company-details",
        action="store_true",
        default=False,
        help="include company brief and stack in output (omitted by default)",
    )
    parser.add_argument(
        "--stack",
        action="store_true",
        default=False,
        help="include role stack in output (omitted by default)",
    )
    args = parser.parse_args()

    data_file = Path(args.data_file).resolve()

    data_stem = data_file.stem  # e.g. "Charles_Donaldson_Resume-data"
    if not data_stem.endswith("-data"):
        parser.error(f"data file name must end with '-data.yaml', got: {data_file.name}")

    base_stem = data_stem[: -len("-data")]  # e.g. "Charles_Donaldson_Resume"
    output_base = data_file.parent / base_stem

    with open(data_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    html = build_html(data, company_details=args.company_details, show_stack=args.stack)

    output_file = output_base.with_suffix(".html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_file}")

    # Formatted TXT (printer-friendly, 80-column wrapped)
    formatted_txt_file = output_base.with_name(output_base.name + "-formatted").with_suffix(".txt")
    formatted_txt = build_formatted_txt(data, company_details=args.company_details, show_stack=args.stack)
    with open(formatted_txt_file, "w", encoding="utf-8") as f:
        f.write(formatted_txt)
    print(f"Generated: {formatted_txt_file}")

    # ATS TXT (no line wrapping, no indented continuations)
    ats_txt_file = output_base.with_suffix(".txt")
    ats_txt = build_ats_txt(data, company_details=args.company_details, show_stack=args.stack)
    with open(ats_txt_file, "w", encoding="utf-8") as f:
        f.write(ats_txt)
    print(f"Generated: {ats_txt_file}")

    # PDF via Brave headless
    pdf_file = output_base.with_suffix(".pdf")
    result = subprocess.run(
        [
            BRAVE,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            output_file.as_uri(),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Generated: {pdf_file}")
    else:
        print(f"Error generating PDF:\n{result.stderr}", file=sys.stderr)


if __name__ == "__main__":
    main()
