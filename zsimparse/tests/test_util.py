"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
"""

import unittest

import zsimparse.util


class TestUtil(unittest.TestCase):
    ''' Test util.py. '''

    def test_format_names(self):
        ''' Test format_names(). '''
        self.assertTupleEqual(zsimparse.util.format_names('ab'),
                              ('ab',))
        self.assertTupleEqual(zsimparse.util.format_names(12),
                              (12,))
        self.assertTupleEqual(zsimparse.util.format_names(['ab', 12]),
                              ('ab', 12,))
        self.assertTupleEqual(zsimparse.util.format_names('a b 0 1'),
                              ('a', 'b', '0', '1'))


if __name__ == '__main__':
    unittest.main()

