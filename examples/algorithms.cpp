#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> values{4, 1, 3, 2};
    std::ranges::sort(values);
    const int total = std::accumulate(values.begin(), values.end(), 0);
    const bool contains_three = std::ranges::find(values, 3) != values.end();
    std::cout << total << ' ' << std::boolalpha << contains_three << '\n';
}

