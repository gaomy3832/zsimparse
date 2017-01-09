"""
 * Copyright (c) 2016. Mingyu Gao
 * All rights reserved.
 *
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
        self.dset = zsimparse.get_hdf5_by_dir(self.simdir)

    def test_single_cache(self):
        ''' Test cache stats are consistent with each other. '''
        hits = zsimparse.get_cache_hit(self.dset, 'l1d')
        misses = zsimparse.get_cache_miss(self.dset, 'l1d')
        reads = zsimparse.get_cache_read(self.dset, 'l1d')
        writes = zsimparse.get_cache_write(self.dset, 'l1d')
        accesses = zsimparse.get_cache_access(self.dset, 'l1d')
        self.assertEqual(hits + misses, accesses)
        self.assertEqual(reads + writes, accesses)

    def test_sum_cache(self):
        ''' Test individual cache stats summed up to aggregated cache stats. '''
        num_l1d = zsimparse.config_get(self.cfg, 'sys caches l1d caches')
        acc = 0
        for idx in range(num_l1d):
            acc += zsimparse.get_cache_access(self.dset, ('l1d', idx))
        self.assertEqual(zsimparse.get_cache_access(self.dset, 'l1d'), acc)


if __name__ == '__main__':
    unittest.main()

