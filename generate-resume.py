#!/usr/bin/env python3
"""Generate Charles_Donaldson_Resume.html (and .pdf) from resume_data.yaml."""

import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

BRAVE = "/usr/bin/brave"


def md_links(text):
    """Convert markdown [text](url) links to HTML <a> tags."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def stack_html(stack):
    """Format pipe-separated stack string with non-breaking spaces."""
    return stack.replace(" | ", " &nbsp; | &nbsp; ")


def nbsp(text):
    """Replace a bare space before non-breaking space markers in jbrief."""
    return text.replace("\u00a0", "&nbsp;")


def build_html(data):
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
        w(f'    <brief>')
        w(f'      {job["brief"].strip()}')
        w(f'    </brief>')
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


def main():
    script_dir = Path(__file__).parent
    data_file = script_dir / "resume_data.yaml"
    output_file = script_dir / "Charles_Donaldson_Resume.html"

    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])

    data_file = data_file.resolve()
    output_file = output_file.resolve()

    with open(data_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    html = build_html(data)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_file}")

    # PDF via Brave headless
    pdf_file = output_file.with_suffix(".pdf")
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
