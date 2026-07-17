// Modern C++ - Chapter 35: Pointers
#include <iostream>

int main() {
    int value = 42;
    int* pointer = &value;
    if (pointer != nullptr) {
        std::cout << *pointer << "\n";
    }
}
