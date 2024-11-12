cmake_minimum_required(VERSION 3.27)
set(CXX_STANDARD_REQUIRED 17)

# Set output directories for all child projects
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)      # Executables
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)      # Shared libraries
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)      # Static libraries

project(tsan-graph)

add_subdirectory(graph)
add_subdirectory(tests)