import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    nav_pkg_dir = get_package_share_directory('testbed_navigation')
    nav2_params_file = os.path.join(nav_pkg_dir, 'config', 'nav2_params.yaml')

    params_file = LaunchConfiguration('params_file')

    declare_params_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=nav2_params_file,
        description='Full path to nav2 params file'
    )

    controller_server_node = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        parameters=[params_file]
    )

    planner_server_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[params_file]
    )

    recoveries_server_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='recoveries_server',
        output='screen',
        parameters=[params_file]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[params_file]
    )

    waypoint_follower_node = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[params_file]
    )

    velocity_smoother_node = Node(
        package='nav2_velocity_smoother',
        executable='velocity_smoother',
        name='velocity_smoother',
        output='screen',
        parameters=[params_file]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': [
                'controller_server',
                'planner_server',
                'recoveries_server',
                'bt_navigator',
                'waypoint_follower',
                'velocity_smoother',
            ],
        }]
    )

    return LaunchDescription([
        declare_params_cmd,
        controller_server_node,
        planner_server_node,
        recoveries_server_node,
        bt_navigator_node,
        waypoint_follower_node,
        velocity_smoother_node,
        lifecycle_manager_node,
    ])
