# Dependency and tool versions

Production verification used:

| Tool | Version / status |
|---|---|
| Python | 3.12.13 |
| GCC | 13.3.0 |
| XeLaTeX | TeX Live 2023, XeTeX 3.141592653 |
| latexmk | 4.83 |
| Pygments | system `pygmentize` |
| Poppler | 26.05.0 |
| CMake | not installed locally; required by project reproduction |
| Clang | not installed locally; covered by CI configuration |
| cppcheck | not installed locally |

The LaTeX source uses standard TeX Live packages including `fontspec`,
`microtype`, `tcolorbox`, `minted`, `natbib`, `hyperref`,
`tocloft`, TikZ, and `imakeidx`. The C++ examples use only the C++
standard library.

