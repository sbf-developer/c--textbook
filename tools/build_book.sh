#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
python3 tools/generate_book.py
mkdir -p output/pdf tmp/pdfs
latexmk -xelatex -shell-escape -interaction=nonstopmode -halt-on-error \
  -jobname=modern-cpp -outdir=output/pdf book.tex
cp output/pdf/modern-cpp.pdf output/pdf/modern-cpp-book.pdf
echo "built output/pdf/modern-cpp-book.pdf"

