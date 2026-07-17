#include <filesystem>
#include <iostream>
#include <system_error>

int main(int argc, char** argv) {
    const std::filesystem::path root = argc > 1 ? argv[1] : ".";
    std::error_code error;
    std::size_t regular_files = 0;
    for (const auto& entry : std::filesystem::recursive_directory_iterator(root, error)) {
        if (error) {
            std::cerr << "directory iteration failed: " << error.message() << '\n';
            return 1;
        }
        if (entry.is_regular_file(error) && !error) {
            ++regular_files;
        }
    }
    if (error) {
        std::cerr << "directory iteration failed: " << error.message() << '\n';
        return 1;
    }
    std::cout << regular_files << '\n';
}

