from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Library description
    name="olutils",
    version="1.1.0",
    description="tools for common operations in a module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="utils tools",

    # Packages / Modules
    packages=find_packages(),
    install_requires=[
        "check-manifest>=0.37",
        "matplotlib>=3.0.3",
        "numpy>=1.10.0",
        "pylint>=2.3.1",
        "pytest>=4.3",
        "python-dateutil>=2.8.0",
        "twine>=1.13.0",
    ],

    # Code source and license
    url="https://github.com/OctaveLauby/olutils",
    author="Octave Lauby",
    author_email="",
    license="Apache 2.0",

    # More
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
