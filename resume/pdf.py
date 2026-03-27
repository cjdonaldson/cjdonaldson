"""PDF generation via Brave headless browser."""

import subprocess
import sys
from pathlib import Path

BRAVE = "/usr/bin/brave"


def generate_pdf(html_file: Path, pdf_file: Path) -> None:
    """Render html_file to pdf_file using Brave in headless mode."""
    result = subprocess.run(
        [
            BRAVE,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            html_file.as_uri(),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Generated: {pdf_file}")
    else:
        print(f"Error generating PDF:\n{result.stderr}", file=sys.stderr)
