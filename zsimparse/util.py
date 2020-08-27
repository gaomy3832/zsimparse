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

import collections.abc


PACKAGE_NAME = 'zsimparse'


def format_names(names):
    '''
    Format `names` and return as a tuple of hierarchical names.

    `names` can be a single string/integer, or a sequence of strings/integers.
    Each string will be decomposed into a sequence of strings, using
    whitespaces and dot (`.`) as separators.
    '''
    def _sep(string):
        return string.replace('.', ' ').split()

    # Translate a single string or integer to a list.
    if isinstance(names, str):
        # In Python 3 all strings are unicode by default.
        names = _sep(names)
    elif isinstance(names, int):
        # In Python 3 no diff between int and long.
        names = [names]
    elif not isinstance(names, collections.abc.Iterable):
        raise ValueError('{}: names need to be a sequence or '
                         'a single string/integer'
                         .format(PACKAGE_NAME))
    names2 = []
    for n in names:
        if isinstance(n, str):
            names2 += _sep(n)
        else:
            names2.append(n)

    return tuple(names2)


def str_names(names):
    '''
    Translate a tuple of hierarchical names to a string with dot (`.`) as
    separator.
    '''
    return '.'.join([str(n) for n in names])

