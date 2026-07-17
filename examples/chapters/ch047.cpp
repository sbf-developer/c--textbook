// Modern C++ - Chapter 47: Classes and Objects
#include <iostream>

class Counter {
public:
    void increment() { ++value_; }
    int value() const { return value_; }
private:
    int value_{0};
};

int main() {
    Counter counter;
    counter.increment();
    std::cout << counter.value() << "\n";
}
