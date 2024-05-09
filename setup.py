# This file is part of pyRDDLGym.

# pyRDDLGym is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Free Software Foundation.

# pyRDDLGym is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with pyRDDLGym. If not, see <https://opensource.org/licenses/MIT>.

from setuptools import setup, find_packages


setup(
      name='rddl-ide',
      version='0.1',
      author="Mike Gimelfarb",
      author_email="mike.gimelfarb@mail.utoronto.ca",
      description="IDE for pyRDDLGym",
      license="MIT License",
      url="https://github.com/pyrddlgym-project/rddl-ide",
      packages=find_packages(),
      install_requires=[
          'tk',
          'Pygments>=2.18.0',
          'customtkinter>=5.2.2',
          'CTkMenuBar>=0.7',
          'pyRDDLGym>=2.0'
        ],
      python_requires=">=3.11",
      package_data={'': ['*.cfg', '*.rddl']},
      include_package_data=True,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
