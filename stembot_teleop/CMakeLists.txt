cmake_minimum_required(VERSION 2.8.3)
project(stembot_teleop)

find_package(catkin REQUIRED COMPONENTS joy)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

add_executable(stembot_teleop src/stembot_teleop.cpp)

target_link_libraries(stembot_teleop ${catkin_LIBRARIES})
