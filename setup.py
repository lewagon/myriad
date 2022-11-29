
from setuptools import setup, find_packages

import os

with open("requirements.txt") as f:
    requirements = [c.strip() for c in f.readlines()]

setup(name="myriad",
      version="0.2.2",
      description="Le Wagon challenge split tool",
      url="https://github.com/lewagon/myriad/",
      author="Sébastien Saunier",
      author_email="seb@lewagon.org",
      packages=find_packages(),
      include_package_data=True,  # use MANIFEST.in
      install_requires=requirements,
      scripts=[os.path.join("scripts", "myriad")])
