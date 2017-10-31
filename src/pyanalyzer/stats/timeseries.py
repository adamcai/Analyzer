import numpy as np
import pandas as pd

class _TimeSeries(pd.Series):

    def __init__(self, index = None, data = None, name = None):
        super(_TimeSeries, self).__init__(index = index, data = data, name = name)


    def log(self):
        return _TimeSeries(index = self.index, data = np.log(self._values), name = self.name)


def TimeSeries(index = None, data = None, name = None):

    if index is not None:
        if len(index) > 2:
            if index[0] > index[1]:
                index = index[::-1]
                if data is not None:
                    data = data[::-1]
            if not all(x<y for x, y in zip(index, index[1:])):
                raise ValueError('Index dates are not strictly increasing')
                                
    return _TimeSeries(index, data, name)
