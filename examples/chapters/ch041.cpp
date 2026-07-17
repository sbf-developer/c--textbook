// Modern C++ - Chapter 41: Smart Pointers
#include <iostream>
#include <memory>

int main() {
    auto value = std::make_unique<int>(42);
    std::cout << *value << "\n";
}
