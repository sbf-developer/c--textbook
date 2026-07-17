// Modern C++ - Chapter 175: Type Erasure
#include <functional>
#include <iostream>
#include <string>

int main() {
    std::function<std::string()> message = [] { return std::string{"erased"}; };
    std::cout << message() << "\n";
}
