import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    nav_pkg_dir = get_package_share_directory('testbed_navigation')
    bringup_pkg_dir = get_package_share_directory('testbed_bringup')

    map_file = os.path.join(bringup_pkg_dir, 'maps', 'testbed_world.yaml')
    amcl_params_file = os.path.join(nav_pkg_dir, 'config', 'amcl_params.yaml')

    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    declare_map_cmd = DeclareLaunchArgument(
        'map', default_value=map_file,
        description='Full path to map yaml file'
    )
    declare_params_cmd = DeclareLaunchArgument(
        'params_file', default_value=amcl_params_file,
        description='Full path to amcl params file'
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': True, 'yaml_filename': map_yaml_file}]
    )

    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[params_file]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['map_server', 'amcl'],
        }]
    )

    return LaunchDescription([
        declare_map_cmd,
        declare_params_cmd,
        map_server_node,
        amcl_node,
        lifecycle_manager_node,
    ])


