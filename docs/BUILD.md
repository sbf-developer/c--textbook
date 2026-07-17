# Reproduction and verification

## Requirements

- Python 3.10 or newer.
- XeLaTeX, `minted`, Pygments, BibTeX, and `makeindex`.
- A C++23 compiler. The production environment used GCC 13.3.0.
- CMake 3.23 or newer for the multi-file project.
- Poppler's `pdftoppm` and `pdfinfo` for PDF QA.

## Rebuild the sources

`
python3 tools/generate_book.py
`

This deterministically regenerates 182 chapter files, 182 chapter programs,
the part introductions, the include manifest, and the book manifest.

## Verify C++

`
bash tools/verify_examples.sh
cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --parallel
ctest --test-dir build/cmake --output-on-failure
`

For sanitizers on GCC or Clang:

`
cmake -S projects/taskledger -B build/taskledger-sanitized \
  -DCMAKE_CXX_FLAGS='-fsanitize=address,undefined -fno-omit-frame-pointer -g'
cmake --build build/taskledger-sanitized --parallel
ctest --test-dir build/taskledger-sanitized --output-on-failure
`

ThreadSanitizer is a separate run because sanitizer combinations are
toolchain-dependent:

`
cmake -S . -B build/tsan -DCMAKE_CXX_FLAGS='-fsanitize=thread -g'
cmake --build build/tsan --parallel
`

## Build the PDF

`
bash tools/build_book.sh
`

The final PDF is written to `output/pdf/modern-cpp-book.pdf`. `minted`
requires `-shell-escape` so XeLaTeX can invoke Pygments; use a clean,
trusted checkout when enabling it.

## Render and inspect

`
pdfinfo output/pdf/modern-cpp-book.pdf
mkdir -p tmp/pdfs/rendered
pdftoppm -f 1 -l 12 -png -r 120 output/pdf/modern-cpp-book.pdf tmp/pdfs/rendered/page
`

The QA script checks page count, extracted text, overfull-box warnings, and a
sample of rendered pages. Visual review remains necessary for a publication
artifact; the final report records the inspected pages and any limitations.

