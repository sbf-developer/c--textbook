#include <cctype>
#include <iostream>
#include <map>
#include <string>
#include <string_view>

std::map<char, int> letter_counts(std::string_view text) {
    std::map<char, int> counts;
    for (const char raw_character : text) {
        const auto character = static_cast<unsigned char>(raw_character);
        if (std::isalpha(character) != 0) {
            ++counts[static_cast<char>(std::tolower(character))];
        }
    }
    return counts;
}

int main() {
    const auto counts = letter_counts("Portable C++ text");
    for (const auto& [letter, count] : counts) {
        std::cout << letter << ':' << count << ' ';
    }
    std::cout << '\n';
}
