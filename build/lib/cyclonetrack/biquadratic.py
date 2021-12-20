# coding: utf-8
"""
Copied by https://github.com/tenomoto/pytrack/blob/master/biquadratic.py interpolate(), https://github.com/tenomoto/pytrack/blob/master/grid.py __set_stencil().
"""
import numpy as np


def set_stencil(g, i0, j0):
    ny, nx = g.shape
    ia = (i0 + nx - 1) % nx
    ib = (i0 + 1) % nx
    ja = max(j0 - 1, 0)
    jb = min(j0 + 1, ny - 1)
    f = np.zeros(9)
    #print(ja, jb, j0, ia, ib, i0)
    f[0] = g[j0, i0]
    f[1] = g[ja, ia]
    f[2] = g[ja, i0]
    f[3] = g[ja, ib]
    f[4] = g[j0, ib]
    f[5] = g[jb, ib]
    f[6] = g[jb, i0]
    f[7] = g[jb, ia]
    f[8] = g[j0, ia]
    return f


def interpolate(f):
    # f: one dimensional array storing stencil value
    #    in the following order
    #  y^
    #  1| 7 6 5
    #  0| 8 0 4
    # -1| 1 2 3
    #  ---------->
    #    -1 0 1 x

    # calculate coefficients
    c = np.zeros_like(f)
    c[0] = f[0]
    c[1] = f[4] - f[8] # fx
    c[2] = f[6] - f[2] # fy
    c[3] = f[1] - f[3] + f[5] - f[7] # fxy
    c[4] = 2.0 * (f[4] + f[8] - 2.0 * f[0])
    c[5] = 2.0 * (f[2] + f[6] - 2.0 * f[0])
    c[6] = 2.0 * (f[5] + f[7] - f[1] - f[3] - 2.0 * (f[6] - f[2]))
    c[7] = 2.0 * (f[3] + f[5] - f[1] - f[7] - 2.0 * (f[4] - f[8]))
    c[8] = 4.0 * (f[1] + f[3] + f[5] + f[7] - 2.0 * (f[2] + f[4] + f[6] + f[8]) + 4.0 * f[0])

    if __debug__ == False:
        c = c
        print("{} {:+}x {:+}y {:+}xy {:+}x^2 {:+}y^2 {:+}x^2y {:+}xy^2 {:+}x^2y^2".\
            format(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]))
        fxy = c[3]
        fxx = 2.0 * c[4]
        fyy = 2.0 * c[5]
        print("fxx = {}".format(fxy))
        print("d = {}".format(fxx * fyy - fxy * fxy))

    # b = (/-fx, -fy/)
    # d = fxx fyy - fxy^2
    # A = |fxx fxy|
    #     |fxy fyy|
    # A^(-1) = 1 | fyy -fxy|
    #          - |-fxy  fxx|
    #          d
    # x = A^(-1)b
    fx = c[1]
    fy = c[2]
    fxy = c[3]
    fxx = 2.0 * c[4]
    fyy = 2.0 * c[5]
    d = fxx * fyy - fxy * fxy
    if d != 0:
        x = ( fyy * (-fx) + (-fxy) * (-fy)) / d
        y = (-fxy * (-fx) +   fxx  * (-fy)) / d
        z = c[0] + c[1] * x + c[2] * y + c[3] * x * y \
             + c[4] * x * x + c[5] * y * y + c[6] * x * x * y \
             + c[7] * x * y * y + c[8] * x * x * y * y
    else:
        x = 0
        y = 0
        z = f[0]
    #print(z)
    return x, y, z
