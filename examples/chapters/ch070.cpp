// Modern C++ - Chapter 70: Lambda Expressions
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> values{1, 2, 3, 4};
    const auto even = std::count_if(values.begin(), values.end(), [](int value) {
        return value % 2 == 0;
    });
    std::cout << even << "\n";
}
