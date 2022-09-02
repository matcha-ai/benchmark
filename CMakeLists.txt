cmake_minimum_required(VERSION 3.21)
project(matcha-benchmark)

set(CMAKE_CXX_STANDARD 20)

add_executable(matcha-benchmark src/collect_cpp/main.cpp)

target_link_libraries(matcha-benchmark matcha)
