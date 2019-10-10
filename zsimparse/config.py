""" $lic$
Copyright (C) 2016-2019 by Mingyu Gao

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

from . import util

class Config:
    '''
    A wrapper class of libconfig object that supports convenient construct and
    access.
    '''

    def __init__(self, fname):
        '''
        Construct from a libconfig file.
        '''
        self.fname = fname
        if not os.path.exists(self.fname):
            raise ValueError('{}: {}: no cfg file {} found'
                             .format(util.PACKAGE_NAME,
                                     self.__class__.__name__,
                                     self.fname))

        with open(self.fname, 'r') as fh:
            self.cfg = libconf.load(fh)


    def get(self, names):
        '''
        Get the config value associated with `names`. Return `None` if not
        exist.
        '''
        names = util.format_names(names)
        val = self.cfg
        try:
            for n in names:
                val = val[n]
        except (IndexError, KeyError, TypeError):
            return None
        return val


    def __getitem__(self, key):
        return self.cfg.__getitem__(key)


    def __getattr__(self, attr):
        return self.__getitem__(attr)

