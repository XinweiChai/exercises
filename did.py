import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm


def time(string, form="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(string, form)


def date(string, form="%Y-%m-%d"):
    return datetime.strptime(string, form)


begin_new_year = {2019: date("2019-02-04"), 2020: date("2020-01-24")}
end_new_year = {2019: date("2019-02-11"), 2020: date("2020-02-10")}
mitigate = date("2020-02-17")


def assembly():
    bikes = pd.read_csv('res_day.csv')
    weather = pd.read_csv('weather.csv')
    weather['date'] = weather.apply(
        lambda y: str(int(y['year'])) + '-' + str(int(y['month'])).zfill(2) + '-' + str(int(y['day'])).zfill(2), axis=1)
    weather = weather[['precipitation', 'temperature', 'date']]
    out = weather.join(bikes.set_index('date'), on='date', how='right')
    out.to_csv('2020.csv', index=False)


def features(df, year):
    df.loc[df["date"].dt.weekday >= 5, "weekend"] = 1
    df.loc[df['weekend'].isnull(), 'weekend'] = 0
    df.loc[(df["date"] >= begin_new_year[year]) & (df["date"] <= end_new_year[year]), "newyear"] = 1
    df.loc[df['newyear'].isnull(), 'newyear'] = 0
    df.loc[(df["date"] <= begin_new_year[year]) & (df["date"].dt.year == 2020), "before"] = 1
    df.loc[df['before'].isnull(), 'before'] = 0
    df.loc[(df["date"] >= begin_new_year[year]) & (df["date"] <= mitigate), "during"] = 1
    df.loc[df['during'].isnull(), 'during'] = 0
    df.loc[df["date"] >= mitigate, "after"] = 1
    df.loc[df['after'].isnull(), 'after'] = 0
    df.loc[df["date"].dt.year == 2020, "year_2020"] = 1
    df.loc[df['year_2020'].isnull(), 'year_2020'] = 0
    df = df.drop(columns=['date'])
    # df[['weekend', 'newyear', 'before', 'during', 'after']] = df[
    #     ['weekend', 'newyear', 'before', 'during', 'after']].astype(int)
    df.to_csv(f"feature_{year}.csv", index=False)


def combine():
    df1 = pd.read_csv("feature_2019.csv")
    df2 = pd.read_csv("feature_2020.csv")
    x = pd.concat([df1, df2])
    x.to_csv("combine.csv", index=False)


if __name__ == '__main__':
    # assembly()
    # for i in [2019, 2020]:
    #     df = pd.read_csv(f"{i}.csv", parse_dates=['date'], date_parser=lambda x: date(x))
    #     features(df, i)
    # combine()
    x = pd.read_csv("combine.csv")
    X = x.drop(columns=['count'])
    y = x['count']
    # X = StandardScaler().fit_transform(X)

    reg = LinearRegression().fit(X, y)
    coeff = reg.coef_
    print(reg.score(X, y))
    print(reg.intercept_)
    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()
    print(est.summary())
