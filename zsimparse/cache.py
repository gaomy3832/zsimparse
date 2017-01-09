"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

from .basic import hdf5_get


CACHE_READ_HIT_COUNTERS = ['fhGETS', 'hGETS']
CACHE_WRITE_HIT_COUNTERS = ['fhGETX', 'hGETX', 'PUTX']
CACHE_READ_MISS_COUNTERS = ['mGETS']
CACHE_WRITE_MISS_COUNTERS = ['mGETXIM', 'mGETXSM']
CACHE_OTHER_COUNTERS = ['PUTS', 'INV', 'INVX', 'FWD']

CACHE_HIT_COUNTERS = CACHE_READ_HIT_COUNTERS + CACHE_WRITE_HIT_COUNTERS
CACHE_MISS_COUNTERS = CACHE_READ_MISS_COUNTERS + CACHE_WRITE_MISS_COUNTERS
CACHE_READ_COUNTERS = CACHE_READ_MISS_COUNTERS + CACHE_READ_HIT_COUNTERS
CACHE_WRITE_COUNTERS = CACHE_WRITE_MISS_COUNTERS + CACHE_WRITE_HIT_COUNTERS


def _get_cache_counters(dset, caches, counters):
    '''
    Get cache statistics. Cache name is specified by `caches`, and stats is
    specified by `counters`.
    '''
    cache_dset = hdf5_get(dset, caches)
    values = None
    for cnt in counters:
        val = hdf5_get(cache_dset, cnt)
        if val is not None:
            values = val if values is None else values + val
    return values


def get_cache_read_hit(dset, caches):
    ''' Get cache read hits. '''
    return _get_cache_counters(dset, caches, CACHE_READ_HIT_COUNTERS)


def get_cache_read_miss(dset, caches):
    ''' Get cache read misses. '''
    return _get_cache_counters(dset, caches, CACHE_READ_MISS_COUNTERS)


def get_cache_write_hit(dset, caches):
    ''' Get cache write hits. '''
    return _get_cache_counters(dset, caches, CACHE_WRITE_HIT_COUNTERS)


def get_cache_write_miss(dset, caches):
    ''' Get cache write misses. '''
    return _get_cache_counters(dset, caches, CACHE_WRITE_MISS_COUNTERS)


def get_cache_hit(dset, caches):
    ''' Get cache hits. '''
    return get_cache_read_hit(dset, caches) \
            + get_cache_write_hit(dset, caches)


def get_cache_miss(dset, caches):
    ''' Get cache misses. '''
    return get_cache_read_miss(dset, caches) \
            + get_cache_write_miss(dset, caches)


def get_cache_read(dset, caches):
    ''' Get cache reads. '''
    return get_cache_read_hit(dset, caches) \
            + get_cache_read_miss(dset, caches)


def get_cache_write(dset, caches):
    ''' Get cache writes. '''
    return get_cache_write_hit(dset, caches) \
            + get_cache_write_miss(dset, caches)


def get_cache_access(dset, caches):
    ''' Get cache accesses. '''
    return get_cache_read(dset, caches) \
            + get_cache_write(dset, caches)

