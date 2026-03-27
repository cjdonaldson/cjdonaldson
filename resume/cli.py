"""CLI entry point and orchestration for resume generation."""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

from .builders.html import build_html
from .builders.formatted_txt import build_formatted_txt
from .builders.ats_txt import build_ats_txt
from .pdf import generate_pdf


def main():
    """Parse arguments, load YAML, and generate all resume output files."""
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

    with open(data_file, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)

    html_content = build_html(
        data,
        company_details=args.company_details,
        show_stack=args.stack,
    )
    html_file = output_base.with_suffix(".html")
    with open(html_file, "w", encoding="utf-8") as output_file:
        output_file.write(html_content)
    print(f"Generated: {html_file}")

    # Formatted TXT (printer-friendly, 80-column wrapped)
    formatted_txt_file = output_base.with_name(output_base.name + "-formatted").with_suffix(".txt")
    formatted_txt_content = build_formatted_txt(
        data,
        company_details=args.company_details,
        show_stack=args.stack,
    )
    with open(formatted_txt_file, "w", encoding="utf-8") as output_file:
        output_file.write(formatted_txt_content)
    print(f"Generated: {formatted_txt_file}")

    # ATS TXT (no line wrapping, no indented continuations)
    ats_txt_file = output_base.with_suffix(".txt")
    ats_txt_content = build_ats_txt(
        data,
        company_details=args.company_details,
        show_stack=args.stack,
    )
    with open(ats_txt_file, "w", encoding="utf-8") as output_file:
        output_file.write(ats_txt_content)
    print(f"Generated: {ats_txt_file}")

    # PDF via Brave headless
    pdf_file = output_base.with_suffix(".pdf")
    generate_pdf(html_file=html_file, pdf_file=pdf_file)
