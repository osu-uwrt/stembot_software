cmake_minimum_required(VERSION 2.8.3)
project(stembot_gazebo)

find_package(catkin REQUIRED COMPONENTS gazebo_ros roslaunch)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

add_executable(stembot_gazebo src/stembot_gazebo.cpp)

target_link_libraries(stembot_gazebo ${catkin_LIBRARIES})
