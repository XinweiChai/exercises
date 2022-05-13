import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from pandas.tseries.offsets import MonthEnd, MonthBegin

date_formats = ['%Y-%m-%d', '%m/%d/%Y']


def date_parser(dat):
    return datetime.strptime(dat, date_formats[0])


def date_parser2(dat):
    return datetime.strptime(dat, date_formats[1])


def daterange(start_date, end_date, step):
    for n in range(int((end_date - start_date).days), step):
        yield start_date + relativedelta(days=n)


def monthrange(start_date, end_date):
    for n in range(diff_months(start_date, end_date)):
        yield start_date + relativedelta(months=n)


def diff_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month


start = datetime.strptime('2020-01-26', date_formats[0])
end = datetime.strptime('2022-03-05', date_formats[0])


def optimize_dataset():
    x = pd.read_csv('confirmed.csv', parse_dates=['time'], date_parser=date_parser2)
    x[['city_zipCode', 'city_confirmedCount', 'city_suspectedCount', 'city_curedCount', 'city_deadCount', 'time',
       'confirmed']].to_csv('confirmed_city.csv', index=False)
    x[['provinceName', 'provinceEnglishName', 'province_zipCode', 'cityName', 'city_zipCode']].drop_duplicates().to_csv(
        'city_data.csv', index=False)


def generate_yearmonth_aggregated_confirmed_data():
    x = pd.read_csv('confirmed_city.csv', parse_dates=['time'], date_parser=date_parser)
    x['yearmonth'] = x['time'].dt.strftime('%Y-%m')
    x = x[['city_zipCode', 'yearmonth', 'confirmed']]
    cols = list(x.columns)
    cols.remove('confirmed')
    y = x.groupby(cols).sum()
    y.to_csv('res.csv')


def generate_dummies():
    x = pd.read_csv('confirmed_city.csv', parse_dates=['time'], date_parser=date_parser)
    x.set_index(['time', 'city_zipCode'])
    y = pd.read_csv('res.csv', parse_dates=['yearmonth'])
    y['has_confirmed'] = np.where(y['confirmed'] == 0, 0, 1)
    y['continue_unconfirmed'] = 30
    y['continue_unconfirmed_dummy'] = 0
    y['continue_unconfirmed_last_month'] = 30
    y['continue_unconfirmed_last_month_dummy'] = 0

    for i in monthrange(start_date=start, end_date=end):
        start_m = i - MonthBegin()
        end_m = i + MonthEnd()
        t = y[y.yearmonth == start_m]
        for _, row in t.iterrows():
            if row.has_confirmed != 0:
                city_code = row.city_zipCode
                temp = x[(x.city_zipCode == city_code) & (x['time'] - MonthBegin() == row.yearmonth)]
                for j in range((end_m - start_m).days):
                    date = end_m - relativedelta(days=j)
                    t2 = temp[(city_code == temp.city_zipCode) & (date == temp.time) & (temp.confirmed != 0)]
                    if not t2.empty:
                        y.loc[(y.city_zipCode == city_code) & (y.yearmonth == start_m), 'continue_unconfirmed'] = j
                        y.loc[
                            (y.city_zipCode == city_code) & (y.yearmonth == start_m), 'continue_unconfirmed_dummy'] = 1
                        next_month = start_m + relativedelta(months=1)
                        y.loc[(y.city_zipCode == city_code) & (
                                y.yearmonth == next_month), 'continue_unconfirmed_last_month'] = j
                        y.loc[(y.city_zipCode == city_code) & (
                                y.yearmonth == next_month), 'continue_unconfirmed_last_month_dummy'] = 1
                        break
    y.to_csv('res2.csv', index=False)


def generate_dummies2():
    x = pd.read_csv('confirmed_city.csv', parse_dates=['time'], date_parser=date_parser)
    x['city_code'] = x['city_zipCode'] // 100
    x['yearmonth'] = x['time'] - MonthBegin()
    x = x[['city_code', 'yearmonth', 'time', 'confirmed']].groupby(['city_code', 'yearmonth', 'time'],
                                                                   as_index=False).sum()
    x.set_index(['time', 'city_code'])
    y = x[['city_code', 'yearmonth', 'confirmed']]
    cols = list(y.columns)
    cols.remove('confirmed')
    y = y.groupby(cols, as_index=False).sum()
    y['has_confirmed'] = np.where(y['confirmed'] == 0, 0, 1)
    y['continue_unconfirmed'] = 30
    y['continue_unconfirmed_dummy'] = 0
    y['continue_unconfirmed_last_month'] = 30
    y['continue_unconfirmed_last_month_dummy'] = 0

    for i in monthrange(start_date=start, end_date=end):
        start_m = i - MonthBegin()
        end_m = i + MonthEnd()
        t = y[y.yearmonth == start_m]
        for _, row in t.iterrows():
            if row.has_confirmed != 0:
                city_code = row.city_code
                temp = x[(x.city_code == city_code) & (x['time'] - MonthBegin() == row.yearmonth)]
                for j in range((end_m - start_m).days):
                    date = end_m - relativedelta(days=j)
                    t2 = temp[(city_code == temp.city_code) & (date == temp.time) & (temp.confirmed != 0)]
                    if not t2.empty:
                        y.loc[(y.city_code == city_code) & (y.yearmonth == start_m), 'continue_unconfirmed'] = j
                        y.loc[
                            (y.city_code == city_code) & (y.yearmonth == start_m), 'continue_unconfirmed_dummy'] = 1
                        next_month = start_m + relativedelta(months=1)
                        y.loc[(y.city_code == city_code) & (
                                y.yearmonth == next_month), 'continue_unconfirmed_last_month'] = j
                        y.loc[(y.city_code == city_code) & (
                                y.yearmonth == next_month), 'continue_unconfirmed_last_month_dummy'] = 1
                        break
    y.to_csv('res2.csv', index=False)


def aa():
    import statsmodels.api as sm
    nsample = 100
    x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)
    beta = np.array([1, 10])
    e = np.random.normal(size=nsample)
    y = np.dot(X, beta) + e
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())
    print(results.params)


if __name__ == '__main__':
    # optimize_dataset()
    # generate_yearmonth_aggregated_confirmed_data()
    # generate_dummies()
    # generate_dummies2()
    aa()
