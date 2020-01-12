import glob
import os
from setuptools import setup, find_packages
import warnings


def here(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def load_version():
    version_file = os.path.join(
        os.path.dirname(__file__), "src", "version.py"
    )
    version = {}
    with open(version_file) as fd:
        exec(fd.read(), version)
    return version["__version__"]


def get_readme():
    """Get the README from the current directory. If there isn't one, return an empty string."""
    all_readmes = sorted(glob.glob("README*"))
    if len(all_readmes) > 1:
        warnings.warn(
            "There seems to be more than one README in this directory. Choosing the "
            "first in lexicographic order."
        )
    if all_readmes:
        return open(all_readmes[0], "r").read()
    warnings.warn("There doesn't seem to be a README in this directory.")
    return ""


setup(
    name="atlas-i2c",
    description="Atlas I2C",
    url="https://github.com/timboring/atlas_i2c",
    author="Tim Boring",
    author_email="tim@boring.green",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    version=load_version(),
    long_description="".join(["\n", get_readme()]),
)
