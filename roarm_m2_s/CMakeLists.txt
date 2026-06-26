cmake_minimum_required(VERSION 3.8)
project(roarm_m2_s)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)

set(dependencies
rclcpp
std_msgs
cv_bridge
sensor_msgs
)

include_directories(
  include
)

add_executable(sub src/sub.cpp)
ament_target_dependencies(sub ${dependencies})

install (

  DIRECTORY roarm_m2_s urdf launch rviz  meshes
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include

)

install(
  TARGETS
  sub
  DESTINATION lib/${PROJECT_NAME}
)

ament_python_install_package(${PROJECT_NAME})

install(
  PROGRAMS
  roarm_m2_s/pub.py
  roarm_m2_s/serial_test.py
  roarm_m2_s/CameraSubscriber.py
  roarm_m2_s/ColourDetection.py
  roarm_m2_s/sendTargetCoordinate.py
  roarm_m2_s/HomePose.py
  roarm_m2_s/PickAndPlace.py
  roarm_m2_s/dum_data.py
  roarm_m2_s/trajectory.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_cmake_pytest REQUIRED)
  find_package(ament_cmake_gtest REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_include_directories(include)

ament_package()
