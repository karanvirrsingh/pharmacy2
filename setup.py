"""Package setup for AI Drug Interaction Checker."""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="drug-interaction-checker",
    version="1.0.0",
    author="pharmacy2 contributors",
    description="AI-powered Drug Interaction Checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karanvirrsingh/pharmacy2",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "flask>=2.3,<4.0",
        "rich>=13.0",
    ],
    entry_points={
        "console_scripts": [
            "drug-checker=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
