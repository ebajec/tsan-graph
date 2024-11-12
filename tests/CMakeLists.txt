cmake_minimum_required(VERSION 3.27)
set(CXX_STANDARD_REQUIRED 17)
project(tests)

add_compile_options( -fsanitize=thread -O2 -g)
add_link_options(-fsanitize=thread)

add_subdirectory(simple)