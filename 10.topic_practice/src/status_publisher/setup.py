from setuptools import find_packages, setup

package_name = 'status_publisher'

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
    maintainer='lxf',
    maintainer_email='2423969470@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sys_status_pub=status_publisher.sys_status_pub:main'
        ],
    },
)
# sys_status_pub (等号左边)
#     这是终端命令名
#     安装包后，你可以在命令行直接运行 sys_status_pub（创建了一个可执行文件）

# status_publisher.sys_status_pub (等号右边，冒号左边)
#     这是Python 模块路径
#     status_publisher 是包名（顶层目录）
#     sys_status_pub 是该包下的 Python 文件名（sys_status_pub.py）

# main (冒号右边)
#     这是入口函数名
#     指向 sys_status_pub.py 文件中的 main() 函数

# 作用：
#     创建可执行脚本：在系统路径中生成一个名为 sys_status_pub 的可执行文件
#     建立映射关系：该可执行文件会自动调用 status_publisher/sys_status_pub.py 中的 main() 