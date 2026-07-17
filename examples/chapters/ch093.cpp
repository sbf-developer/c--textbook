// Modern C++ - Chapter 93: Exceptions
#include <iostream>
#include <stdexcept>

int divide(int numerator, int denominator) {
    if (denominator == 0) { throw std::invalid_argument{"zero denominator"}; }
    return numerator / denominator;
}

int main() {
    try { std::cout << divide(8, 2) << "\n"; }
    catch (const std::exception& error) { std::cerr << error.what() << "\n"; return 1; }
}
