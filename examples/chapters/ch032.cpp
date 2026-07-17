// Modern C++ - Chapter 32: std::vector
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> values{2, 4, 6, 8};
    for (const int value : values) {
        std::cout << value << " ";
    }
    std::cout << "\n";
}
