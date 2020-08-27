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

from . import util

class BaseDataDict:
    '''
    A data dictionary wrapper class that supports convenient construct and
    access.
    '''

    def __init__(self, ddict):
        '''
        Construct from a data dict object.
        '''
        self.ddict = ddict


    def get(self, names):
        '''
        Get the counter value associated with `names`. Return `None` if not
        exist.
        '''
        names = util.format_names(names)
        val = self.ddict
        try:
            for n in names:
                val = val[n]
        except (IndexError, KeyError, ValueError, TypeError):
            # An object which cannot be indexed will throw TypeError.
            # A numpy object may throw ValueError if no matched field name.
            return None
        return val


    def lookup(self, names):
        '''
        Look up `names` and return a wrapped data dictionary. Return None if
        not exist.
        '''
        return self.__class__(self.get(names))


    @property
    def raw(self):
        ''' Get the raw underlying data dictionary. '''
        return self.ddict


    def __getitem__(self, key):
        return self.ddict.__getitem__(key)


    def __getattr__(self, attr):
        return self.ddict.__getitem__(attr)

