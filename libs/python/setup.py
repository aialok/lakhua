"""Setup configuration for lakhua (fallback for older pip versions)."""

from pathlib import Path

from setuptools import find_packages, setup

README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="lakhua",
    version="1.0.0",
    description="Fast, offline reverse geocoding for India",
    long_description=README,
    long_description_content_type="text/markdown",
    author="aialok",
    author_email="your.email@example.com",
    url="https://github.com/aialok/lakhua",
    project_urls={
        "Homepage": "https://github.com/aialok/lakhua",
        "Repository": "https://github.com/aialok/lakhua",
        "Issues": "https://github.com/aialok/lakhua/issues",
    },
    packages=find_packages(),
    package_data={
        "lakhua": ["data/*.json", "py.typed"],
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "h3>=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="geocoding reverse-geocoding h3 india offline",
    license="MIT",
)

