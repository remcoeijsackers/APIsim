import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="APIsim",
    version="0.0.1",
    author="Remco Eijsackers",
    author_email="contact@remcoeijsackers.com",
    description="A package to simulate api users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remcoeijsackers/APIsim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, MacOS",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)