// Modern C++ - Chapter 78: File Input and Output
#include <fstream>
#include <iostream>
#include <string>

int main() {
    const std::string path = "modern_cpp_example.txt";
    { std::ofstream output(path); output << "portable text\n"; }
    std::ifstream input(path);
    std::string line;
    std::getline(input, line);
    std::cout << line << "\n";
}
