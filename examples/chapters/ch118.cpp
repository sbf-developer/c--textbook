// Modern C++ - Chapter 118: Graphs
#include <iostream>
#include <cstddef>
#include <queue>
#include <vector>

int main() {
    const std::vector<std::vector<std::size_t>> graph{{1, 2}, {0, 3}, {0}, {1}};
    std::vector<bool> seen(graph.size());
    std::queue<std::size_t> pending;
    pending.push(0); seen[0] = true;
    while (!pending.empty()) {
        const std::size_t node = pending.front(); pending.pop();
        std::cout << node << " ";
        for (const std::size_t next : graph[node]) if (!seen[next]) { seen[next] = true; pending.push(next); }
    }
    std::cout << "\n";
}
