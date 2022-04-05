import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="carbon-aware-scheduler",
    version="1.0.1",
    description="Carbon-minimizing task scheduler for Unix systems",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abel-vs/carbon-scheduler",
    author="Wander Siemers, Abel van Steenweghen, Florentin Arsene",
    author_email="wandersiemers@me.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "requests", "python-crontab", "croniter", "pyinquirer"],
    entry_points={
        "console_scripts": [
            "cas=src.__main__:main",
        ]
    },
)