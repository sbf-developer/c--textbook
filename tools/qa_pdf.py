#!/usr/bin/env python3
"""Small, deterministic PDF QA checks used for the release report."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "modern-cpp-book.pdf"
LOG = ROOT / "output" / "pdf" / "modern-cpp.log"


def command(*args: str) -> str:
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"missing PDF: {PDF}")
    info = command("pdfinfo", str(PDF))
    pages_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    pages = int(pages_match.group(1)) if pages_match else 0
    text = command("pdftotext", "-layout", str(PDF), "-")
    checks = {
        "title": "MODERN C++" in text,
        "author": "Scott Brodie Forsyth" in text,
        "chapter_1": "What a Computer Program Is" in text,
        "chapter_182": "Legacy-Code Modernization" in text,
        "bibliography": "The C++ Programming Language" in text,
        "index": "Virtual Functions" in text,
        "reasonable_page_count": pages >= 400,
    }
    if LOG.exists():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        checks["final_log_has_no_layout_errors"] = not bool(
            re.search(r"Overfull|Underfull|undefined references|Citation .*undefined|Font Warning", log)
        )
    else:
        checks["final_log_has_no_layout_errors"] = False
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"pages={pages}")
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()

