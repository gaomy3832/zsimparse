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

    def test_single_cache_first_level(self):
        '''
        Test cache stats are consistent with each other, at the first level.
        '''
        hits = zsimparse.get_cache_hit(self.dset, 'l1d')
        misses = zsimparse.get_cache_miss(self.dset, 'l1d')
        reads = zsimparse.get_cache_read(self.dset, 'l1d')
        writes = zsimparse.get_cache_write(self.dset, 'l1d')
        accesses = zsimparse.get_cache_access(self.dset, 'l1d')
        insertions = zsimparse.get_cache_insertion(self.dset, 'l1d')
        self.assertEqual(hits + misses, accesses)
        self.assertEqual(reads + writes, accesses + insertions)
        writebacks = zsimparse.get_cache_write(self.dset, 'l1d',
                                               with_insertion=False)
        self.assertEqual(reads + writebacks, accesses)

    def test_single_cache_higher_level(self):
        '''
        Test cache stats are consistent with each other, at higher levels.
        '''
        hits = zsimparse.get_cache_hit(self.dset, 'l2')
        misses = zsimparse.get_cache_miss(self.dset, 'l2')
        reads = zsimparse.get_cache_read(self.dset, 'l2')
        writes = zsimparse.get_cache_write(self.dset, 'l2')
        accesses = zsimparse.get_cache_access(self.dset, 'l2')
        insertions = zsimparse.get_cache_insertion(self.dset, 'l2')
        self.assertEqual(hits + misses, accesses)
        self.assertEqual(reads + writes, accesses + insertions)
        writebacks = zsimparse.get_cache_write(self.dset, 'l2',
                                               with_insertion=False)
        self.assertEqual(reads + writebacks, accesses)

    def test_sum_cache(self):
        ''' Test individual cache stats summed up to aggregated cache stats. '''
        num_l1d = zsimparse.config_get(self.cfg, 'sys caches l1d caches')
        acc = 0
        ins = 0
        for idx in range(num_l1d):
            acc += zsimparse.get_cache_access(self.dset, ('l1d', idx))
            ins += zsimparse.get_cache_insertion(self.dset, ('l1d', idx))
        self.assertEqual(zsimparse.get_cache_access(self.dset, 'l1d'), acc)
        self.assertEqual(zsimparse.get_cache_insertion(self.dset, 'l1d'), ins)


if __name__ == '__main__':
    unittest.main()

