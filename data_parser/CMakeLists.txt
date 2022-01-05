cmake_minimum_required(VERSION 3.19)
project(data_parser)

set(CMAKE_CXX_STANDARD 20)

add_compile_options(-Ofast)

add_executable(data_parser data_parser.cpp)