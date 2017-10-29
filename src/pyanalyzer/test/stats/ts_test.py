from unittest import TestCase
from pyanalyzer.stats.ts import no_scaling, time_scaling, diff_return, rv
import datetime
import numpy as np
from pyanalyzer.stats.timeseries import TimeSeries

class ModuleTest(TestCase):

    def test_no_scaling(self):
        f = no_scaling(datetime.datetime(2016,12,1), datetime.datetime(2016,12,2))
        self.assertEquals(1, f)

    def test_time_scaling(self):
        f = time_scaling(datetime.datetime(2017,10,17), datetime.datetime(2017,10,18))
        self.assertEqual(1, f)
        f = time_scaling(datetime.datetime(2017,10,17), datetime.datetime(2017,10,24))
        self.assertAlmostEqual(5, f ** 2, )

    def test_diff_return(self):

        ts = TimeSeries(data = [1, 2, 3], index = [datetime.datetime(2016,12,1), datetime.datetime(2016,12,2), datetime.datetime(2016,12,3)], name = 'the name')
        result = diff_return(ts, 1)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[1])
        self.assertTrue(np.isnan(result[0]))
        self.assertEqual('the name', result.name)

        h = object()
        def scaling(d1, d2, holidays):
            self.assertEqual(id(h), id(holidays))
            # return 2, 6
            return d1.day * d2.day 

        result = diff_return(ts, 1, scaling, h)
        self.assertEqual(3, len(result))
        self.assertEqual(0.5, result[1])
        self.assertEqual(1 / 6, result[2])

    def test_rv(self):

        ts = TimeSeries(index = [datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21), datetime.datetime(2017, 10, 20), datetime.datetime(2017, 10, 19), datetime.datetime(2017, 10, 18)], data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], name = "X")
        result = rv(ts, window = 5)
        expected = TimeSeries(index = [datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21), datetime.datetime(2017, 10, 20), datetime.datetime(2017, 10, 19), datetime.datetime(2017, 10, 18)], data = [0.0, 0.0, 0.0, 0.0, None, None, None, None, None], name = "X")
        self.assertEqual(expected.name, ts.name)
        self.assertEqual(len(expected), len(expected))
        for d1, d2 in zip(expected.index, result.index):
            self.assertEqual(d1, d2)

        for v1, v2 in zip(expected, result):
            if np.isnan(v1):
                self.assertTrue(np.isnan(v2))
            else:
                self.assertEqual(v1, v2)



