from pyanalyzer.test.utils import TestCase2
from pyanalyzer.stats.timeseries import TimeSeries
import datetime
import numpy as np

class TimeSeriesTest(TestCase2):

    def test_log(self):

        timeseries = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], name = "X")
        expected = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27), datetime.datetime(2017, 10, 26), datetime.datetime(2017, 10, 25), datetime.datetime(2017, 10, 24), datetime.datetime(2017, 10, 23), datetime.datetime(2017, 10, 22), datetime.datetime(2017, 10, 21)], data = [0.0, 0.6931471805599453, 1.0986122886681098, 1.3862943611198906, 1.6094379124341003, 1.791759469228055, 1.9459101490553132, 2.0794415416798357, 2.1972245773362196], name = "X")
        result = timeseries.log()
        self.assertEqual(expected, result)



        timeseries = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27)], 
                                data = [-1, 0, None], name = "X")
        expected = TimeSeries(index = [datetime.datetime(2017, 10, 29), datetime.datetime(2017, 10, 28), datetime.datetime(2017, 10, 27),], data = [
            np.NaN, -np.inf, np.NaN], name = "X")
        result = timeseries.log()
        self.assertEqual(expected, result)