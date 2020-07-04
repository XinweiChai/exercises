from scipy.optimize import fsolve
from numpy import array


def func(i):
    a, b, x, y = i[0], i[1], i[2], i[3]
    return [a * x + b * y - 3,
            a * (x ** 2) + b * (y ** 2) - 7,
            a * (x ** 3) + b * (y ** 3) - 16,
            a * (x ** 4) + b * (y ** 4) - 42]


x = fsolve(func, array([0, 0, 0, 0]))
print(x[3])
print(x)
y = x[0] * (x[2] ** 5) + x[1] * (x[3] ** 5)
print(y)

from sympy.solvers import solve
from sympy import Symbol
from sympy import solve, Poly, Eq, Function, exp
from sympy.abc import x, y, a, b

sol = solve([a * x + b * y - 3,
             a * (x ** 2) + b * (y ** 2) - 7,
             a * (x ** 3) + b * (y ** 3) - 16,
             a * (x ** 4) + b * (y ** 4) - 42], dict=True)
print(sol)
for i in sol:
    print(float(i[a]) * (float(i[x]) ** 5) + float(i[b]) * (float(i[y]) ** 5))
