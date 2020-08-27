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

from .cache_stat import CacheStat


def get_cache_read_hit(dset, caches):
    ''' Get cache read (protocol) hits. '''
    return CacheStat(dset, caches).get_read_hit()


def get_cache_read_miss(dset, caches):
    ''' Get cache read (protocol) misses. '''
    return CacheStat(dset, caches).get_read_miss()


def get_cache_write_hit(dset, caches):
    ''' Get cache write (protocol) hits. '''
    return CacheStat(dset, caches).get_write_hit()


def get_cache_write_miss(dset, caches):
    ''' Get cache write (protocol) misses. '''
    return CacheStat(dset, caches).get_write_miss()


def get_cache_insertion(dset, caches):
    ''' Get cache insertions. '''
    return CacheStat(dset, caches).get_insertion()


def get_cache_writeback(dset, caches):
    ''' Get cache writebacks. '''
    return CacheStat(dset, caches).get_writeback()


def get_cache_hit(dset, caches):
    ''' Get cache (protocol) hits. '''
    return CacheStat(dset, caches).get_hit()


def get_cache_miss(dset, caches):
    ''' Get cache (protocol) misses. '''
    return CacheStat(dset, caches).get_miss()


def get_cache_read(dset, caches, with_writeback=True):
    ''' Get cache reads. Include writebacks if `with_writeback` is True. '''
    return CacheStat(dset, caches).get_read(with_writeback=with_writeback)


def get_cache_write(dset, caches, with_insertion=True):
    ''' Get cache writes. Include insertions if `with_insertion` is True. '''
    return CacheStat(dset, caches).get_write(with_insertion=with_insertion)


def get_cache_access(dset, caches):
    ''' Get cache accesses. '''
    return CacheStat(dset, caches).get_access()

