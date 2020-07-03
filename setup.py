import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taxonupdate",
    version="0.7.1",
    author="Bernd Kampe",
    author_email="bernd.kampe@uni-jena.de",
    description="Turn the NCBI Taxonomy into a dictionary for LINNAEUS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JULIELab/taxonupdate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research"
    ],
    python_requires='>=3.6',
)
