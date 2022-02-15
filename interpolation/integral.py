import csv
from itertools import count
import math
from cv2 import sort
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

x = []
y = []
with open('der2.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    for row in data:
        [xx, yy] = row[0].split(",")
        # print("xx,yy", xx, yy)
        count += 1
        if count % 1 == 0:
            x.append(float(xx))
            y.append(float(yy))


def integral(x, y, s=0):
    intY = []
    for i in range(len(x) - 1):
        ds = (x[i + 1] - x[i]) * (y[i] + y[i + 1]) / 2
        s = s + ds
        intY.append(s)
    intY.append(intY[-1])
    return intY


intY = integral(x, y, 1)
intY2 = integral(x, intY, 0)

# plt.figure()
# # plt.plot(x, y)
# plt.plot(x, intY)
# plt.plot(x, intY2)

# plt.plot(xintpl, curvature)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('x')
ax1.set_ylabel('y', color=color)
ax1.plot(x, y, color=color)
ax1.plot(x, intY, color=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('y2', color=color)  # we already handled the x-label with ax1
ax2.plot(x, intY2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# for x in xintpl:
#     ax2.plot(x, dydx(x), "d", color=color)
#     ax2.plot(x, d2ydx2(x), "s", color=color)
#     # ax2.plot(x, interpolate.splev(x, tck, der=3), "s", color=color)
#     ax2.tick_params(axis='y', labelcolor=color)

# fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()