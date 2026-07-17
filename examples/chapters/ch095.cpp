// Modern C++ - Chapter 95: Expected-Style Error Handling
#include <iostream>
#include <string>
#include <type_traits>
#include <variant>

struct Error { std::string message; };
using Result = std::variant<int, Error>;

Result parse_positive(int value) {
    if (value < 0) return Error{"negative value"};
    return value;
}

int main() {
    const Result result = parse_positive(4);
    std::visit([](const auto& value) {
        if constexpr (std::is_same_v<std::decay_t<decltype(value)>, Error>) std::cout << value.message << "\n";
        else std::cout << value << "\n";
    }, result);
}
