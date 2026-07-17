#include <concepts>
#include <iostream>

template <std::integral T>
T add(T left, T right) {
    return left + right;
}

int main() {
    std::cout << add(20, 22) << '\n';
}

