# Technical fact-check report

Date: 2026-07-17  
Book baseline: C++23  
Author: Scott Brodie Forsyth

## Verified baseline

The book uses C++23 as its portable baseline. The Standard C++ Foundation
identifies the current published standard as ISO/IEC 14882:2024(E), commonly
called C++23 because the technical work completed in 2023. The same source
describes C++26 as work in progress. The book therefore labels C++26 material
as non-baseline and does not require draft-only facilities.

## Source hierarchy

Claims about standard status were checked against the Standard C++ Foundation
and ISO metadata. Compiler support claims are intentionally phrased as
feature-by-feature and point to the current GCC, Clang, and Microsoft
conformance tables. Build-system claims point to current CMake documentation.
The bibliography preserves URLs and access dates.

Primary and authoritative sources used:

- ISO/IEC 14882:2024 metadata: <https://www.iso.org/standard/83626.html>
- Standard C++ - current standard: <https://isocpp.org/std/the-standard>
- Standard C++ - status: <https://isocpp.org/std/status>
- GCC C++ status: <https://gcc.gnu.org/projects/cxx-status.html>
- Clang C++ status: <https://clang.llvm.org/cxx_status.html>
- Microsoft conformance table: <https://learn.microsoft.com/en-us/cpp/overview/visual-cpp-language-conformance>
- CMake documentation: <https://cmake.org/cmake/help/latest/>
- C++ Core Guidelines: <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>

## Editorial distinctions enforced

- Standard requirements are not presented as universal machine-layout facts.
- Common implementation behavior is labelled as typical.
- Platform-specific commands and ABI behavior are treated as conditional.
- Performance claims are framed as hypotheses to measure, not guarantees.
- Draft C++26 proposals are separated from C++23 examples.
- Raw pointers are introduced as possible observers; ownership is taught through
  RAII and smart pointers.

## Scope note

The fact-check covers the claims and references in this generated edition. A
future edition should rerun the compiler-status checks because vendor support,
standard defect resolutions, and C++26 status can change.

