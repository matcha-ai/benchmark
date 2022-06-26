#pragma once

#include <iostream>
#include <functional>
#include <fstream>
#include <chrono>
#include <filesystem>
#include <cmath>


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

  template <class Iterable>
  void space(const std::function<void (size_t)>& function, 
             const Iterable& iterable,
             size_t n,
             const std::string& name) 
  {
    std::ofstream file(dir_ + name + ".txt");
    for (size_t i = 0; i < n; i++) {
      for (auto&& xscale: iterable) {
        auto scale = (size_t) xscale;
        std::cout << scale << std::endl;
        auto begin = std::chrono::high_resolution_clock::now();
        function(scale);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = end - begin;
        size_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(duration).count();
        double s = (double) ns / 1e9;
        file << scale << " \t " << s << std::endl;
      }
    }
  }

  void linspace(const std::function<void (size_t)>& function,
                size_t low, size_t high,
                size_t points, size_t n,
                const std::string& name)
  {
    std::ofstream file(dir_ + name + ".txt");

    double dhigh = (double) high;
    double dlow = (double) low;
    double dpoints = (double) points;
    double dstep = (dhigh - dlow) / (dpoints - 1);

    for (size_t i = 0; i < n; i++) {
      double dscale = dlow;
      for (size_t j = 0; j < points; j++) {
        size_t scale = (size_t) dscale;
        std::cout << scale << std::endl;
        auto begin = std::chrono::high_resolution_clock::now();
        function(scale);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = end - begin;
        size_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(duration).count();
        double s = (double) ns / 1e9;
        file << scale << " \t " << s << std::endl;
        dscale += dstep;
      }
    }
  }

  void geomspace(const std::function<void (size_t)>& function,
                size_t low, size_t high,
                size_t points, size_t n,
                const std::string& name)
  {
    std::ofstream file(dir_ + name + ".txt");

    double dhigh = (double) high;
    double dlow = (double) low;
    double dpoints = (double) points;
    double dquotient = std::pow(dhigh / dlow, 1. / (dpoints - 1));

    for (size_t i = 0; i < n; i++) {
      double dscale = dlow;
      for (size_t j = 0; j < dpoints; j++) {
        size_t scale = (size_t) dscale;
        std::cout << scale << std::endl;
        auto begin = std::chrono::high_resolution_clock::now();
        function(scale);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = end - begin;
        size_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(duration).count();
        double s = (double) ns / 1e9;
        file << scale << " \t " << s << std::endl;
        dscale *= dquotient;
      }
    }
  }

private:
  std::string target_;
  std::string group_;
  std::string dir_;
};
