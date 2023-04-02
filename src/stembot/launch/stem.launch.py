from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration as LC
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("address", default_value="stembot-phoenix.local", description="Address of the stembot to drive"),
        
        Node(
            package="joy",
            executable="joy_node",
            name="joy_node",
            parameters=[
                {
                    "dev" : "/dev/input/js0",
                    "coalesce_interval" : 0.02,
                    "autorepeat_rate" : 1.0,
                    "default_trig_val" : True
                }
            ]
        ),
        
        Node(
            package="stembot",
            executable="stembot_driver.py",
            name="driver",
            parameters=[
                {
                    "address" : LC("address")
                }
            ]
        )
    ])
