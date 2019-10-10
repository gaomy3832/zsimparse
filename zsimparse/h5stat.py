""" $lic$
Copyright (C) 2016-2018 by Mingyu Gao

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

from . import util

class H5Stat:
    '''
    A wrapper class of h5 stat that supports convenient construct and access.
    '''

    def __init__(self, fname):
        '''
        Construct from an h5 file.
        '''
        self.fname = fname
        if not os.path.exists(self.fname):
            raise ValueError('{}: {}: no h5 file {} found'
                             .format(util.PACKAGE_NAME,
                                     self.__class__.__name__,
                                     self.fname))

        fobj = h5py.File(self.fname, 'r')
        self.stat = fobj['stats']['root']
        if self.stat.shape[0] < 2:
            raise RuntimeError('{}: {}: incomplete simulation for h5 file {}'
                               .format(util.PACKAGE_NAME,
                                       self.__class__.__name__,
                                       self.fname))


    def num_samples(self):
        ''' Get the number of stat samples. '''
        return self.stat.shape[0]


    def get(self, names):
        '''
        Get the counter value associated with `names`. Return `None` if not
        exist.
        '''
        names = util.format_names(names)
        val = self.stat
        try:
            for n in names:
                val = val[n]
        except (IndexError, KeyError, TypeError):
            return None
        return val


    def __getitem__(self, key):
        return self.stat[key]

