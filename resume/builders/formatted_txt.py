"""Printer-friendly formatted TXT resume builder (80-column wrapped)."""

import textwrap

from .._text_utils import strip_md_links, stack_txt

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


def build_formatted_txt(data, company_details=False, show_stack=False):
    """Build a printer-friendly 80-column wrapped plain-text resume."""
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
    w(join_items_no_break(skills))
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
        # if edu.get("curriculum"):
        #     w(f'Curriculum: {edu["curriculum"]}')

    return "\n".join(lines) + "\n"
