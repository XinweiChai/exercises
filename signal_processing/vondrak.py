import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
from scipy import stats
import cubic_spline


def preprocess(df):
    while 1:
        u = df['data'].mean(axis=0)
        std = df['data'].std(axis=0)
        error = df[np.abs(df['data'] - u) > 3 * std]
        if error.empty:
            break
        df = df[np.abs(df['data'] - u) <= 3 * std]
    return df


def vondrak(x, y, epsilon, sigma):
    n = len(x)
    B = np.zeros((n, 1))
    p = np.ones((n, 1))
    p *= sigma

    a = np.zeros((n + 3, 1))
    b = np.zeros((n + 3, 1))
    c = np.zeros((n + 3, 1))
    d = np.zeros((n + 3, 1))
    for i in range(n - 3):
        a[i + 3] = 6 * sqrt(x[i + 2] - x[i + 1]) / ((x[i] - x[i + 1]) * (x[i] - x[i + 2]) * (x[i] - x[i + 3]))
        b[i + 3] = 6 * sqrt(x[i + 2] - x[i + 1]) / ((x[i + 1] - x[i]) * (x[i + 1] - x[i + 2]) * (x[i + 1] - x[i + 3]))
        c[i + 3] = 6 * sqrt(x[i + 2] - x[i + 1]) / ((x[i + 2] - x[i]) * (x[i + 2] - x[i + 1]) * (x[i + 2] - x[i + 3]))
        d[i + 3] = 6 * sqrt(x[i + 2] - x[i + 1]) / ((x[i + 3] - x[i]) * (x[i + 3] - x[i + 1]) * (x[i + 3] - x[i + 2]))

    A = np.zeros((n, 7))
    for i in range(n):
        A[i, 0] = a[i] * d[i]
        A[i, 1] = a[i + 1] * c[i + 1] + b[i] * d[i]
        A[i, 2] = a[i + 2] * b[i + 2] + b[i + 1] * c[i + 1] + c[i] * d[i]
        A[i, 3] = epsilon * p[i] / (n - 3) + a[i + 3] ** 2 + b[i + 2] ** 2 + c[i + 1] ** 2 + d[i] ** 2
        A[i, 4] = a[i + 3] * b[i + 3] + b[i + 2] * c[i + 2] + c[i + 1] * d[i + 1]
        A[i, 5] = a[i + 3] * c[i + 3] + b[i + 2] * d[i + 2]
        A[i, 6] = a[i + 3] * d[i + 3]
        B[i] = epsilon * p[i] / (n - 3)

    A[2, 0: 6] = A[2, 1: 7]
    A[2, 6] = 0

    A[1, 0: 5] = A[1, 2: 7]
    A[1, 5: 7] = [0, 0]

    A[0, 0: 4] = A[0, 3: 7]
    A[0, 4: 7] = [0, 0, 0]

    y = (y * B.T).T
    ls = 4
    for k in range(n - 1):
        max_value = 0
        iss = -1
        for i in range(k, ls):
            t = abs(A[i, 0])
            if t > max_value:
                max_value = t  # 列选主元
                iss = i
        if iss != -1:
            y[[k, iss], :] = y[[iss, k], :]
            A[[k, iss], :] = A[[iss, k], :]

        y[k] /= A[k, 0]
        A[k, :] /= A[k, 0]  # 系数归一化
        for i in range(k + 1, ls):
            t = A[i, 0]
            y[i] -= y[k] * t  # 常数向量消元
            A[i, :] -= A[k, :] * t  # 系数矩阵消元
            A[i, 0: 6] = A[i, 1: 7]  # 系数矩阵左移一位
            A[i, 6] = 0
        if ls != n:
            ls += 1
    q = A[n - 1, 0]
    y[n - 1] /= q
    ls = 2
    for i in range(n - 2, -1, -1):
        y[i] -= np.dot(A[i, 1:ls], y[i + 1: i + ls])
        if ls != 7:
            ls += 1
    y = np.c_[x, y]
    return y


def p(k, targs):  # 运用闭包返回p_k(x)
    def rtn_func(x):
        rtn = 1
        for i in targs:  # 累乘
            if i == k: continue  # i!=k
            rtn *= x - i[0]
            rtn /= k[0] - i[0]
        rtn *= k[1]
        return rtn

    return rtn_func


def L(*targs):  # 运用闭包返回L(x)
    funcs = [p(i, targs) for i in targs]  # 获取p_k(x)

    def rtn_func(x):
        rtn = 0
        for i in funcs: rtn += i(x)  # 执行累加
        return rtn

    return rtn_func


if __name__ == '__main__':
    # df = pd.read_csv("test_data.csv")
    df = pd.read_csv("59200原始值.txt", usecols=['time', 'data'])
    # df = pd.read_csv("59250原始值.txt", usecols=['time', 'data'])
    x_tocompute = pd.read_csv("result59200.txt").values.tolist()
    # x_tocompute = pd.read_csv("result59250.txt").values.tolist()
    x_tocompute = [i[0] for i in x_tocompute]
    ax = plt.gca()
    df.plot(x='time', y='data', ax=ax)
    df = preprocess(df)
    u = df['data'].mean(axis=0)
    std = df['data'].std(axis=0)
    print(stats.kstest(df['data'], 'norm', (u, std)))
    u = df['data'].mean(axis=0)
    std = df['data'].std(axis=0)
    df.plot(x='time', y='data', ax=ax)
    df['time'] = (df['time'] - 59200) * 24 * 60
    orig = df['time']
    # plt.show()
    eps = 1 / 4250000
    res = vondrak(df['time'].values, df['data'].values, epsilon=eps, sigma=1)
    test = np.mean(res, axis=0)
    df['time'] = df['time'] / 24 / 60 + 59200
    res[:, 0] = res[:, 0] / 24 / 60 + 59200
    li = res.tolist()
    temp = pd.DataFrame(data=li, columns=['time', 'data'])
    temp.plot(x='time', y='data', ax=ax)
    ax.legend(['original', '3-sigma', 'smoothed'])

    y2 = np.interp(x_tocompute, res[:, 0], res[:, 1])
    plt.scatter(x_tocompute, y2, label="插值", color="blue")
    x_tocompute = np.array(x_tocompute)
    final = np.c_[x_tocompute, y2]
    final = pd.DataFrame(final, columns=['time', 'data'])

    # samples = cubic_spline.grasp_sample(res[:, 0].tolist(), res[:, 1].tolist())
    # plt.plot(samples[0], samples[1], label="拟合曲线", color="black")
    # res_interpolation = cubic_spline.solve(res[:, 0].tolist(), res[:, 1].tolist(), x_tocompute)
    # plt.scatter(res[:, 0].tolist(), res[:, 1].tolist(), label="离散数据", color="red")
    # plt.scatter(x_tocompute, res_interpolation, label="插值", color="blue")
    plt.show()
    # final = pd.DataFrame(np.array(res), columns=['time', 'data'])
    # final.to_csv("59200.txt", index=False)
    # final.to_csv("59250.txt", index=False)
