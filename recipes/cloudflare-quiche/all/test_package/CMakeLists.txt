cmake_minimum_required(VERSION 3.24)
project(PackageTest CXX)

if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS "6")
  message(FATAL_ERROR "The current GCC version is ${CMAKE_CXX_COMPILER_VERSION}, however, we only support GCC 6 and newer versions")
elseif (CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL "7")
  set(CMAKE_CXX_STANDARD 17)
  message(STATUS "Current GCC version: ${CMAKE_CXX_COMPILER_VERSION}, so using C++17.")
else()
  # The GCC version is not less than 6, nor 7 or greater, so it should be GCC 6, which means, C++14
  set(CMAKE_CXX_STANDARD 14)
  message(STATUS "Current GCC version: ${CMAKE_CXX_COMPILER_VERSION}, so using C++14.")
endif()

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(cloudflare-quiche REQUIRED)

add_executable(test-server server.cpp)
target_link_libraries(test-server PRIVATE cloudflare-quiche::cloudflare-quiche)
