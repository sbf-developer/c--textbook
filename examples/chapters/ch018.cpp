// Modern C++ - Chapter 18: Repetition with for, while, and do-while
#include <iostream>

int main() {
    int total = 0;
    for (int value = 1; value <= 5; ++value) {
        total += value;
    }
    std::cout << total << "\n";
}
