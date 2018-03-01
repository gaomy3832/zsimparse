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

import collections
import types


PACKAGE_NAME = 'zsimparse'


def format_names(names):
    '''
    Format `names` and return as a tuple of hierarchical names.

    Given `names` can be a single string/integer, or a sequence of
    strings/integers. If names are all strings, `names` can also be a
    whitespace-delimited string.
    '''
    # Support whitespace-delimited string names.
    if isinstance(names, types.StringTypes):
        names = names.split()
    # Make sure names is a non-string iterable.
    if not isinstance(names, collections.Iterable):
        names = (names,)
    return tuple(names)

