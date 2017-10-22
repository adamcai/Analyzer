from unittest import TestCase
from stats.ts import no_scaling, time_scaling, diff_return, rv
import pandas
from datetime import datetime

class ModuleTest(TestCase):

    def test_no_scaling(self):
        f = no_scaling(datetime(2016,12,1), datetime(2016,12,2))
        self.assertEquals(1, f)

    def test_time_scaling(self):
        f = time_scaling(datetime(2017,10,17), datetime(2017,10,18))
        self.assertEqual(1, f)
        f = time_scaling(datetime(2017,10,17), datetime(2017,10,24))
        self.assertAlmostEqual(5, f ** 2, )

    def test_diff_return(self):

        ts = pandas.Series(data = [1, 2, 3], index = [datetime(2016,12,1), datetime(2016,12,2), datetime(2016,12,3)], name = 'the name')
        result = diff_return(ts, 1)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[1])
        self.assertTrue(pandas.isnull(result[0]))
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
        ts = pandas.Series(data = [1, 2, 3, 4], index = [datetime(2016,12,1), datetime(2016,12,2), datetime(2016,12,3), datetime(2016,12,4)], name = 'the name')
        result = rv(ts, window = 5)
        
        return



