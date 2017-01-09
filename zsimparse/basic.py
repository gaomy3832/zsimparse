"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

import numpy as np

from . import util


def config_get(cfg, names):
    '''
    Get the config value with name(s) as `names` in libconfig object `cfg`.
    Return `None` if the config specified by `names` does not exist.
    '''
    names = util.format_names(names)
    # Turn names into ``str1.str2.[int1].[int2]'' key.
    key = '.'.join(['[{}]'.format(n) if isinstance(n, (int, long)) else str(n)
                    for n in names])
    return cfg.lookup(key, default=None)


def hdf5_get(dset, names):
    '''
    Get the counter with name(s) as `names` in hdf5 h5py dataset `dset`. Return
    `None` if the counter specified by `names` does not exist.
    '''
    names = util.format_names(names)
    try:
        data = dset
        for n in names:
            data = data[n]
    except (KeyError, ValueError):
        return None
    return np.array(data)

