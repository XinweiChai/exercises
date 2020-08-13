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


def assembly(fn):
    bikes = pd.read_csv(fn, parse_dates=['date'], date_parser=lambda x: date(x))
    weather = pd.read_csv('weather.csv')
    weather['date'] = weather.apply(lambda x: datetime(year=int(x['year']), month=int(x['month']), day=int(x['day'])),
                                    axis=1)
    # lambda y: str(int(y['year'])) + '-' + str(int(y['month'])).zfill(2) + '-' + str(int(y['day'])).zfill(2), axis=1)
    # weather = weather[['precipitation', 'temperature', 'date']]
    weather = weather[['temperature', 'date']]
    out = weather.join(bikes.set_index('date'), on='date', how='right')
    return out
    # out.to_csv('2020.csv', index=False)


def features(df, year):
    df.loc[df["date"].dt.weekday >= 5, "weekend"] = 1
    df.loc[df['weekend'].isnull(), 'weekend'] = 0
    # df.loc[(df["date"] >= begin_new_year[year]) & (df["date"] <= end_new_year[year]), "newyear"] = 1
    # df.loc[df['newyear'].isnull(), 'newyear'] = 0
    df.loc[(df["date"] <= begin_new_year[year]) & (df["date"].dt.year == 2020), "before"] = 1
    df.loc[df['before'].isnull(), 'before'] = 0
    df.loc[(df["date"] > begin_new_year[year]) & (df["date"] <= mitigate), "during"] = 1
    df.loc[df['during'].isnull(), 'during'] = 0
    df.loc[df["date"] > mitigate, "after"] = 1
    df.loc[df['after'].isnull(), 'after'] = 0
    df.loc[df["date"].dt.year == 2020, "year_2020"] = 1
    df.loc[df['year_2020'].isnull(), 'year_2020'] = 0
    df = df.drop(columns=['date'])
    # df[['weekend', 'newyear', 'before', 'during', 'after']] = df[
    #     ['weekend', 'newyear', 'before', 'during', 'after']].astype(int)
    return df
    # df.to_csv(f"feature_{year}.csv", index=False)


def combine(fn1, fn2):
    df1 = pd.read_csv(fn1)
    df2 = pd.read_csv(fn2)
    x = pd.concat([df1, df2])
    x.to_csv("combine.csv", index=False)


if __name__ == '__main__':
    for i in ["", "_8h", "_10-11h", "_18h"]:
        to_combine = []
        for j in [2019, 2020]:
            # df = pd.read_csv(f"{i}.csv", parse_dates=['date'], date_parser=lambda x: date(x))
            # features(df, i)
            to_combine.append(features(assembly(f"res_{j}{i}.csv"), j))
        # combine()
        # x = pd.read_csv("combine.csv")
        x = pd.concat(to_combine)
        X = x.drop(columns=['count'])
        y = x['count']
        y = np.log(y)
        # X = StandardScaler().fit_transform(X)

        reg = LinearRegression().fit(X, y)
        coeff = reg.coef_
        print(reg.score(X, y))
        print(reg.intercept_)
        X = sm.add_constant(X)
        est = sm.OLS(y, X).fit()
        with open(f'report{i}', 'w+') as f:
            f.write(str(est.summary()))
