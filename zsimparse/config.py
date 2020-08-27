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

import libconf

from .base_data_dict import BaseDataDict
from . import util

class Config(BaseDataDict):
    '''
    A wrapper class of libconfig object.
    '''

    @classmethod
    def make_from_file(cls, fname):
        '''
        Construct from a libconfig file.
        '''
        if not os.path.exists(fname):
            raise ValueError('{}: {}: no cfg file {} found'
                             .format(util.PACKAGE_NAME, cls.__name__, fname))
        with open(fname, 'r') as fh:
            cfg = libconf.load(fh)

        return cls(cfg)

