import xlwings as xw
import datetime
OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)


@xw.func
def axTimeSeriesScript(obj):

    def ole_to_datetime(ole):
        """ Input:  ole - float. Gives ole time, the number of DAYS since midnight 12/30/1899
            Output: float - epoch time
        """
        return OLE_TIME_ZERO + datetime.timedelta(days=float(ole))

    def to_float(v):
        if v == -2146826246:
            return None
        else:
            return v
    n = len(obj)
    index = [row[0] for row in obj[1:]]
    values = [to_float(row[1]) for row in obj[1:]]
    dates = []
    for i in index:
        if isinstance(i, datetime.datetime):
            d = i
        else:
            d = ole_to_datetime(i)
        dates.append('datetime.datetime(%s, %s, %s)' % (d.year, d.month, d.day))
    name = obj[0][1]
    script = 'TimeSeries(index = [%s], value = %s, name = "%s")' % (', '.join(dates), values, name) 
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(script.encode('utf-8'), win32clipboard.CF_TEXT)
    #win32clipboard.SetClipboardText(unicode(script), win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return True




if __name__ == '__main__':
    xw.serve()