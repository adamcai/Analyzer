import QuantLib
import datetime


class Calendar(object):

    def is_business_day(self, date):
        raise NotImplemented()

    def business_days_between(self, date1, date2):
        '''
            count the number of days between 2 dates
            date1, date2: datetime days
            return integer

            Note: we fall days to previous business days
            For example:
            date1 is a Friday, date2 is Sunday, function returns 0
            date1 is a Friday, date2 is next Monday, function returns 1

        '''
        
        raise NotImplemented()
    
    def add_days(self, date, n):
        raise NotImplemented()

def _to_qldate(date):
    return QuantLib.Date(date.day, date.month, date.year)

def _to_date(date):
    return datetime.date(date.year(), date.month(), date.dayOfMonth())

class OpenCalendar(Calendar):

    def is_business_day(self, date):
        return True

    def business_days_between(self, date1, date2):
        return (date2 - date1).days

    def add_days(self, date : datetime.datetime, n):
        return date + datetime.timedelta(n)


class WeekdayCalendar(Calendar):

    def is_business_day(self, date):
        return day.weekday() < 5

    def business_days_between(self, date1, date2):
        '''
            count the number of days between 2 dates
            date1, date2: datetime days
            return integer

            Note: we fall days to previous business days
            For example:
            date1 is a Friday, date2 is Sunday, function returns 0
            date1 is a Friday, date2 is next Monday, function returns 1

        '''
        daygenerator = (date1 + datetime.timedelta(x + 1) for x in range((date2 - date1).days))
        return sum(1 for day in daygenerator if day.weekday() < 5)

    def add_days(self, date : datetime.datetime, n):
        return date + datetime.timedelta(1 if date.weekday() < 4 else 7 - date.weekday())

class _QuantLibCalendar(Calendar):

    def __init__(self, ql_calendar):
        self._ql_calendar = ql_calendar

    def is_business_day(self, date):
        return self._ql_calendar.isBusinessDay(_to_qldate(date))

    def business_days_between(self, date1, date2):
        return self._ql_calendar(_to_qldate(date1), _to_qldate(date2))

    def add_days(self, date, n):
        d = self._ql_calendar.advance(_to_qldate(date), int(n), QuantLib.Days)
        return _to_date(d)

class UnitedKingdom(_QuantLibCalendar):

    def __init__(self):
        super(UnitedKingdom, self).__init__(QuantLib.UnitedKingdom())

class UnitedStates(_QuantLibCalendar):

    def __init__(self):
        super(UnitedStates, self).__init__(QuantLib.UnitedStates())
        
   
def get_calendar_by_name(name : str) -> Calendar:
    name = name.upper()
    if name == 'OPEN':
        return OpenCalendar()
    elif name == 'WEEKDAY':
        return WeekdayCalendar()
    elif name == 'US':
        return UnitedStates()
    elif name == 'UK':
        return UnitedKingdom()
