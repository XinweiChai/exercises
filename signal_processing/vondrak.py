import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
from scipy import stats


def preprocess(df, y_axis='data'):
    while 1:
        u = df[y_axis].mean(axis=0)
        std = df[y_axis].std(axis=0)
        error = df[np.abs(df[y_axis] - u) > 3 * std]
        if error.empty:
            break
        df = df[np.abs(df[y_axis] - u) <= 3 * std]
    return df


def vondrak(x, y, epsilon, sigma, x_axis='time', y_axis='data'):
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

    coeff = np.zeros((n, n))
    for i in range(n):
        for j in range(7):
            if 0 <= i + j - 3 <= n - 1:
                coeff[i][i + j - 3] = A[i][j]

    y = (y * B.T).T
    y_smooth = np.linalg.solve(coeff, y)

    # A[2, 0: 6] = A[2, 1: 7]
    # A[2, 6] = 0
    #
    # A[1, 0: 5] = A[1, 2: 7]
    # A[1, 5: 7] = [0, 0]
    #
    # A[0, 0: 4] = A[0, 3: 7]
    # A[0, 4: 7] = [0, 0, 0]
    #
    # ls = 4
    # for k in range(n - 1):
    #     max_value = 0
    #     max_line = -1
    #     for i in range(k, ls):
    #         t = abs(A[i, 0])
    #         if t > max_value:
    #             max_value = t  # 列选主元
    #             max_line = i
    #     if max_line != -1:
    #         y[[k, max_line], :] = y[[max_line, k], :]
    #         A[[k, max_line], :] = A[[max_line, k], :]
    #
    #     y[k] /= A[k, 0]
    #     A[k, :] /= A[k, 0]  # 系数归一化
    #     for i in range(k + 1, ls):
    #         t = A[i, 0]
    #         y[i] -= y[k] * t  # 常数向量消元
    #         A[i, :] -= A[k, :] * t  # 系数矩阵消元
    #         A[i, 0: 6] = A[i, 1: 7]  # 系数矩阵左移一位
    #         A[i, 6] = 0
    #     if ls != n:
    #         ls += 1
    # q = A[n - 1, 0]
    # y[n - 1] /= q
    # ls = 2
    # for i in range(n - 2, -1, -1):
    #     y[i] -= np.dot(A[i, 1:ls], y[i + 1: i + ls])
    #     if ls != 7:
    #         ls += 1
    # y = np.c_[x, y]
    return pd.DataFrame(np.c_[x, y_smooth], columns=[x_axis, y_axis])


def position(x, to_localize):
    l = x.tolist()
    for i in l:
        if to_localize < i:
            break
    return l.index(i) - 1


def interpolation_lagrange(x, y, to_compute):  # 三次样条拉格朗日插值，假设自然边界，L''=0
    n = len(x)
    solutions = []
    coeffs = np.zeros((2, 4))
    coeffs[0] = np.linalg.solve([[6 * x[0], 2, 0, 0],
                                 [x[0] ** 3, x[0] ** 2, x[0], 1],
                                 [x[1] ** 3, x[1] ** 2, x[1], 1],
                                 [x[2] ** 3, x[2] ** 2, x[2], 1]],
                                [0, y[0], y[1], y[2]])
    coeffs[1] = np.linalg.solve([[6 * x[n - 1], 2, 0, 0],
                                 [x[n - 1] ** 3, x[n - 1] ** 2, x[n - 1], 1],
                                 [x[n - 2] ** 3, x[n - 2] ** 2, x[n - 2], 1],
                                 [x[n - 3] ** 3, x[n - 3] ** 2, x[n - 3], 1]],
                                [0, y[n - 1], y[n - 2], y[n - 3]])
    for i in to_compute:
        pos = position(x, i)
        if pos <= 0:
            s = np.dot(coeffs[0], np.array([i ** 3, i ** 2, i, 1]))
        elif pos >= n - 2:
            s = np.dot(coeffs[1], np.array([i ** 3, i ** 2, i, 1]))
        else:
            s = 0
            for j in range(4):
                temp = y[pos - 1 + j]
                for k in range(4):
                    if k != j:
                        temp *= (i - x[pos - 1 + k]) / (x[pos - 1 + j] - x[pos - 1 + k])
                s += temp
        solutions.append(s)
    return solutions


def rescale(df, mean_x, x_axis='time'):  # rescale from Julian day to minute
    df[x_axis] = (df[x_axis] - mean_x) * 24 * 60
    return df


def descale(df, mean_x, x_axis='time'):
    df[x_axis] = df[x_axis] / 24 / 60 + mean_x
    return df


if __name__ == '__main__':
    eps = 1 / 4250000  # 平滑因子
    sig = 1  # 权重
    x = 'time'
    y = 'data'
    df = pd.read_csv("59200原始值.txt", usecols=[x, y])
    # df = pd.read_csv("59250原始值.txt", usecols=[x, y])
    x_tocompute = pd.read_csv("result59200.txt")
    # x_tocompute = pd.read_csv("result59250.txt")
    mean_x = df[x].mean(axis=0)
    mean_y = df[y].mean(axis=0)
    std = df[y].std(axis=0)
    print(stats.kstest(df[y], 'norm', (mean_y, std)))  # 验证是否符合正态分布（pvalue<0.05）

    x_tocompute = rescale(x_tocompute, mean_x)
    x_tocompute = x_tocompute.values.tolist()
    x_tocompute = [i[0] for i in x_tocompute]

    ax = plt.gca()
    df.plot(x=x, y=y, ax=ax)  # original data

    df = preprocess(df)
    df.plot(x=x, y=y, ax=ax)  # 3-sigma

    df = rescale(df, mean_x)
    res = vondrak(df[x].values, df[y].values, epsilon=eps, sigma=sig)

    y2 = interpolation_lagrange(res[x], res[y], x_tocompute)  # 三次样条插值
    # y2 = np.interp(x_tocompute, res[x], res[y])  # 线性插值

    res = descale(res, mean_x)
    res.plot(x=x, y=y, ax=ax)

    final = np.c_[x_tocompute, y2]
    final = pd.DataFrame(final, columns=[x, y])
    final = descale(final, mean_x)
    final.plot(x=x, y=y, ax=ax, kind='scatter', color='blue')

    ax.legend(['original', '3-sigma', 'smoothed', 'interpolation'])
    plt.show()
    final.to_csv("59200.txt", index=False)
    # final.to_csv("59250.txt", index=False)
