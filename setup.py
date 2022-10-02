import os
from setuptools import setup, find_packages


def dependences():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    requirements = os.path.join(package_dir, "requirements.txt")
    package_dep = []
    if os.path.isfile(requirements):
        with open(requirements, mode="r") as file:
            package_dep = file.read().splitlines()
    return package_dep


def version():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    version_file = os.path.join(package_dir, "cgiserver", "__version__.py")
    result = {}
    with open(version_file, mode="r") as file:
        exec(file.read(), result)
    return result["__version__"]


setup(
    name="cgi-server",
    version=version(),
    author="zengqunhong; xuzheyuan; luxinbo;",
    author_email="zengqunhong@gmail.com",
    description="multi thread cgi server using python3",
    url="https://github.com/0x404/cgi-server",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=dependences(),
)
