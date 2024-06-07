import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node
import xacro

def generate_robot_description(context, *args, **kwargs):
    # Ottenere i valori delle configurazioni di lancio
    use_sim_time = context.launch_configurations['use_sim_time']
    use_ros2_control = context.launch_configurations['use_ros2_control']
    
    # Processare il file URDF/XACRO
    pkg_path = os.path.join(get_package_share_directory('my_bot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    doc = xacro.process_file(xacro_file, mappings={'use_ros2_control': use_ros2_control, 'sim_mode': use_sim_time})
    robot_description_config = doc.toprettyxml(indent='  ')

    # Creare i parametri del nodo
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}

    # Restituire il nodo robot_state_publisher
    return [Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'
        ),
        OpaqueFunction(function=generate_robot_description)
    ])
