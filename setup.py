from setuptools import setup, find_packages

setup(
    name="azoe",
    version='17.10.21',
    packages=find_packages(),
    package_data={
        "libs": ["font_tahoma.ttf", "font_tahoma.LICENCE.txt",
                 "textrect_readme.txt", "Verdana.ttf", "VerdanaEULA.txt"]
    }
)
