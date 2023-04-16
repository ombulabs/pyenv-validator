# noqa=D100
# type: ignore
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}
with open("./src/pyenv_validator/version.py", encoding="utf-8") as f:
    exec(f.read(), meta)

setup(
    name="pyenv_validator",
    version=meta["__version__"],
    author="OmbuLabs - The Lean Software Boutique LLC",
    author_email="oss@ombulabs.com",
    desciption="Validate environment variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/ombulabs/pyenv-validator",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)
