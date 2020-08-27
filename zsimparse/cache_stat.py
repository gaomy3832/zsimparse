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

import numpy as np

from .base_data_dict import BaseDataDict
from .h5stat import H5Stat
from . import util

class CacheStat(H5Stat):
    '''
    Cache event counters of h5 stat.
    '''

    OTHER_COUNTERS = ('PUTS', 'INVX')

    def __init__(self, stat, cache_names):
        '''
        Construct from a h5 stat with the names of the cache.
        '''
        if not isinstance(stat, BaseDataDict):
            stat = BaseDataDict(stat)
        raw = stat.get(cache_names)
        if raw is None:
            raise ValueError('{}: {}: cannot get cache {} from h5 stat'
                             .format(util.PACKAGE_NAME,
                                     self.__class__.__name__,
                                     cache_names))
        super().__init__(raw)
        dummy = self.get('mGETS')  # used to decide shape and type
        if dummy is None:
            raise ValueError('{}: {}: {} is not a cache stat'
                             .format(util.PACKAGE_NAME,
                                     self.__class__.__name__,
                                     cache_names))
        self.cnt_shape = dummy.shape
        self.cnt_dtype = dummy.dtype


    def get_count(self, *events):
        ''' Get cache event counts. '''
        cnt = np.zeros(self.cnt_shape, dtype=self.cnt_dtype)
        for e in events:
            c = self.get(e)
            if c is not None:
                cnt += c
        return cnt


    def get_read_hit(self):
        ''' Get cache read (protocol) hits. '''
        if self.is_first_level():
            return self.get_count('fhGETS', 'hGETS')
        return self.get_count('fhGETS', 'hGETS', 'fhGETX', 'hGETX')


    def get_read_miss(self):
        ''' Get cache read (protocol) misses. '''
        if self.is_first_level():
            return self.get_count('mGETS')
        return self.get_count('mGETS', 'mGETXIM', 'mGETXSM')


    def get_write_hit(self):
        ''' Get cache write (protocol) hits. '''
        if self.is_first_level():
            return self.get_count('fhGETX', 'hGETX', 'PUTX')
        return self.get_count('PUTX')


    def get_write_miss(self):
        ''' Get cache write (protocol) misses. '''
        if self.is_first_level():
            return self.get_count('mGETXIM', 'mGETXSM')
        return self.get_count()


    def get_insertion(self):
        ''' Get cache insertions (writes) due to misses. '''
        return self.get_count('mGETS', 'mGETXIM')


    def get_writeback(self):
        ''' Get cache writebacks (reads) due to evictions. '''
        return self.get_count('INV', 'FWD')


    def get_hit(self):
        ''' Get cache (protocol) hits. '''
        return self.get_read_hit() + self.get_write_hit()


    def get_miss(self):
        ''' Get cache (protocol) misses. '''
        return self.get_read_miss() + self.get_write_miss()


    def get_read(self, with_writeback=True):
        ''' Get cache reads. Include writebacks if `with_writeback` is True. '''
        cnt = self.get_read_hit() + self.get_read_miss()
        if with_writeback:
            cnt += self.get_writeback()
        return cnt


    def get_write(self, with_insertion=True):
        ''' Get cache writes. Include insertions if `with_insertion` is True. '''
        cnt = self.get_write_hit() + self.get_write_miss()
        if with_insertion:
            cnt += self.get_insertion()
        return cnt


    def get_access(self):
        ''' Get cache accesses. '''
        cnt = self.get_hit() + self.get_miss()
        assert np.array_equal(
            cnt,
            self.get_read(with_writeback=False)
            + self.get_write(with_insertion=False))
        return cnt


    def is_first_level(self):
        ''' Whether this cache is a first-level cache. '''
        return self.get('fhGETS') is not None

