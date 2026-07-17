#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    int count = 0;
    std::mutex guard;
    std::vector<std::jthread> workers;
    for (int worker = 0; worker < 4; ++worker) {
        workers.emplace_back([&] {
            for (int step = 0; step < 1000; ++step) {
                const std::scoped_lock lock(guard);
                ++count;
            }
        });
    }
    for (auto& worker : workers) {
        worker.join();
    }
    std::cout << count << '\n';
}

