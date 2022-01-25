"""
=======================================
A simple plot with a custom dashed line
=======================================

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
import numpy as np
import matplotlib.pyplot as plt

# x = np.linspace(0, 10, 500)
# dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
#
# fig, ax = plt.subplots()
# line1, = ax.plot(x, np.sin(x), '--', linewidth=2,
#                  label='Dashes set retroactively')
# line1.set_dashes(dashes)
#
# line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5],
#                  label='Dashes set proactively')
#
# ax.legend(loc='lower right')
#
# plt.show()
fig, ax = plt.subplots()
x = np.linspace(0, 5.5, 1000)
cond = [True if i > 1 else False for i in x]
y = (1 - np.exp(-0.5 * (x - 1))) * cond
z = 1 + 0 * x
plt.plot(x, y, label='$1-e^{-k(x-a)}$')
plt.plot(x, z, '--')
plt.legend(fontsize='large')
plt.xlim(0)
plt.ylim(0, 1.1)
plt.xticks(np.arange(0, 6, step=1), fontsize='large')
plt.yticks(fontsize='large')
x1 = np.array(range(4)) + 2
y1 = 1 - np.exp(-0.5 * (x1 - 1))
for i, j in zip(x1, y1):
    ax.plot(x1, y1, 'o')
    # plt.text(i, j, '%.2f' % j,)
    ax.annotate('%.2f' % j, (i, j), xytext=(i + 0.05, j - 0.05), fontsize='large')
fig.tight_layout()
plt.show()

fig, ax = plt.subplots()
x = np.linspace(0, 6, 1000)
cond = [True if i > 1 else False for i in x]
y = (x - 1) / 5 * cond
z = 1 + 0 * x
plt.plot(x, y, label='$\\dfrac{x-1}{5}$')
plt.plot(x, z, '--')
plt.legend(fontsize='large')
plt.xlim(0)
plt.ylim(0, 1.1)
plt.xticks(np.arange(0, 7, step=1), fontsize='large')
plt.yticks(fontsize='large')
x1 = np.array(range(4)) + 2
y1 = (x1 - 1) / 5
for i, j in zip(x1, y1):
    ax.plot(x1, y1, 'o')
    # plt.text(i, j, '%.2f' % j,)
    ax.annotate('%.2f' % j, (i, j), xytext=(i + 0.05, j - 0.05), fontsize='large')
fig.tight_layout()
plt.show()
