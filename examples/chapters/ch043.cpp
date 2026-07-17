// Modern C++ - Chapter 43: Copy and Move Semantics
#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string original = "resource";
    std::string moved = std::move(original);
    std::cout << moved << "\n";
}
