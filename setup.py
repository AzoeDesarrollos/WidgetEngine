from setuptools import setup, find_packages

setup(
    name="azoe",
    version='17.10.22',
    packages=find_packages(),
    package_data={
        "libs": ["*.ttf", "*.txt"]
    }
)
