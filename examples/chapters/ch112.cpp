// Modern C++ - Chapter 112: Sorting
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{9, 4, 7, 1};
    std::sort(values.begin(), values.end());
    std::cout << values.front() << " " << values.back() << "\n";
}
