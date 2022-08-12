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

        F = F + (1 - F) * gamma(gamma_, scale=beta).cdf(x0)
    S = 1 if F > 0.5 else -1
    t = (-2 * log(F)) ** 0.5
    Z = S * (t - (c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1)
    return Z