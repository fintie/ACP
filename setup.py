#!/usr/bin/env python
"""Setup configuration for ACP Harness Hub Connector Platform."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="acp-harness-connector",
    version="0.1.0",
    author="Fintie",
    author_email="fintie@example.com",
    description="ACP Harness Hub Connector Platform for seamless developer collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fintie/ACP",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.21.0",
        "PyGithub>=1.58.0",
        "pydantic>=1.10.0",
        "httpx>=0.23.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
