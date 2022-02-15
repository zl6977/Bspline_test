import csv
from itertools import count
import math
from cv2 import sort
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

x = []
y = []
with open('data45.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    for row in data:
        [xx, yy] = row[0].split(",")
        # print("xx,yy", xx, yy)
        count += 1
        if count % 1 == 0:
            x.append(float(xx))
            y.append(float(yy))


def SortInput(Xin, Yin):
    XTemp = Xin.copy()
    XTemp.sort()
    Xout = XTemp
    Yout = []
    for x in Xout:
        index = Xin.index(x)
        Yout.append(Yin[index])
    return Xout, Yout


x, y = SortInput(x, y)
tck = interpolate.splrep(x, y, s=0, k=4)
xnew = 0.1
ynew = interpolate.splev(xnew, tck, der=0)
dydx = interpolate.splev(xnew, tck, der=1)
# print("tck:", func)

cs = interpolate.Akima1DInterpolator(x, y)


def function(xIn):
    y = interpolate.splev(xIn, tck, der=0)
    # y = cs(xIn)
    return y


def dydx(xIn):
    dydx = interpolate.splev(xIn, tck, der=1)
    return dydx


def dydx0(xIn):
    h = 0.000001
    x_l = xIn 
    x_r = xIn + h
    y_l = function(x_l)
    y_r = function(x_r)
    dx = x_r - x_l
    dy = y_r - y_l
    dydx = dy / dx
    return dydx


def d2ydx2(xIn):
    d2ydx2 = interpolate.splev(xIn, tck, der=2)
    return d2ydx2


def d2ydx20(xIn):
    h = 0.0000001
    x_l = xIn 
    x_r = xIn +h
    y_l = dydx(x_l)
    y_r = dydx(x_r)
    dx = x_r - x_l
    dy = y_r - y_l
    d2ydx2 = dy / dx
    return d2ydx2


def d2ydx21(xIn):
    h = 0.001
    x_m = xIn
    x_l = xIn - h
    x_r = xIn + h
    y_m = function(x_m)
    y_l = function(x_l)
    y_r = function(x_r)
    d2ydx2 = (y_r + y_l - 2 * y_m) / h**2
    return d2ydx2


xintpl = np.linspace(x[0], x[-1], 500)
yintpl = []
for xIn in xintpl:
    yintpl.append(function(xIn))
    # print(xIn, function(xIn))

dyLst = []
for xIn in xintpl:
    dyLst.append(dydx(xIn))

d2yLst = []
for xIn in xintpl:
    d2yLst.append(d2ydx2(x))

with open('der2.csv','w', newline='') as csvfile:
    der2 = csv.writer(csvfile, delimiter=',', quotechar='|')
    for i in range(len(xintpl)):
        der2.writerow([xintpl[i],interpolate.splev(xintpl[i], tck, der=2)])

curvature = []
for xIn in xintpl:
    curv = abs(d2ydx2(xIn)) / (1 + (dydx(xIn))**2)**(3 / 2)
    # print(curv)
    curvature.append(curv)

# plt.figure()
# plt.plot(x, y, "x")
# plt.plot(xintpl, yintpl)
# # plt.plot(xintpl, curvature)

# plt.legend(['sample points', 'cubic spline'])
# # plt.axis([-0.05, 0.3, -1.05, 1.05])
# plt.title('Cubic-spline interpolation')
# plt.show()

# t = np.arange(0.01, 10.0, 0.01)
# data1 = np.exp(t)
# data2 = np.sin(2 * np.pi * t)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('x')
ax1.set_ylabel('y', color=color)
ax1.plot(xintpl, yintpl, color=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('curvature', color=color)  # we already handled the x-label with ax1
ax2.plot(xintpl, curvature, color=color)
ax2.tick_params(axis='y', labelcolor=color)

for x in xintpl:
    ax2.plot(x, dydx(x), "d", color=color)
    ax2.plot(x, d2ydx2(x), "s", color=color)
    # ax2.plot(x, interpolate.splev(x, tck, der=3), "s", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()