"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

import collections
import types


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

