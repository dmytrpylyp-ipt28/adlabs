cmake_minimum_required(VERSION 3.10)
project(OpenCV_Lab)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS} include)

file(GLOB SOURCES "src/*.cpp")

add_executable(opencv_lab ${SOURCES})
target_link_libraries(opencv_lab ${OpenCV_LIBS})