# Modern C++ — From First Program to Professional Software

This repository contains the publication-ready source, examples, projects, reports, and generated PDF for **Modern C++: From First Program to Professional Software** by Scott Brodie Forsyth.

## Build the book

Requirements: XeLaTeX, `latexmk`, Pygments, `minted`, BibTeX, MakeIndex, Poppler, and a C++23 compiler.

```bash
python3 tools/generate_book.py
bash tools/build_book.sh
python3 tools/qa_pdf.py
```

The final PDF is written to `output/pdf/modern-cpp-book.pdf`.

## Verify the code

```bash
bash tools/verify_examples.sh
```

This compiles all 182 chapter programs plus the standalone hand-written examples as C++23 translation units. The Task Ledger project can also be built directly or through CMake where CMake is installed:

```bash
cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake
ctest --test-dir build/cmake --output-on-failure
```

The book uses C++23 as its baseline. C++26 material is deliberately treated as forward-looking rather than assumed available in every toolchain.

## Repository map

- `chapters/`, `parts/`: generated book source
- `examples/`, `examples/chapters/`: complete compilable examples
- `projects/taskledger/`: end-to-end Task Ledger project
- `docs/`: build, fact-check, verification, and visual-QA reports
- `figures/`: source for the book figures
- `tools/`: generation, build, verification, and QA scripts
- `output/pdf/`: generated PDF
