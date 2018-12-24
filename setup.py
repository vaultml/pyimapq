import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimapq",
    version="0.0.1",
    author="Nir Tzachar",
    author_email="nir.tzachar@gmail.com",
    description="An IMAP queue package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vaultml/pyimapq",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
