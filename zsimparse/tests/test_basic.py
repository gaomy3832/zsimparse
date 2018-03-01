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

import os
from tempfile import NamedTemporaryFile
import numpy as np

import h5py
import pylibconfig2 as lcfg

import zsimparse


class TestBasic(unittest.TestCase):
    ''' Test basic.py. '''

    def setUp(self):
        # Example sim directory.
        self.simdir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'simdir')
        # Create config.
        self.cfg = lcfg.Config('g1 = {s1 = {t1 = 1; t2 = "val";}} '
                               'g2 = (0, 1, 2); '
                               'g3 = 3;')

        # Create temp file.
        self.fhdl = NamedTemporaryFile(suffix='.h5')
        # Create file object.
        self.fobj = h5py.File(self.fhdl.name, 'r+')
        # Create the datasets.
        dtype = np.dtype([('g1', np.dtype([('t1', 'u8', (100,)),
                                           ('t2', 'u8')])),
                          ('g2', 'u8', (10, 10))])
        dset = np.array(((np.ones(100),
                          10),
                         np.zeros((10, 10))),
                        dtype=dtype)
        self.fobj.create_dataset('root', data=dset)

    def tearDown(self):
        # Close (and remove) temp file.
        tfname = self.fhdl.name
        self.fhdl.close()
        self.assertFalse(os.path.exists(tfname))

    def test_get_config_by_dir(self):
        ''' Test get_config_by_dir(). '''
        cfg = zsimparse.get_config_by_dir(self.simdir)
        self.assertIsNotNone(cfg)
        self.assertIsNotNone(zsimparse.config_get(cfg, 'sys'))

    def test_get_hdf5_by_dir(self):
        ''' Test get_hdf5_by_dir(). '''
        dset = zsimparse.get_hdf5_by_dir(self.simdir)
        self.assertIsNotNone(dset)
        self.assertGreater(zsimparse.hdf5_get(dset, 'phase'), 0)
        dset = zsimparse.get_hdf5_by_dir(self.simdir, suffix='')
        self.assertGreater(dset.shape[0], 1)

    def test_get_config_by_dir_bad_dir(self):
        ''' Test get_config_by_dir() when dir is invalid. '''
        bad_dir = os.path.join(self.simdir, 'sim')
        try:
            _ = zsimparse.get_config_by_dir(bad_dir)
        except ValueError as e:
            self.assertIn('cfg', str(e))

    def test_get_hdf5_by_dir_bad_dir(self):
        ''' Test get_hdf5_by_dir() when dir is invalid. '''
        bad_dir = os.path.join(self.simdir, 'sim')
        try:
            _ = zsimparse.get_hdf5_by_dir(bad_dir)
        except ValueError as e:
            self.assertIn('hdf5', str(e))

    def test_get_hdf5_by_dir_bad_suffix(self):
        ''' Test get_hdf5_by_dir() when suffix is invalid. '''
        try:
            _ = zsimparse.get_hdf5_by_dir(self.simdir, suffix='abc')
        except ValueError as e:
            self.assertIn('suffix', str(e))

    def test_config_get(self):
        ''' Test config_get(). '''
        self.assertEqual(zsimparse.config_get(self.cfg, ('g1', 's1', 't1')), 1)
        self.assertEqual(zsimparse.config_get(self.cfg, ('g2', 1)), 1)
        self.assertEqual(zsimparse.config_get(self.cfg, 'g1 s1 t2'), 'val')
        self.assertEqual(zsimparse.config_get(self.cfg, 'g3'), 3)

    def test_config_get_invalid_names(self):
        ''' Test config_get() with invalid names. '''
        self.assertIsNone(zsimparse.config_get(self.cfg, ('g1', 's2')))
        self.assertIsNone(zsimparse.config_get(self.cfg, 'g1 s1 t3'))
        self.assertIsNone(zsimparse.config_get(self.cfg, 'g4'))

    def test_hdf5_get(self):
        ''' Test hdf5_get(). '''
        # /root/g1/t1.
        g1_t1 = zsimparse.hdf5_get(self.fobj, ('root', 'g1', 't1'))
        self.assertIsNotNone(g1_t1)
        self.assertEqual(g1_t1.shape, (100,))
        self.assertTrue((g1_t1 == 1).all())
        # /root/g1/t2.
        g1_t2 = zsimparse.hdf5_get(self.fobj, ('root g1 t2'))
        self.assertIsNotNone(g1_t2)
        self.assertEqual(g1_t2, 10)
        # /root/g2.
        g2 = zsimparse.hdf5_get(self.fobj['root'], 'g2')
        self.assertIsNotNone(g2)
        self.assertEqual(g2.shape, (10, 10))
        self.assertTrue((g2 == 0).all())

    def test_hdf5_get_invalid_names(self):
        ''' Test hdf5_get() with invalid names. '''
        self.assertIsNone(zsimparse.hdf5_get(self.fobj, ('g1', 't1')))
        self.assertIsNone(zsimparse.hdf5_get(self.fobj, 'root g2 t1'))
        self.assertIsNone(zsimparse.hdf5_get(self.fobj, 'g3'))


if __name__ == '__main__':
    unittest.main()

