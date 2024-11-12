cmake_minimum_required(VERSION 3.27)
set(CXX_STANDARD_REQUIRED 17)

project(simple-race)

add_executable(simple-race)

target_sources(simple-race PRIVATE main.cpp)

