import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def ReadDataFile(fileName, interval=1):
    s0, u1, u2, u3 = [], [], [], []
    with open(fileName, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
        count = 0
        for row in data:
            lineTmp = row[0].split(",")
            # print("xx,yy", xx, yy)
            count += 1
            if count % interval == 0:
                s0.append(float(lineTmp[0]))
                u1.append(float(lineTmp[1]))
                u2.append(float(lineTmp[2]))
                u3.append(float(lineTmp[3]))
    return s0, u1, u2, u3


def CalcCurveXYZCoodinate(s0, u1, u2, u3):
    XYZtoReturn = []
    for i in range(len(s0)):
        XYZTmp = []
        XYZTmp.append(u1[i])
        XYZTmp.append(u2[i])
        XYZTmp.append(u3[i] + s0[i])
        XYZtoReturn.append(XYZTmp)
    return XYZtoReturn


def ReadDataFile_6Columns(fileName, gap=1):
    u1, u2, u3, dx, dy, dz = [], [], [], [], [], []
    with open(fileName, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
        count = 0
        for row in data:
            lineTmp = row[0].split(",")
            # print("xx,yy", xx, yy)
            count += 1
            if count % gap == 0:
                u1.append(float(lineTmp[0]))
                u2.append(float(lineTmp[1]))
                u3.append(float(lineTmp[2]))
                dx.append(float(lineTmp[3]))
                dy.append(float(lineTmp[4]))
                dz.append(float(lineTmp[5]))
    return u1, u2, u3, dx, dy, dz


def CalcCurveXYZCoodinate_6Columns(u1, u2, u3, dx, dy, dz):
    XYZtoReturn = []
    for i in range(len(u1)):
        XYZTmp = []
        XYZTmp.append(u1[i] + dx[i])
        XYZTmp.append(u2[i] + dy[i])
        XYZTmp.append(u3[i] + dz[i])
        XYZtoReturn.append(XYZTmp)
    return XYZtoReturn


def CalcCurveParaCoodinate(x, y, z):
    SXYZtoReturn = []
    s = 0
    for i in range(len(x)):
        Rcur = np.array([x[i], y[i], z[i]])
        if i == 0:
            ds = 0
            SXYZTmp = []
            SXYZTmp.append(s)
            SXYZTmp.append(Rcur[0])
            SXYZTmp.append(Rcur[1])
            SXYZTmp.append(Rcur[2])
        else:
            Rpre = np.array([x[i - 1], y[i - 1], z[i - 1]])
            dR = Rcur - Rpre
            ds = np.linalg.norm(dR, ord=2)
            s += ds
            SXYZTmp = []
            SXYZTmp.append(s)
            SXYZTmp.append(Rcur[0])
            SXYZTmp.append(Rcur[1])
            SXYZTmp.append(Rcur[2])

        SXYZtoReturn.append(SXYZTmp)
    return SXYZtoReturn


def CalcCurveTNB(s, x, y, z):
    sTNB = []
    for i in range(len(x)):
        Rcur = np.array([x[i], y[i], z[i]])
        if i == 0:
            T = []
            N = []
            B = []
            k = 0
            tao = 0
            sTNBTmp = [s[i], T, N, B, k, tao]
            sTNB.append(sTNBTmp)
        elif i == 1:
            Rpre = np.array([x[i - 1], y[i - 1], z[i - 1]])
            dR = Rcur - Rpre
            ds = np.linalg.norm(dR, ord=2)
            T = dR / ds
            N = []
            B = []
            k = 0
            tao = 0
            # print('i',i)
            # print('T',T)
            # print('------')
            sTNBTmp = [s[i], T, N, B, k, tao]
            sTNB.append(sTNBTmp)
        elif i == 2:
            Rpre = np.array([x[i - 1], y[i - 1], z[i - 1]])
            Rprepre = np.array([x[i - 2], y[i - 2], z[i - 2]])

            dR = Rcur - Rpre
            ds = np.linalg.norm(dR, ord=2)
            T = dR / ds

            dRpre = Rpre - Rprepre
            dspre = np.linalg.norm(dRpre, ord=2)
            Tpre = dRpre / dspre

            dT = T - Tpre
            k = np.linalg.norm((dT / ds), ord=2)
            N = dT / ds / k
            B = np.cross(T, N)

            tao = 0
            # print('i',i)
            # print('T',T)
            # print('------')
            sTNBTmp = [s[i], T, N, B, k, tao]
            sTNB.append(sTNBTmp)
        else:
            Rpre = np.array([x[i - 1], y[i - 1], z[i - 1]])
            Rprepre = np.array([x[i - 2], y[i - 2], z[i - 2]])

            dR = Rcur - Rpre
            ds = np.linalg.norm(dR, ord=2)
            T = dR / ds

            # dRpre = Rpre - Rprepre
            # dspre = np.linalg.norm(dRpre, ord=2)
            # Tpre = dRpre / dspre

            Tpre = sTNB[i - 1][1]
            Bpre = sTNB[i - 1][3]

            dT = T - Tpre
            k = np.linalg.norm((dT / ds), ord=2)
            N = dT / ds / k
            B = np.cross(T, N)

            dB = B - Bpre
            tao = np.linalg.norm((dB / ds), ord=2)
            # print('i',i)
            # print('dT',dT)
            # print('k',k)
            # print('T',T)
            # print('N',N)
            # print('B',B)
            # print('------')

            sTNBTmp = [s[i], T, N, B, k, tao]
            sTNB.append(sTNBTmp)
        # sTNB.append(sTNBTmp)

    sTNB[2][5] = sTNB[3][5]

    sTNB[1][2] = sTNB[2][2]
    sTNB[1][3] = sTNB[2][3]
    sTNB[1][4] = sTNB[2][4]
    sTNB[1][5] = sTNB[2][5]

    sTNB[0][1] = sTNB[1][1]
    sTNB[0][2] = sTNB[1][2]
    sTNB[0][3] = sTNB[1][3]
    sTNB[0][4] = sTNB[1][4]
    sTNB[0][5] = sTNB[1][5]
    return sTNB


if __name__ == "__main__":

    # [s0, u1, u2, u3] = ReadDataFile('data6.csv', 4)
    # curveXYZ = CalcCurveXYZCoodinate(s0, u1, u2, u3)

    [u1, u2, u3, dx, dy, dz] = ReadDataFile_6Columns('data9-circle.csv', 80)
    curveXYZ = CalcCurveXYZCoodinate_6Columns(u1, u2, u3, dx, dy, dz)

    curve = np.array(curveXYZ)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(curve[:, 0], curve[:, 1], curve[:, 2], label='curve')
    ax.legend()

    plt.show()

    curveSXYZ = CalcCurveParaCoodinate(curve[:, 0], curve[:, 1], curve[:, 2])
    curveSXYZ = np.array(curveSXYZ)
    curveTNB = CalcCurveTNB(curveSXYZ[:, 0], curveSXYZ[:, 1], curveSXYZ[:, 2], curveSXYZ[:, 3])
    curveTNB = np.array(curveTNB)
    # for i in curveSXYZ:
    #     print(i)

    plt.figure()
    plt.plot(curveTNB[:, 0], curveTNB[:, 4])
    plt.title('Curvanture')
    plt.show()

    plt.figure()
    plt.plot(curveTNB[:, 0], curveTNB[:, 5])
    plt.title('Torsion')
    plt.show()