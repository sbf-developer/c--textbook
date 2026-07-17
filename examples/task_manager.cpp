#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

struct Task {
    int id;
    std::string title;
    bool done{false};
};

class TaskManager {
public:
    int add(std::string title) {
        const int id = next_id_++;
        tasks_.push_back(Task{id, std::move(title)});
        return id;
    }

    bool complete(int id) {
        const auto found = std::ranges::find(tasks_, id, &Task::id);
        if (found == tasks_.end()) {
            return false;
        }
        found->done = true;
        return true;
    }

    void print() const {
        for (const Task& task : tasks_) {
            std::cout << task.id << ". [" << (task.done ? 'x' : ' ') << "] "
                      << task.title << '\n';
        }
    }

private:
    int next_id_{1};
    std::vector<Task> tasks_;
};

int main() {
    TaskManager manager;
    const int first = manager.add("read a chapter");
    manager.add("write a test");
    manager.complete(first);
    manager.print();
}
