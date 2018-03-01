"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

import os
import numpy as np

import h5py
import pylibconfig2 as lcfg

from . import util
from .util import PACKAGE_NAME


def get_config_by_dir(simdir):
    '''
    Get the libconfig object from ```simdir`/out.cfg''.
    '''
    cfgfname = os.path.join(simdir, 'out.cfg')
    if not os.path.exists(cfgfname):
        raise ValueError('{}: get_config_by_dir: invalid simdir {}, '
                         'no cfg file {} found'
                         .format(PACKAGE_NAME, simdir, cfgfname))
    with open(cfgfname, 'r') as fh:
        cfg = lcfg.Config(fh.read())
    return cfg


def get_hdf5_by_dir(simdir, suffix='-ev'):
    '''
    Get the hdf5 dataset in ```simdir`/zsim`suffix`.h5''. `suffix` can be one
    of `-ev`, `-cmp`, and `''`. If `suffix` is `-ev`, then only return the final
    dump dataset (by removing the initial dataset).
    '''
    if suffix != '-ev' and suffix != '-cmp' and suffix != '':
        raise ValueError('{}: get_hdf5_by_dir: invalid suffix {}'
                         .format(PACKAGE_NAME, suffix))
    h5fname = os.path.join(simdir, 'zsim{}.h5'.format(suffix))
    if not os.path.exists(h5fname):
        raise ValueError('{}: get_hdf5_by_dir: invalid simdir {}, '
                         'no hdf5 file {} found'
                         .format(PACKAGE_NAME, simdir, h5fname))
    fobj = h5py.File(h5fname, 'r')
    dset = fobj['stats']['root']
    if suffix == '-ev':
        if dset.shape[0] < 2:
            raise RuntimeError('{}: get_hdf5_by_dir: incomplete simulation in '
                               '{}, bad hdf5 file {}'
                               .format(PACKAGE_NAME, simdir, h5fname))
        dset = dset[-1]
    return dset


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
    except (IndexError, KeyError, ValueError):
        return None
    return np.array(data)

