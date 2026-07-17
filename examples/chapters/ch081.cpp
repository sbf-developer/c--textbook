// Modern C++ - Chapter 81: Function Templates
#include <iostream>

template <typename T>
T maximum(T left, T right) {
    return left < right ? right : left;
}

int main() {
    std::cout << maximum(3, 8) << "\n";
}
