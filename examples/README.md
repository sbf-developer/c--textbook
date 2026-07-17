# Standalone examples

Every `examples/*.cpp` file is a complete C++23 translation unit. The
generated `examples/chapters/chNNN.cpp` files are the complete micro-program
embedded in the corresponding chapter. They are intentionally small so that a
reader can compile one file while learning a single concept.

Compile one example directly:

```sh
g++ -std=c++23 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion \
  -O2 examples/calculator.cpp -o /tmp/calculator
/tmp/calculator
```

The repository-level verification script compiles all examples and runs the
deterministic ones. The generated programs are not a substitute for the
larger multi-file `projects/taskledger` application; the two layers are meant
to support different stages of learning.

