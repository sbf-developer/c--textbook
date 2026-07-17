#pragma once

#include <filesystem>
#include <iosfwd>
#include <string>
#include <vector>

namespace taskledger {

struct Task {
    int id;
    std::string title;
    bool completed;
};

class TaskStore {
public:
    explicit TaskStore(std::filesystem::path database_path);

    int add(std::string title);
    bool complete(int id);
    std::vector<Task> list() const;

private:
    std::filesystem::path database_path_;

    void save(const std::vector<Task>& tasks) const;
    static std::vector<Task> parse(std::istream& input);
};

}  // namespace taskledger
