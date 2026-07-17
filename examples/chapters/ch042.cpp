// Modern C++ - Chapter 42: RAII
#include <iostream>
#include <string>
#include <utility>

class Message {
public:
    explicit Message(std::string text) : text_(std::move(text)) {
        std::cout << "acquired\n";
    }
    ~Message() { std::cout << "released\n"; }
private:
    std::string text_;
};

int main() {
    Message message{"RAII"};
}
