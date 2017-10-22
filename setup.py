from setuptools import setup, find_packages

setup(
    name="azoe",
    version='17.10.22-1',
    packages=find_packages(),
    package_data={
        "libs": ["*.ttf", "*.txt"]
    },
    install_requires=['pygame']
)
