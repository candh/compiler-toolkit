from setuptools import setup, find_packages
import sys
import os

if sys.version_info.major < 3:
    raise Exception("python3 is required to run this script")

print("Packages Found:", find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="compilertk",
    version="0.12.1",
    description=(
        "Collections of tools useful for syntax analysis part of compiler design"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="candh",
    license="MIT",
    entry_points={"console_scripts": ["compilertk=toolkit.main:main"]},
    url="https://github.com/candh/compiler-toolkit",
    keywords=(
        "compiler toolkit syntax analysis first follow null unit production grammar LL1"
    ),
    install_requires=["colorful", "PyInquirer", "docopt", "tabulate"],
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
    ],
)
