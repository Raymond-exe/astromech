cmake_minimum_required(VERSION 3.25)
project(Astromech)

set(CMAKE_CXX_STANDARD 23)

find_package(PiPCA9685 REQUIRED)

add_executable(astromech-cpp src/main.cpp)
target_link_libraries(astromech-cpp PiPCA9685::PiPCA9685)
