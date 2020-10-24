#!/usr/bin/env python
# Motherstarter setup file
from setuptools import setup, find_packages
from motherstarter import __version__, __author__

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setup(
    author_email="danielfjteycheney@gmail.com",
    description="Network automation inventory data translation tool.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/writememe/motherstarter",
    name="motherstarter",
    version=__version__,
    author=__author__,
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        motherstarter=motherstarter.motherstarter:cli
    """,
)
