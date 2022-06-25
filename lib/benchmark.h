#pragma once

#include <iostream>
#include <functional>
#include <fstream>
#include <chrono>
#include <filesystem>


class Benchmark {
public:
  Benchmark(const std::string& group, const std::string& target = ".") {
    target_ = target;
    if (target_.empty()) target_ += '.';
    if (target_.back() != '/') target_ += '/';

    if (!std::filesystem::is_directory(target_))
      throw std::invalid_argument("target path is not a directory");

    group_ = group;

    dir_ = target_ + group;
    if (dir_.back() != '/') dir_ += '/';

    std::filesystem::create_directories(dir_);
  }

  void run(const std::function<void ()>& function, size_t n, const std::string& name) {
    std::ofstream file(dir_ + name + ".txt");
    for (size_t i = 0; i < n; i++) {
      auto begin = std::chrono::high_resolution_clock::now();
      function();
      auto end = std::chrono::high_resolution_clock::now();
      auto duration = end - begin;
      size_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(duration).count();
      double s = (double) ns / 1e9;
      file << s << std::endl;
    }
  }

private:
  std::string target_;
  std::string group_;
  std::string dir_;
};
