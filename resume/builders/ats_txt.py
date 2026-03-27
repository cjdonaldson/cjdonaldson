"""ATS-ingest TXT resume builder: no line wrapping, no indented continuations."""

from .._text_utils import normalize, strip_md_links, stack_txt


def build_ats_txt(data, company_details=False, show_stack=False):
    """Build an ATS-ingest plain-text resume with no wrapping or indentation."""
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
        # if edu.get("curriculum"):
        #     w(f'Curriculum: {edu["curriculum"]}')

    return "\n".join(lines) + "\n"
