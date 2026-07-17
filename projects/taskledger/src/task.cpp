#include "taskledger/task.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>
#include <utility>

namespace taskledger {

namespace {

bool contains_record_separator(const std::string& title) {
    return title.find('\t') != std::string::npos || title.find('\n') != std::string::npos ||
           title.find('\r') != std::string::npos;
}

}  // namespace

TaskStore::TaskStore(std::filesystem::path database_path)
    : database_path_(std::move(database_path)) {}

std::vector<Task> TaskStore::parse(std::istream& input) {
    std::vector<Task> tasks;
    std::string line;
    while (std::getline(input, line)) {
        std::istringstream row(line);
        std::string id_text;
        std::string completed_text;
        std::string title;
        if (!std::getline(row, id_text, '\t') || !std::getline(row, completed_text, '\t') ||
            !std::getline(row, title)) {
            throw std::runtime_error{"invalid task record"};
        }
        try {
            const int id = std::stoi(id_text);
            if (completed_text != "0" && completed_text != "1") {
                throw std::runtime_error{"invalid completion flag"};
            }
            tasks.push_back(Task{id, title, completed_text == "1"});
        } catch (const std::invalid_argument&) {
            throw std::runtime_error{"invalid task identifier"};
        } catch (const std::out_of_range&) {
            throw std::runtime_error{"task identifier out of range"};
        }
    }
    return tasks;
}

std::vector<Task> TaskStore::list() const {
    if (!std::filesystem::exists(database_path_)) {
        return {};
    }
    std::ifstream input(database_path_);
    if (!input) {
        throw std::runtime_error{"could not open task database for reading"};
    }
    return parse(input);
}

void TaskStore::save(const std::vector<Task>& tasks) const {
    const auto temporary_path = database_path_.string() + ".tmp";
    std::ofstream output(temporary_path, std::ios::trunc);
    if (!output) {
        throw std::runtime_error{"could not open task database for writing"};
    }
    for (const Task& task : tasks) {
        output << task.id << '\t' << (task.completed ? 1 : 0) << '\t' << task.title << '\n';
    }
    output.close();
    if (!output) {
        throw std::runtime_error{"could not write task database"};
    }
    std::error_code error;
    std::filesystem::rename(temporary_path, database_path_, error);
    if (error) {
        std::filesystem::remove(temporary_path);
        throw std::runtime_error{"could not replace task database: " + error.message()};
    }
}

int TaskStore::add(std::string title) {
    if (title.empty() || contains_record_separator(title)) {
        throw std::invalid_argument{"title must be non-empty and contain no tabs or newlines"};
    }
    auto tasks = list();
    int next_id = 1;
    for (const Task& task : tasks) {
        if (task.id >= next_id) {
            next_id = task.id + 1;
        }
    }
    tasks.push_back(Task{next_id, std::move(title), false});
    save(tasks);
    return next_id;
}

bool TaskStore::complete(int id) {
    auto tasks = list();
    for (Task& task : tasks) {
        if (task.id == id) {
            task.completed = true;
            save(tasks);
            return true;
        }
    }
    return false;
}

}  // namespace taskledger

