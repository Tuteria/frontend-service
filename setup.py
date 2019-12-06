#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os,re
from setuptools import setup, find_packages

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="frontend-service",
    version=get_version("frontend_service"),
    python_requires=">=3.7",
    license="BSD",
    description="The service hosted on now.sh for handling information from google sheet",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Biola",
    author_email="b33sama@gmail.com",
    packages=get_packages("frontend_service"),
    # package_data={"databases": ["py.typed"]},
    # data_files=[("", ["LICENSE.md"])],
    install_requires=[
        "starlette==0.12.4",
        "websockets==8.0.1",
        'dalchemy @ git+https://github.com/Tuteria/shared_lib.git@master',
    ],
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)