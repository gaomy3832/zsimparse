""" $lic$
Copyright (C) 2016-2020, Mingyu Gao
All rights reserved.

This program is free software: you can redistribute it and/or modify it under
the terms of the Modified BSD-3 License as published by the Open Source
Initiative.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the BSD-3 License for more details.

You should have received a copy of the Modified BSD-3 License along with this
program. If not, see <https://opensource.org/licenses/BSD-3-Clause>.
"""

import os
import re
import setuptools

PACKAGE = 'zsimparse'
DESC = 'Python utilities to parse zsim simulation results'

def _get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, PACKAGE, '__init__.py'), 'r') as fh:
        matches = re.findall(r'^\s*__version__\s*=\s*[\'"]([^\'"]+)[\'"]',
                             fh.read(), re.M)
        if matches:
            return matches[-1]
    return '0.0.0'

def _readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst'), 'r') as fh:
        return fh.read()

setuptools.setup(
    name=PACKAGE,
    version=_get_version(),
    description=DESC,

    author='Mingyu Gao',
    author_email='gaomy@tsinghua.edu.cn',
    long_description=_readme(),
    url='https://github.com/gaomy3832/zsimparse',
    license='BSD 3-clause',

    packages=setuptools.find_packages(),

    include_package_data=True,

    install_requires=[
        'coverage>=5',
        'h5py>=2.10.0',
        'numpy>=1.7',
        'libconf>=2.0.0',
        'pytest>=3',
        'pytest-cov>=2',
        'pytest-xdist>=2',
    ],

    keywords='zsim parse libconfig hdf5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Hardware',
        'Topic :: Utilities',
    ],
)
