import numpy as np
import pandas as pd


def TimeSeries(index = None, data = None, name = None):

    if index is not None:
        if len(index) > 2:
            if index[0] > index[1]:
                index = index[::-1]
                if data is not None:
                    data = data[::-1]
            if not all(x<y for x, y in zip(index, index[1:])):
                raise ValueError('Index dates are not strictly increasing')
                                
    return pd.Series(index = index, data = data, name =  name)
