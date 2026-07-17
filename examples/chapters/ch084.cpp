// Modern C++ - Chapter 84: Concepts and Constraints
#include <concepts>
#include <iostream>

template <std::integral T>
T add(T left, T right) { return left + right; }

int main() {
    std::cout << add(2, 3) << "\n";
}
