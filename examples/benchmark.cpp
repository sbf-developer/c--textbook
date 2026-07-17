#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    constexpr int repetitions = 1000;
    std::vector<int> values(1000, 1);
    const auto start = std::chrono::steady_clock::now();
    long long total = 0;
    for (int repetition = 0; repetition < repetitions; ++repetition) {
        total += std::accumulate(values.begin(), values.end(), 0LL);
    }
    const auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now() - start);
    std::cout << total << ' ' << elapsed.count() << " us\n";
}

