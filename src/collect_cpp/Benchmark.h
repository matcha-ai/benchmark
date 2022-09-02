#include <chrono>
#include <string>
#include <tuple>
#include <vector>
#include <functional>
#include <fstream>
#include <filesystem>

using SizeRange = std::tuple<size_t, size_t, size_t>;

/**
 * @brief named generator wrapper
 */
template <class Internal>
struct Generator {
  Generator(const std::string& name, const Internal& internal)
  : name(name)
  , internal(internal)
  {}

  std::string name;
  Internal internal;
};

/**
 * @brief named payload wrapper
 */
template <class Internal>
struct Payload {
  Payload(const std::string& name, const Internal& internal)
    : name(name)
    , internal(internal)
  {}

  std::string name;
  Internal internal;
};

/**
 * @brief benchmark family wrapper
 */
class Benchmark {
  std::filesystem::path out_dir_;
  std::string engine_;

public:
  explicit Benchmark(const std::string& out_dir, const std::string& engine)
    : out_dir_(out_dir)
    , engine_(engine)
  {}

  /**
   * @brief benchmark payload on pre-generated inputs from a linear space of scales
   * @param range tuple of {begin, end, steps}
   * @param n per-scale sampling
   * @param generator input generator, accepts scale
   * @param payload payload operation, accepts inputs
   */
  template <class Generator, class Payload>
  void linspace(const SizeRange& range,
                size_t n,
                const Generator& generator,
                const Payload& payload)
  {
    std::string name = "linspace " + engine_ + " " + payload.name + " " + generator.name;
    std::ofstream os(out_dir_ / (name + ".txt"));

    for (size_t i = 0; i < n; i++) {
      auto&& [begin, end, samples] = range;
      double increment = (double)(end - begin) / (double)(samples - 1);

      auto b = (double) begin;
      for (size_t j = 0; j < samples; j++) {
        auto scale = (size_t) b;
        auto inputs = generator.internal(scale);

        auto time0 = std::chrono::high_resolution_clock::now();
        payload.internal(inputs);
        auto time1 = std::chrono::high_resolution_clock::now();
        auto duration = time1 - time0;
        size_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(duration).count();

        double seconds = (double) ns / 1e9;
        os << scale << " \t " << seconds << "\n";
        std::cout << scale << " \t " << seconds << "\n";
        b += increment;
      }
    }
  }

};