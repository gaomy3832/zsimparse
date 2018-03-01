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

