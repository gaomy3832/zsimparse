"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

from .basic import hdf5_get


CACHE_OTHER_COUNTERS = ['PUTS', 'INV', 'INVX', 'FWD']


def _get_cache_counters(cache_dset, counters):
    ''' Get cache counters from cache statistics. '''
    values = None
    if not counters:
        # No given counters, should return a zero array with proper shape.
        values = hdf5_get(cache_dset, CACHE_OTHER_COUNTERS[-1])
        values.fill(0)
    for cnt in counters:
        val = hdf5_get(cache_dset, cnt)
        if val is not None:
            values = val if values is None else values + val
    return values


def get_cache_read_hit(dset, caches):
    ''' Get cache read hits. '''
    cache_dset = hdf5_get(dset, caches)
    first_level = hdf5_get(cache_dset, 'fhGETS') is not None
    return _get_cache_counters(cache_dset,
                               ['fhGETS', 'hGETS'] if first_level else
                               ['hGETS', 'hGETX'])


def get_cache_read_miss(dset, caches):
    ''' Get cache read misses. '''
    cache_dset = hdf5_get(dset, caches)
    first_level = hdf5_get(cache_dset, 'fhGETS') is not None
    return _get_cache_counters(cache_dset,
                               ['mGETS'] if first_level else
                               ['mGETS', 'mGETXIM', 'mGETXSM'])


def get_cache_write_hit(dset, caches):
    ''' Get cache write hits. '''
    cache_dset = hdf5_get(dset, caches)
    first_level = hdf5_get(cache_dset, 'fhGETS') is not None
    return _get_cache_counters(cache_dset,
                               ['fhGETX', 'hGETX', 'PUTX'] if first_level else
                               ['PUTX'])


def get_cache_write_miss(dset, caches):
    ''' Get cache write misses. '''
    cache_dset = hdf5_get(dset, caches)
    first_level = hdf5_get(cache_dset, 'fhGETS') is not None
    return _get_cache_counters(cache_dset,
                               ['mGETXIM', 'mGETXSM'] if first_level else
                               [])


def get_cache_insertion(dset, caches):
    ''' Get cache insertions. '''
    cache_dset = hdf5_get(dset, caches)
    return _get_cache_counters(cache_dset, ['mGETS', 'mGETXIM'])


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


def get_cache_write(dset, caches, with_insertion=True):
    ''' Get cache writes. Include insertions if `with_insertion` is True. '''
    return get_cache_write_hit(dset, caches) \
            + get_cache_write_miss(dset, caches) \
            + (get_cache_insertion(dset, caches) if with_insertion else 0)


def get_cache_access(dset, caches):
    ''' Get cache accesses. '''
    acc = get_cache_hit(dset, caches) + get_cache_miss(dset, caches)
    assert acc == get_cache_read(dset, caches) \
            + get_cache_write(dset, caches, with_insertion=False)
    return acc

