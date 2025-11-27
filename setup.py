"""Setup configuration for raw_locator_generator package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="raw-locator-generator",
    version="1.0.0",
    author="Raw Locator Generator Team",
    description="A Python-based agent that extracts DOM elements and generates automation scripts for multiple frameworks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitsharma007/raw_locator_generator",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "raw-locator-generator=raw_locator_generator.dom_extractor_agent:main",
        ],
    },
    keywords="selenium playwright puppeteer cypress automation testing web-scraping dom-extraction",
    project_urls={
        "Bug Reports": "https://github.com/rohitsharma007/raw_locator_generator/issues",
        "Source": "https://github.com/rohitsharma007/raw_locator_generator",
        "Documentation": "https://github.com/rohitsharma007/raw_locator_generator/tree/main/docs",
    },
)
