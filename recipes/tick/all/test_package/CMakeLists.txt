cmake_minimum_required(VERSION 3.1)
project(test_package)

find_package(tick REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} tick::tick)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)
