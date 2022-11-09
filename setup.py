# type: ignore
import setuptools

import versioneer

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pedpy",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="T. Schroedter",
    description="pedpy is a python module for pedestrian movement analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pedpy", "pedpy.data", "pedpy.io", "pedpy.methods"],
    python_requires=">=3.8",
    install_requires=[
        "aenum == 3.1.5",
        "numpy == 1.22.0",
        "pandas == 1.5.1",
        "Shapely == 2.0b2",
        "scipy == 1.9.3",
    ],
)
