#include <iostream>
#include <cstddef>
#include <queue>
#include <vector>

std::vector<int> breadth_first_order(const std::vector<std::vector<std::size_t>>& graph, std::size_t start) {
    std::vector<int> order;
    std::vector<bool> visited(graph.size());
    std::queue<std::size_t> pending;
    pending.push(start);
    visited[start] = true;
    while (!pending.empty()) {
        const std::size_t node = pending.front();
        pending.pop();
        order.push_back(static_cast<int>(node));
        for (const std::size_t neighbour : graph[node]) {
            if (!visited[neighbour]) {
                visited[neighbour] = true;
                pending.push(neighbour);
            }
        }
    }
    return order;
}

int main() {
    const std::vector<std::vector<std::size_t>> graph{{1, 2}, {0, 3}, {0}, {1}};
    for (const int node : breadth_first_order(graph, 0)) {
        std::cout << node << ' ';
    }
    std::cout << '\n';
}
