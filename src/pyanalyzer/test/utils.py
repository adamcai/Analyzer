from unittest import TestCase
from pyanalyzer.stats.timeseries import _TimeSeries
import numpy as np

class TestCase2(TestCase):

    def assertEqual(self, first, second, msg = None):

        if isinstance(first, _TimeSeries):
            self.assertIsInstance(second, _TimeSeries)

            self.assertEqual(first.name, second.name)
            self.assertEqual(len(first), len(second))
            for d1, d2 in zip(first.index, second.index):
                self.assertEqual(d1, d2, msg)

            for v1, v2 in zip(first, second):
                if np.isnan(v1):
                    self.assertTrue(np.isnan(v2), msg)
                else:
                    self.assertEqual(v1, v2, msg)
        else:
            return super().assertEqual(first, second, msg)

