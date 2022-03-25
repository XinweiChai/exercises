import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from pandas.tseries.offsets import MonthEnd


# date_parser = lambda dat: datetime.strptime(dat, '%m/%d/%Y')

def date_parser(dat):
    return datetime.strptime(dat, '%m/%d/%Y')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + relativedelta(days=n)


def monthrange(start_date, end_date):
    for n in range(int((end_date - start_date).months)):
        yield start_date + relativedelta(months=n)


start = datetime.strptime('2020-01-26', '%Y-%m-%d')
end = datetime.strptime('2022-03-05', '%Y-%m-%d')

# x = pd.read_csv('confirmed.csv', parse_dates=['time'], date_parser=date_parser)
# x['yearmonth'] = x['time'].dt.strftime('%Y-%m')


# x = x[['city_zipCode', 'yearmonth', 'confirmed']]
# cols = list(x.columns)
# cols.remove('confirmed')
# y = x.groupby(cols).sum()
# y.to_csv('res.csv')
#
y = pd.read_csv('res.csv', parse_dates=['yearmonth'])
# y['has_confirmed'] = np.where(y['confirmed'] == 0, 0, 1)
# y['continue_confirmed'] = 0
#
# x = x[['city_zipCode', 'yearmonth', 'time', 'confirmed']]
# z = x[(x['time'] == x['time'] + MonthEnd(0))]
# z.to_csv('z.csv', index=False)
#
# z = pd.read_csv('z.csv', parse_dates=['yearmonth'])
# y = y.join(z, on='yearmonth')
# aaa = 1
# for i in monthrange(start_date=start, end_date=end):
# y['continue_confirmed'] = np.where(
# (z['confirmed'] == 0) & (z['time'] == pd.to_datetime(y['yearmonth'], format="%Y-%m") + MonthEnd(1)), 0, 1)
# (x['time'].dt.year == y['time'].dt.year) & (x['time'].dt.month == y['time'].dt.month) & x['time'].dt.day==)
# y.to_csv('res2.csv')
# x = x[['provinceName', 'provinceEnglishName', 'province_zipCode', 'time', 'confirmed']]

# for i in daterange(start_date=start, end_date=end):
