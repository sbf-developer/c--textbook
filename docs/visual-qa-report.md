# Visual quality-assurance report

Date: 2026-07-17  
PDF: `output/pdf/modern-cpp-book.pdf`

## Automated checks

- XeLaTeX build completed with `-shell-escape`.
- Final PDF contains 429 A4 pages.
- `pdfinfo` reports the expected title and author.
- `pdftotext` confirms the first and last chapters, bibliography, and index.
- Final LaTeX log contains no `Overfull`, `Underfull`,
  undefined-reference, undefined-citation, or font-shape warnings.

## Rendered inspection

Rendered PNG samples were inspected for:

- cover and title hierarchy;
- standards/citation page;
- table-of-contents leaders and chapter numbering;
- early, middle, and late chapter pages;
- the Part I translation-pipeline figure;
- bibliography/index ending pages.

No clipped text, overlapping boxes, broken code blocks, decorative clutter, or
elements extending beyond the page margins were observed. The cover uses one
solid color bar, restrained typography, and no circles, gradients, or
overlapping lines.

## Reproduction

`
python3 tools/qa_pdf.py
pdftoppm -f 1 -l 12 -png -r 120 \
  output/pdf/modern-cpp-book.pdf tmp/pdfs/rendered/page
`
