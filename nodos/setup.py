from setuptools import find_packages, setup

package_name = 'uav_project_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drone_connector = uav_project_pkg.drone_connector:main',
            'video_viewer = uav_project_pkg.video_viewer:main',
            'telemetry_monitor = uav_project_pkg.telemetry_monitor:main',
            'battery_failsafe = uav_project_pkg.battery_failsafe:main',
            'mission_planner = uav_project_pkg.mission_planner:main',
            'object_detector = uav_project_pkg.object_detector:main',
            'custom_mission = uav_project_pkg.custom_mission:main',
            'emergency_stop = uav_project_pkg.emergency_stop:main',
            'gui_controller = uav_project_pkg.gui_controller:main'
        ],
    },
)