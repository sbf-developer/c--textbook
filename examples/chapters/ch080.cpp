// Modern C++ - Chapter 80: Filesystem Operations
#include <filesystem>
#include <iostream>

int main() {
    const auto path = std::filesystem::current_path();
    std::cout << path.filename().string() << "\n";
}
