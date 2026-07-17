// Modern C++ - Chapter 143: Processes and Threads
#include <iostream>
#include <thread>

int main() {
    std::jthread worker([] { std::cout << "worker\n"; });
    std::cout << "main\n";
}
