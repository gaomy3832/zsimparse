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

from .h5stat import H5Stat
from .config import Config

def get_config_by_dir(simdir):
    '''
    Get the libconfig object from ```simdir`/out.cfg''.
    '''
    return Config.make_from_file(os.path.join(simdir, 'out.cfg'))


def get_hdf5_by_dir(simdir, final_only=False):
    '''
    Get the hdf5 data stat from ```simdir`/zsim.h5''. If `final_only` is True,
    return only the final stat snapshot instead of the periodic sequence.
    '''
    stat_seq = H5Stat.make_from_file(os.path.join(simdir, 'zsim.h5'))
    return stat_seq.lookup(-1) if final_only else stat_seq


def config_get(cfg, names):
    '''
    Get the config value associated with `names` in the libconfig object `cfg`.
    Return `None` if not exist.
    '''
    return cfg.get(names)


def hdf5_get(stat, names):
    '''
    Get the counter value associated with `names` in the hdf5 dataset `stat`.
    Return `None` if not exist.
    '''
    return stat.get(names)

