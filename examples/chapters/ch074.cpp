// Modern C++ - Chapter 74: Optional Values and Variants
#include <iostream>
#include <variant>
#include <string>

int main() {
    std::variant<int, std::string> result = std::string{"ready"};
    std::visit([](const auto& value) { std::cout << value << "\n"; }, result);
}
