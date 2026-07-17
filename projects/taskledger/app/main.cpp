#include "taskledger/task.hpp"

#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

void log_event(const std::string& path, const std::string& event) {
    std::ofstream log(path, std::ios::app);
    if (log) {
        log << event << '\n';
    }
}

void print_usage(const char* program) {
    std::cerr << "usage: " << program << " DATABASE [list|add TITLE|done ID]\n";
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 2;
    }
    try {
        taskledger::TaskStore store(argv[1]);
        const std::string command = argc >= 3 ? argv[2] : "list";
        const std::string log_path = std::string{argv[1]} + ".log";
        if (command == "list") {
            for (const auto& task : store.list()) {
                std::cout << task.id << "\t" << (task.completed ? "done" : "open") << "\t"
                          << task.title << '\n';
            }
            return 0;
        }
        if (command == "add" && argc >= 4) {
            const int id = store.add(argv[3]);
            log_event(log_path, "add " + std::to_string(id));
            std::cout << id << '\n';
            return 0;
        }
        if (command == "done" && argc >= 4) {
            const bool changed = store.complete(std::stoi(argv[3]));
            log_event(log_path, changed ? "complete" : "complete-missing");
            std::cout << (changed ? "updated" : "not found") << '\n';
            return changed ? 0 : 1;
        }
        print_usage(argv[0]);
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}

