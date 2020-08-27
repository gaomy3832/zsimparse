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

import h5py
import numpy as np

from .base_data_dict import BaseDataDict
from . import util

class H5Stat(BaseDataDict):
    '''
    A wrapper class of h5 stat.
    '''

    @classmethod
    def make_from_file(cls, fname):
        '''
        Construct from an h5 file.
        '''
        if not os.path.exists(fname):
            raise ValueError('{}: {}: no h5 file {} found'
                             .format(util.PACKAGE_NAME, cls.__name__, fname))
        fobj = h5py.File(fname, 'r')
        stat = fobj['stats']['root']
        if stat.shape[0] < 2:
            raise RuntimeError('{}: {}: incomplete simulation for h5 file {}'
                               .format(util.PACKAGE_NAME, cls.__name__, fname))

        return cls(stat)


    def num_samples(self):
        ''' Get the number of stat samples. '''
        return np.prod(self.ddict.shape)


    def num_dims(self):
        ''' Get the dimensions of stat samples. '''
        return len(self.ddict.shape)

