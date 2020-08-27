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

import unittest

import os

import zsimparse


class TestCache(unittest.TestCase):
    ''' Test cache.py. '''

    def setUp(self):
        # Example sim directory.
        self.simdir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'simdir')
        # Get config.
        self.cfg = zsimparse.get_config_by_dir(self.simdir)
        # Get hdf5 dataset.
        self.dset = zsimparse.get_hdf5_by_dir(self.simdir, final_only=True)

    def test_single_cache_first_level(self):
        '''
        Test cache stats are consistent with each other, at the first level.
        '''
        hits = zsimparse.get_cache_hit(self.dset, ('l1d', 0))
        misses = zsimparse.get_cache_miss(self.dset, ('l1d', 0))
        reads = zsimparse.get_cache_read(self.dset, ('l1d', 0))
        writes = zsimparse.get_cache_write(self.dset, ('l1d', 0))
        self.assertEqual(hits,
                         zsimparse.get_cache_read_hit(self.dset, ('l1d', 0))
                         + zsimparse.get_cache_write_hit(self.dset, ('l1d', 0)))
        self.assertEqual(misses,
                         zsimparse.get_cache_read_miss(self.dset, ('l1d', 0))
                         + zsimparse.get_cache_write_miss(self.dset, ('l1d', 0)))
        accesses = zsimparse.get_cache_access(self.dset, ('l1d', 0))
        insertions = zsimparse.get_cache_insertion(self.dset, ('l1d', 0))
        writebacks = zsimparse.get_cache_writeback(self.dset, ('l1d', 0))
        self.assertEqual(hits + misses, accesses)
        self.assertEqual(reads + writes, accesses + insertions + writebacks)

    def test_single_cache_higher_level(self):
        '''
        Test cache stats are consistent with each other, at higher levels.
        '''
        hits = zsimparse.get_cache_hit(self.dset, 'l2')
        misses = zsimparse.get_cache_miss(self.dset, 'l2')
        reads = zsimparse.get_cache_read(self.dset, 'l2')
        writes = zsimparse.get_cache_write(self.dset, 'l2')
        self.assertEqual(hits,
                         zsimparse.get_cache_read_hit(self.dset, 'l2')
                         + zsimparse.get_cache_write_hit(self.dset, 'l2'))
        self.assertEqual(misses,
                         zsimparse.get_cache_read_miss(self.dset, 'l2')
                         + zsimparse.get_cache_write_miss(self.dset, 'l2'))
        accesses = zsimparse.get_cache_access(self.dset, 'l2')
        insertions = zsimparse.get_cache_insertion(self.dset, 'l2')
        writebacks = zsimparse.get_cache_writeback(self.dset, 'l2')
        self.assertEqual(hits + misses, accesses)
        self.assertEqual(reads + writes, accesses + insertions + writebacks)

    def test_sum_cache(self):
        ''' Test individual cache stats summed up to aggregated cache stats. '''
        num_l1d = zsimparse.config_get(self.cfg, 'sys caches l1d caches')
        self.assertEqual(num_l1d, 4)
        acc = 0
        ins = 0
        for idx in range(num_l1d):
            acc += zsimparse.get_cache_access(self.dset, ('l1d', idx))
            ins += zsimparse.get_cache_insertion(self.dset, ('l1d', idx))
        self.assertEqual(zsimparse.get_cache_access(self.dset, 'l1d').sum(),
                         acc)
        self.assertEqual(zsimparse.get_cache_insertion(self.dset, 'l1d').sum(),
                         ins)

    def test_cache_invalid(self):
        ''' Test invalid name. '''
        with self.assertRaisesRegex(ValueError, '.*cannot get.*'):
            _ = zsimparse.CacheStat(self.dset, 'null')
        with self.assertRaisesRegex(ValueError, '.*not a cache stat.*'):
            _ = zsimparse.CacheStat(self.dset, 'simpleCore')

    def test_raw_stat_input(self):
        ''' Test with a raw stat input. '''
        data = zsimparse.get_hdf5_by_dir(self.simdir)
        self.assertEqual(zsimparse.get_cache_hit(self.dset, 'l2'),
                         zsimparse.get_cache_hit(data[-1], 'l2'))

