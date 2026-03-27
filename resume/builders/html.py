"""HTML resume builder."""

from .._text_utils import md_links, stack_html


def build_html(data, company_details=False, show_stack=False):
    """Build an HTML resume string from the YAML data dict."""
    personal = data["personal"]
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
    w(f'  <meta name="author" content="{personal["name"]}">')
    w('')
    w(f'  <title>{personal["name"]} Resume</title>')
    w('  <link rel="stylesheet" href="resume.css">')
    w('  <style>')
    w('    @media print { @page { size: letter; margin: 13mm 13mm; } body { margin: 0; } }')
    w('  </style>')
    w('</head>')
    w('')
    w('<body>')
    w(f'  <div class="resume-title">{personal["name"]}</div>')
    w('  <hr />')
    w('  <div class="contact-grid">')
    w(f'    <div>{personal["location"]}</div>')
    w(f'    <div><a href="mailto:{personal["email"]}">{personal["email"]}</a></div>')
    w(f'    <div>{personal["phone"]}</div>')
    linkedin_display = personal["linkedin"].replace("https://", "")
    w(f'    <div><a href="{personal["linkedin"]}">{linkedin_display}</a></div>')
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
        w(f'  {edu["degree"]}')
        w(f'  {edu["institution"]}, {edu["location"]}<br />')

    w('')
    w('</body>')
    w('')
    w('</html>')

    return "\n".join(lines) + "\n"
