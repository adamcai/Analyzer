from pyanalyzer.calendar import UnitedStates
from pyanalyzer.test.utils import TestCase2
import datetime

class UnitedStatesTest(TestCase2):

    def test_add_days(self):

        calendar = UnitedStates()
        d1 = datetime.datetime(2017, 10, 30)
        result = calendar.add_days(d1, 2)
        expected = datetime.date(2017, 11, 1)
        self.assertEqual(expected, result)
