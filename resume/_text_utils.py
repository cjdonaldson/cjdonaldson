"""Shared text transformation utilities for resume builders."""

import re


def md_links(text):
    """Convert markdown [text](url) links to HTML <a> tags."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def strip_md_links(text):
    """Strip markdown [text](url) links to plain title text only."""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)


def normalize(text):
    """Collapse all internal whitespace and newlines to single spaces."""
    return " ".join(text.split())


def stack_html(stack):
    """Format pipe-separated stack string with non-breaking spaces."""
    return stack.replace(" | ", " &nbsp; | &nbsp; ")


def nbsp(text):
    """Replace Unicode non-breaking space characters with HTML &nbsp;."""
    return text.replace("\u00a0", "&nbsp;")


def stack_txt(stack):
    """Convert pipe-separated stack string to a comma-separated plain string."""
    return re.sub(r'\s*\|\s*', ', ', stack)
