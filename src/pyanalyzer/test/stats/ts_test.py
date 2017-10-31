from pyanalyzer.test.utils import TestCase2
from pyanalyzer.stats.ts import time_scaling, diff_return, rv
import datetime
import numpy as np
from pyanalyzer.stats.timeseries import TimeSeries
from pyanalyzer.calendar import WeekdayCalendar, Calendar

class CalendarStub(Calendar):
    def business_days_between(self, date1, date2):
        return date1.day * date2.day

class ModuleTest(TestCase2):

    def test_time_scaling(self):
        f = time_scaling(datetime.datetime(2017,10,17), datetime.datetime(2017,10,18))
        self.assertEqual(1, f)
        f = time_scaling(datetime.datetime(2017,10,17), datetime.datetime(2017,10,24))
        self.assertAlmostEqual(5, f ** 2, )


        f = time_scaling(datetime.datetime(2017,10,17), datetime.datetime(2017,10,24), calendar = WeekdayCalendar())
        self.assertAlmostEqual(5, f ** 2, ) 

    def test_diff_return(self):

        ts = TimeSeries(data = [1, 2, 3], index = [datetime.datetime(2016,12,1), datetime.datetime(2016,12,2), datetime.datetime(2016,12,3)], name = 'the name')
        result = diff_return(ts, 1)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[1])
        self.assertTrue(np.isnan(result[0]))
        self.assertEqual('the name', result.name)



        result = diff_return(ts, 1, True, CalendarStub())
        self.assertEqual(3, len(result))
        self.assertEqual(1 / (2 ** 0.5), result[1])
        self.assertEqual(1 / (6 ** 0.5), result[2])



    def test_rv(self):

        ts = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], name = "X")
        result = rv(ts, window = 5, rtype = 'N', lag = 1, scaling = False)
        expected = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [0.0, 0.0, 0.0, 0.0, None, None, None, None, None], name = "X")
        self.assertEqual(expected, result)

        ts = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [1.0, 3.0, 6.0, 10.0, 15.0, 21.0, 28.0, 36.0, 45.0], name = "X")
        result = rv(ts, window = 5, rtype = 'N', lag = 1, scaling = False)
        expected = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [1.5811388300841898, 1.5811388300841898, 1.5811388300841898, 1.5811388300841898, None, None, None, None, None], name = "X")
        self.assertEqual(expected, result)

