import numpy
from pyanalyzer.stats.timeseries import TimeSeries
from unittest import TestCase



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

@not_implemented('holidays')
def _no_scaling(d1, d2, holidays = None):
    return 1

def no_scaling(d1, d2, holidays = None):
    return _no_scaling(d1, d2, holidays = holidays)

@not_implemented('holidays')
def _time_scaling(d1, d2, holidays = None):
    import datetime
    daygenerator = (d1 + datetime.timedelta(x + 1) for x in range((d2 - d1).days))
    return sum(1 for day in daygenerator if day.weekday() < 5) ** 0.5

def time_scaling(d1, d2, holidays = None):
    return _time_scaling(d1, d2, holidays)

def diff_return(ts, lag, scaling = no_scaling, holidays = None):
    if lag < 0:
        raise ValueError("lag must be >= 0")
    r = ts - ts.shift(lag) 
    n = len(ts)
    for i in range(n - lag):
        d1 = ts.index[i]
        d2 = ts.index[i + lag]
        factor = scaling(d1, d2, holidays)
        r.iloc[i + lag] = r.iloc[i + lag] / factor
        
    return r

def rv(ts, window, rtype = 'N', lag = 1, drift = False, scaling = no_scaling):
    ''' calculate timeseries realized vol
        
        Keyword arguments:
        ts -- time Series
        window -- estimation window for rv. must be integer > 1
        rtype -- return type. N<default> = normal vol(i.e. diff return) 
        lag -- return lag. For now it has to be integer
     '''


    if rtype == 'N':
        return_ts = diff_return(ts, lag, scaling)
    else:
        raise ValueError("Invalid rtype input %s" % rtype)
    rv_result = []
    for i in range(len(return_ts)):
        if numpy.isnan(return_ts.iloc[i]):
            rv_result.append(numpy.NaN)
            continue
        std = return_ts.iloc[i:i+window].std()
        rv_result.append(std)
    return TimeSeries(index = ts.index, data = rv_result, name = ts.name)


    



    





