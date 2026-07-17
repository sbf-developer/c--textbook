// Modern C++ - Chapter 149: Atomic Operations
#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<int> count{0};
    std::jthread first([&] { for (int i = 0; i < 1000; ++i) ++count; });
    std::jthread second([&] { for (int i = 0; i < 1000; ++i) ++count; });
    first.join(); second.join();
    std::cout << count.load() << "\n";
}
