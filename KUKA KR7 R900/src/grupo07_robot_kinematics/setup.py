from setuptools import find_packages, setup

package_name = 'grupo07_robot_kinematics'

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
    maintainer='alex',
    maintainer_email='gutierrezjhamil556@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fk_node = grupo07_robot_kinematics.fk_node:main',
            'ik_node = grupo07_robot_kinematics.ik_node:main',
            'target_gui = grupo07_robot_kinematics.target_gui_node:main',
        ],
    },
)
