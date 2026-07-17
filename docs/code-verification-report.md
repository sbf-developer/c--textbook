# Code-verification report

Date: 2026-07-17  
Compiler: GCC 13.3.0 on Ubuntu 24.04  
Language mode: `-std=c++23`

## Results

- 182 generated chapter translation units compiled.
- 12 hand-written standalone example translation units compiled.
- Total standalone units compiled: 194.
- Warning flags: `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion`.
- Threading flag: `-pthread`.
- Task Ledger library, application, and test executable compiled directly.
- Task Ledger unit tests passed.
- Task Ledger add/list/complete workflow passed in a temporary database.
- AddressSanitizer/UndefinedBehaviorSanitizer runs were executed for the
  ownership, concurrency, and Task Ledger paths without a reported failure.
  LeakSanitizer was disabled for these runs because the production container
  runs under tracing, which prevents LeakSanitizer from inspecting `/proc`.

## Reproduction

`
bash tools/verify_examples.sh
g++ -std=c++23 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion \
  -Iprojects/taskledger/include \
  projects/taskledger/src/task.cpp projects/taskledger/tests/test_task.cpp \
  -o /tmp/taskledger_tests
/tmp/taskledger_tests
`

The repository also includes CMake targets for the hand-written examples and
the Task Ledger project, plus a CTest target for the generated standalone
programs on POSIX-like systems.

## Environment limitations

CMake and Clang were not installed in the production workspace, so their
commands were included and checked structurally but not executed here.
Windows and macOS runners are covered by the CI workflow rather than claimed as
local test results. `cppcheck` was unavailable locally; compiler warnings
and AddressSanitizer/UndefinedBehaviorSanitizer runs were used instead.
