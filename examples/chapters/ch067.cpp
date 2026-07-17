// Modern C++ - Chapter 67: Algorithms
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{4, 1, 3, 2};
    std::sort(values.begin(), values.end());
    for (const int value : values) { std::cout << value << " "; }
    std::cout << "\n";
}
