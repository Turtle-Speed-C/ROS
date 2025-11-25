from setuptools import find_packages, setup

package_name = "demo_python_service"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            "share/" + package_name + "/resource",
            ["resource/default.jpg", "resource/test1.jpg", "resource/test2.jpg"],
        ),
        # "share/" + package_name + "/resource"把文件放置在install下面的share的resource
        # ["resource/default.jpg"]的意思是原文件
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="lxf",
    maintainer_email="2423969470@qq.com",
    description="TODO: Package description",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "face_detect=demo_python_service.face_detect:main",
            # face_detect:指的是可执行文件的名字
            # demo_python_service包名
            # face_detect文件名
            "face_detect_node=demo_python_service.face_detect_node:main",
            "face_detect_client_node=demo_python_service.face_detect_client_node:main",
            "face_detect_client_two_node=demo_python_service.face_detect_client_two_node:main",
            "face_detect_client_thread=demo_python_service.face_detect_client_thread:main",
        ],
    },
)
