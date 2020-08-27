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

import libconf

import zsimparse


class TestBasic(unittest.TestCase):
    ''' Test basic.py. '''

    def setUp(self):
        # Example sim directory.
        self.simdir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'simdir')

    def test_get_config_by_dir(self):
        ''' Test get_config_by_dir(). '''
        cfg = zsimparse.get_config_by_dir(self.simdir)
        self.assertIsNotNone(cfg)
        self.assertIsNotNone(zsimparse.config_get(cfg, 'sys'))

    def test_get_hdf5_by_dir(self):
        ''' Test get_hdf5_by_dir(). '''
        stat = zsimparse.get_hdf5_by_dir(self.simdir)
        self.assertIsNotNone(stat)
        self.assertGreater(stat.num_samples(), 1)
        stat_first = zsimparse.hdf5_get(stat, 0)
        stat_last = zsimparse.hdf5_get(stat, -1)
        self.assertEqual(stat_first['phase'], 0)
        self.assertGreater(stat_last['phase'], 0)
        self.assertEqual(
            zsimparse.get_hdf5_by_dir(self.simdir, final_only=True).raw,
            stat_last)

    def test_get_config_by_dir_bad_dir(self):
        ''' Test get_config_by_dir() when dir is invalid. '''
        bad_dir = os.path.join(self.simdir, 'sim')
        with self.assertRaisesRegex(ValueError, '.*cfg.*'):
            _ = zsimparse.get_config_by_dir(bad_dir)

    def test_get_hdf5_by_dir_bad_dir(self):
        ''' Test get_hdf5_by_dir() when dir is invalid. '''
        bad_dir = os.path.join(self.simdir, 'sim')
        with self.assertRaisesRegex(ValueError, '.*h5.*'):
            _ = zsimparse.get_hdf5_by_dir(bad_dir)

    def test_config_get(self):
        ''' Test config_get(). '''
        cfg = zsimparse.get_config_by_dir(self.simdir)
        cfg.raw['list'] = [1, 2, 3]

        self.assertEqual(
            zsimparse.config_get(cfg, ('sys', 'caches', 'l1d', 'size')),
            65536)
        self.assertEqual(
            zsimparse.config_get(cfg, ('list', 1)),
            2)
        self.assertEqual(
            zsimparse.config_get(cfg, 'sys caches l1d type'),
            'Simple')
        self.assertEqual(
            zsimparse.config_get(cfg, 'sim.maxTotalInstrs'),
            libconf.LibconfInt64(0))

        self.assertEqual(cfg['sys']['caches']['l1d']['size'], 65536)
        self.assertEqual(cfg['list'][1], 2)
        self.assertEqual(cfg['sys']['caches']['l1d']['type'], 'Simple')
        self.assertEqual(cfg['sim']['maxTotalInstrs'], libconf.LibconfInt64(0))

        self.assertEqual(cfg.sys.caches.l1d.size, 65536)
        self.assertEqual(cfg.sys.caches.l1d.type, 'Simple')
        self.assertEqual(cfg.sim.maxTotalInstrs, libconf.LibconfInt64(0))

    def test_config_get_invalid_names(self):
        ''' Test config_get() with invalid names. '''
        cfg = zsimparse.get_config_by_dir(self.simdir)
        cfg.raw['list'] = [1, 2, 3]

        self.assertIsNone(zsimparse.config_get(cfg, ('g1', 's2')))
        self.assertIsNone(zsimparse.config_get(cfg, 'g1 s1 t3'))
        self.assertIsNone(zsimparse.config_get(cfg, 'g4'))

        with self.assertRaises(KeyError):
            _ = cfg['g1']['s2']
        with self.assertRaises(KeyError):
            _ = cfg['g1']['s1']['t3']
        with self.assertRaises(IndexError):
            _ = cfg['list'][4]
        with self.assertRaises(TypeError):
            _ = cfg['sys']['frequency'][1]

        with self.assertRaises(KeyError):
            _ = cfg.g1.s2
        with self.assertRaises(KeyError):
            _ = cfg.g1.s1.t3
        with self.assertRaises(IndexError):
            _ = cfg.list[4]
        with self.assertRaises(TypeError):
            _ = cfg.sys.frequency[1]

    def test_config_lookup(self):
        ''' Test lookup(). '''
        val = zsimparse.get_config_by_dir(self.simdir)
        for key in ('sys', 'caches', 'l1d', 'size'):
            val = val.lookup(key)
        self.assertEqual(val.raw, 65536)

    def test_hdf5_get(self):
        ''' Test hdf5_get(). '''
        stat = zsimparse.get_hdf5_by_dir(self.simdir)

        last_l2_putx = 0
        last_c0_instrs = 0
        for idx in range(stat.num_samples()):
            c0_instrs = zsimparse.hdf5_get(stat, (idx, 'simpleCore', 0, 'instrs'))
            l2_putx = zsimparse.hdf5_get(stat, (idx, 'l2', 0, 'PUTX'))
            self.assertGreaterEqual(c0_instrs, last_c0_instrs)
            self.assertGreaterEqual(l2_putx, last_l2_putx)

    def test_hdf5_get_final_only(self):
        ''' Test hdf5_get() for final only. '''
        stat = zsimparse.get_hdf5_by_dir(self.simdir, final_only=True)

        l2_putx = zsimparse.hdf5_get(stat, ('l2', 0, 'PUTX'))
        self.assertEqual(l2_putx, 1545)
        self.assertEqual(stat['l2'][0]['PUTX'], l2_putx)

        sched_rqszhist = stat.lookup('sched.rqSzHist')
        self.assertEqual(sched_rqszhist.num_samples(), 17)
        self.assertEqual(sched_rqszhist.num_dims(), 1)
        sched_rqszhist = sched_rqszhist.raw
        self.assertEqual(sched_rqszhist[0], 121)
        self.assertTrue((sched_rqszhist[1:] == 0).all())
        self.assertTrue((stat['sched']['rqSzHist'] == sched_rqszhist).all())

    def test_hdf5_get_invalid_names(self):
        ''' Test hdf5_get() with invalid names. '''
        stat = zsimparse.get_hdf5_by_dir(self.simdir)

        self.assertIsNone(zsimparse.hdf5_get(stat, ('g1', 't1')))
        self.assertIsNone(zsimparse.hdf5_get(stat, 'root g2 t1'))
        self.assertIsNone(zsimparse.hdf5_get(stat, 'g3'))
        self.assertIsNone(zsimparse.hdf5_get(stat, (-1, 'phase', 'g3')))

        with self.assertRaises(ValueError):
            _ = stat['g1']['t1']
        with self.assertRaises(ValueError):
            _ = stat['root']['g2']['t1']
        with self.assertRaises(ValueError):
            _ = stat['g3']
        with self.assertRaises(IndexError):
            _ = stat[-1]['phase']['g3']

    def test_hdf5_lookup(self):
        ''' Test lookup(). '''
        val = zsimparse.get_hdf5_by_dir(self.simdir)
        for key in (-1, 'l2', 0, 'PUTX'):
            val = val.lookup(key)
        self.assertEqual(val.raw, 1545)

