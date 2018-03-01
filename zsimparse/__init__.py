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

from .basic import get_config_by_dir, get_hdf5_by_dir
from .basic import config_get, hdf5_get

from .cache import get_cache_read_hit, get_cache_read_miss, \
        get_cache_write_hit, get_cache_write_miss, \
        get_cache_hit, get_cache_miss, get_cache_read, get_cache_write, \
        get_cache_access, get_cache_insertion

__version__ = '0.1.0'

