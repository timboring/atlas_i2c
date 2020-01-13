import glob
import os
from setuptools import setup, find_packages
import warnings


def here(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def load_version():
    version_file = os.path.join(os.path.dirname(__file__), "src", "version.py")
    version = {}
    with open(version_file) as fd:
        exec(fd.read(), version)
    return version["__version__"]


def long_description():
    with open("README.md", "r") as fd:
        return fd.read()


setup(
    name="atlas-i2c",
    description="Atlas I2C",
    url="https://github.com/timboring/atlas_i2c",
    author="Tim Boring",
    author_email="tim@boring.green",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    py_modules=["atlas_i2c"],
    python_requires=">=3.6",
    version=load_version(),
    long_description=long_description(),
    long_description_content_type="text/markdown",
)
