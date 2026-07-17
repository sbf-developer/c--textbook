#include <iostream>
#include <memory>
#include <numbers>
#include <vector>

struct Shape {
    virtual ~Shape() = default;
    virtual double area() const = 0;
};

struct Circle final : Shape {
    explicit Circle(double radius) : radius(radius) {}
    double area() const override { return std::numbers::pi * radius * radius; }
    double radius;
};

struct Rectangle final : Shape {
    Rectangle(double width, double height) : width(width), height(height) {}
    double area() const override { return width * height; }
    double width;
    double height;
};

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(2.0));
    shapes.push_back(std::make_unique<Rectangle>(3.0, 4.0));
    double total = 0.0;
    for (const auto& shape : shapes) {
        total += shape->area();
    }
    std::cout << total << '\n';
}

