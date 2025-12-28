from setuptools import setup, find_packages

setup(
    name="nexus-gateway",
    version="0.1.0",
    description="The Python SDK for Nexus Gateway - AI Semantic Caching Layer",
    author="Sunny Anand",
    author_email="your_email@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)