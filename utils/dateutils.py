import datetime, time

def datetime2time(dt):
    return time.mktime(dt.timetuple())
    
def time2datetime(t):
    return datetime.datetime.fromtimestamp(t)

def date_range(start, end):
    max_interval = 30
    delta = end - start
    if delta.days < max_interval:
        oneday_delta1 = datetime.timedelta(1)
    else:
        oneday_delta1 = datetime.timedelta( delta.days/max_interval+1 )

    itday = start
    while itday <= end:
        tmpday = itday + oneday_delta1
        yield itday, tmpday - datetime.timedelta(1)
        itday = tmpday

        def today0():
    today = datetime.date.today()
    today0 = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    return today0

def today0():
    today = datetime.date.today()
    today0 = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    return today0

def todaymidnight(today0):
    delta = datetime.timedelta(1, 0, -1)
    return today0 + delta

def tomorrow0(today0):
    delta = datetime.timedelta(1)
    return today0 + delta

def yesterday0(today0):
    delta = datetime.timedelta(1)
    return today0 - delta

def safeDate(year, month, day):
    def _safe(year, month, day):
        try:
            return datetime.date(year, month, day)
        except ValueError:
            return False

    while(True):
        d = _safe(year, month, day)
        if d:
            return d
        else:
            day = day - 1

def prevmonthRange(today0):
    cur_month = today0.month
    delta = datetime.timedelta(1)
    prevmonth_last = datetime.date(today0.year, today0.month, 1) - delta
    prevmonth_first = datetime.date(prevmonth_last.year, prevmonth_last.month, 1)
    return prevmonth_first, prevmonth_last

def nextYearMonth(cur_year, cur_month):
    if cur_month < 12:
        next_month = cur_month + 1
        next_year = cur_year
    else:
        next_month = 1
        next_year = cur_year + 1
    return next_year, next_month

def nextmonthRange(today0):
    delta = datetime.timedelta(1)

    next_year, next_month = nextYearMonth(today0.year, today0.month)
    next_year1, next_month1 = nextYearMonth(next_year, next_month)

    nextmonth_first = datetime.date(next_year, next_month, 1)
    nextmonth_last = datetime.date(next_year1, next_month1, 1) - delta

    return nextmonth_first, nextmonth_last

def detailDateRange(year, month, day):
    today = datetime.datetime(int(year),int(month),int(day),0,0,0)
    tomorrow = tomorrow0(today)
    yesterday = yesterday0(today)
    today_midnight = todaymidnight(today)
    nextday = datetime.date(tomorrow.year, tomorrow.month, tomorrow.day)
    prevday = datetime.date(yesterday.year, yesterday.month, yesterday.day)
    return today, today_midnight, prevday, nextday

    