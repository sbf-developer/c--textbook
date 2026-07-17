# Task Ledger

Task Ledger is the book's small multi-file capstone. It stores tasks as a
portable tab-separated text file, uses a library boundary for domain behavior,
offers a command-line front end, writes a minimal event log, and has a test
executable. The storage format is intentionally simple so readers can inspect
it with an ordinary editor.

## Build

From this directory:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

Run the program:

```sh
./build/taskledger taskledger.db add "read a chapter"
./build/taskledger taskledger.db list
./build/taskledger taskledger.db done 1
```

The project uses only the C++ standard library. Its on-disk format is a
teaching format, not a concurrency-safe database: two processes writing the
same file concurrently are outside its contract.

