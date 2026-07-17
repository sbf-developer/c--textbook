#include <iostream>
#include <memory>
#include <utility>

struct Resource {
    explicit Resource(int identifier) : identifier(identifier) {}
    int identifier;
};

std::unique_ptr<Resource> make_resource(int identifier) {
    return std::make_unique<Resource>(identifier);
}

int main() {
    auto owner = make_resource(7);
    auto new_owner = std::move(owner);
    std::cout << new_owner->identifier << '\n';
    std::cout << std::boolalpha << (owner == nullptr) << '\n';
}

