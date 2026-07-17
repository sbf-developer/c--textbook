// Modern C++ - Chapter 58: Runtime Polymorphism
#include <iostream>
#include <memory>
#include <vector>

struct Shape {
    virtual ~Shape() = default;
    virtual int area() const = 0;
};
struct Square final : Shape {
    explicit Square(int side) : side(side) {}
    int area() const override { return side * side; }
    int side;
};

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Square>(5));
    std::cout << shapes.front()->area() << "\n";
}
