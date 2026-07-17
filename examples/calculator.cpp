#include <charconv>
#include <iostream>
#include <stdexcept>
#include <string_view>

int parse_integer(std::string_view text) {
    int value = 0;
    const auto result = std::from_chars(text.data(), text.data() + text.size(), value);
    if (result.ec != std::errc{} || result.ptr != text.data() + text.size()) {
        throw std::invalid_argument{"not an integer"};
    }
    return value;
}

int main() {
    try {
        const int left = parse_integer("18");
        const int right = parse_integer("24");
        std::cout << left + right << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
