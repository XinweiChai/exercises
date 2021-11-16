import numpy as np
from numpy import array, log
from scipy.stats import gamma
import matplotlib.pyplot as plt

c0 = 2.515517
c1 = 0.802853
c2 = 0.010328
d1 = 1.432788
d2 = 0.189269
d3 = 0.001308


def spi(sample, x0):
    x = array(sample)
    size_x = len(x)
    x = x[x != 0]
    F = 1 - len(x) / size_x
    if x0 == 0:
        if len(x) == size_x:
            return float('-inf')
    else:
        x_bar = x.mean()
        A = log(x_bar) - log(x).mean()

        gamma_ = (1 + (1 + 4 * A / 3) ** 0.5) / (4 * A)
        beta = x_bar / gamma_

        # fig, ax = plt.subplots(1, 1)
        # fit_alpha, fit_loc, fit_beta = gamma.fit(x)
        # print(fit_alpha - gamma_)
        # print(fit_beta - beta)
        # range_ = np.linspace(0, 10, 1000)
        # ax.plot(range_, gamma(fit_alpha, scale=fit_beta, loc=fit_loc).pdf(range_),
        #         'g-', lw=5, alpha=0.6, label='gamma cdf')
        # ax.plot(range_, gamma(gamma_, scale=beta).pdf(range_),
        #         'r-', lw=5, alpha=0.6, label='gamma cdf')
        # ax.hist(x, density=True, histtype='stepfilled', alpha=0.2)
        # ax.legend(loc='best', frameon=False)
        # plt.show()

        F = F + (1 - F) * gamma(gamma_, scale=beta).cdf(x0)
    t = (-2 * log(F)) ** 0.5 if F <= 0.5 else (-2 * log(1 - F)) ** 0.5
    S = 1 if F > 0.5 else -1
    Z = S * (t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1))
    return Z


if __name__ == '__main__':
    # print(spi([0, 0, 1, 2, 3, 4, 5], 3000))
    # print(spi(np.linspace(gamma.ppf(0.01, 1.99), gamma.ppf(0.99, 1.99), 1000), 0.5))
    # print(spi(gamma.rvs(1.99, size=1000), 0.5))
    x = [278, 178.5, 206.5, 136.8, 181.1, 142.6, 297.6, 115.2, 344.7, 256.1, 187.9, 196.6, 304.1, 243, 256.5, 260.8,
         269, 137.9, 262.9, 239.3, 197.4, 353.3, 409.9, 181.2, 196.6, 223.5, 663.5, 173.5, 211.5, 168, 183.8, 365.6,
         108.6, 143.1, 117.1, 88.8, 130.6, 201.4, 120.1, 191, 303.5, 305.3, 323.1]
    print(spi(x, 278))
