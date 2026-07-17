#include <iostream>
#include <string>
#include <type_traits>
#include <variant>

struct ParseError {
    std::string message;
};

using ParseResult = std::variant<int, ParseError>;

ParseResult parse_positive(int value) {
    if (value < 0) {
        return ParseError{"value must be non-negative"};
    }
    return value;
}

int main() {
    const ParseResult result = parse_positive(12);
    std::visit([](const auto& value) {
        if constexpr (std::is_same_v<std::decay_t<decltype(value)>, ParseError>) {
            std::cerr << value.message << '\n';
        } else {
            std::cout << value << '\n';
        }
    }, result);
}
