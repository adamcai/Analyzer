import numpy
from pyanalyzer.stats.timeseries import TimeSeries
from unittest import TestCase
from pyanalyzer.calendar import Calendar


class not_implemented(object):

    def __init__(self, kwargs_name):
        self.kwargs_name = kwargs_name

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            kwarg = kwargs.pop(self.kwargs_name, None)
            if kwarg is not None:
                raise NotImplementedError('%s is not implemented' % self.kwargs_name)
            return f(*args, **kwargs)
        return wrapper

def time_scaling(d1, d2, calendar : Calendar = None):
    from pyanalyzer.calendar import WeekdayCalendar
    return (calendar if calendar is not None else WeekdayCalendar()).business_days_between(d1, d2) ** 0.5

def diff_return(ts, lag, scaling : bool = True, calendar : Calendar = None):

    if lag < 0:
        raise ValueError("lag must be >= 0")
    r = ts - ts.shift(lag) 
    if scaling:
    
        n = len(ts)
        for i in range(n - lag):
            d1 = ts.index[i]
            d2 = ts.index[i + lag]
            factor = time_scaling(d1, d2, calendar)
            r.iloc[i + lag] = r.iloc[i + lag] / factor
    return r

def rv(ts, window, rtype = 'N', lag = 1, drift = True, scaling = True, calendar : Calendar = None):
    ''' calculate timeseries realized vol
        
        Keyword arguments:
        ts -- time Series
        window -- estimation window for rv. must be integer > 1
        rtype -- return type. N<default> = normal vol(i.e. diff return) 
        lag -- return lag. For now it has to be integer
        drift -- timeseries has drift
     '''
    if rtype == 'N':
        return_ts = diff_return(ts, lag, scaling, calendar)
    else:
        raise ValueError("Invalid rtype input %s" % rtype)
    rv_result = []
    for i in range(len(return_ts)):
        if numpy.isnan(return_ts.iloc[i]) or i < window:
            rv_result.append(numpy.NaN)
            continue
        window_ts = return_ts.iloc[i - window + 1:i + 1]
        if drift:
            rv_result.append(window_ts.std())
        else:
            rv_result.append(sum(v ** 2 for v in window_ts) / (window - 1))
    return TimeSeries(index = ts.index, data = rv_result, name = ts.name)


    



    





