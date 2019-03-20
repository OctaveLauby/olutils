from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Library description
    name="olutils",
    version="0.2.1",
    description="tools for common operations in a module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="utils tools",

    # Packages / Modules
    packages=find_packages(),
    install_requires=[
        "python-dateutil>=2.8.0",
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
