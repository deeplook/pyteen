#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []
this_directory = abspath(dirname(__file__))
with open(join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyteen",
    version="0.0.0",
    description=(
        "Collection of short reusable Python code snippets."
    ),
    long_description_content_type="text/x-rst",
    long_description=long_description,
    author="Dinu Gherman",
    url="https://github.com/deeplook/pyteen",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    setup_requires=[] + pytest_runner,
    tests_require=["pytest"],
    packages=find_packages(exclude=["tests"]),
)
