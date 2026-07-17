#include "taskledger/task.hpp"

#include <cassert>
#include <filesystem>
#include <stdexcept>

int main() {
    const auto path = std::filesystem::temp_directory_path() / "modern_cpp_taskledger_test.db";
    std::error_code cleanup_error;
    std::filesystem::remove(path, cleanup_error);

    taskledger::TaskStore store(path);
    assert(store.list().empty());
    const int first_id = store.add("learn ownership");
    const int second_id = store.add("write tests");
    assert(first_id == 1);
    assert(second_id == 2);
    assert(store.complete(first_id));
    assert(!store.complete(999));

    const auto tasks = store.list();
    assert(tasks.size() == 2);
    assert(tasks[0].completed);
    assert(!tasks[1].completed);

    bool rejected = false;
    try {
        store.add("bad\ttitle");
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    assert(rejected);
    std::filesystem::remove(path, cleanup_error);
}

