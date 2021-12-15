# coding: utf-8
"""
back up not used function.
"""
import numpy as np


def d_from_filterd_mins(prmsl: np.ndarray, lat: np.ndarray, lon: np.ndarray):
    # minimum value filter
    filterd_prmsl = np.where(
            ndimage.filters.minimum_filter(
                prmsl, size=(9, 9), mode=('nearest', 'wrap')
            ) == prmsl
    )

    # spherical trigonometry (球面三角法)
    dx_s = np.array([
        np.deg2rad(lon[filterd_prmsl[1]] - lo)
        for lo in lon
    ])
    y0_s = np.deg2rad(lat)
    y1_s = np.deg2rad(lat[filterd_prmsl[0]])

    cos_d_part1 = np.array([
        np.sin(y0) * np.sin(y1_s)
        for y0 in y0_s
    ])
    cos_d_part2_ = np.array([
        np.cos(y0) * np.cos(y1_s)
        for y0 in y0_s
    ])
    cos_d_part2 = np.array([
            cos_d_part2_[i] * np.cos(dx)
            for i in range(len(cos_d_part2_))
            for dx in dx_s
]).reshape(len(cos_d_part2_), len(dx_s), len(filterd_prmsl[0]))
    cos_d = np.array([
            cos_d_part1[i] + cos_d_part2[i][j]
            for i in range(len(cos_d_part1))
            for j in range(len(dx_s))
]).T.reshape(len(filterd_prmsl[0]), len(cos_d_part2_), len(dx_s))
    cos_d[cos_d > 1.0] = 1.0

    d_from_mins = np.arccos(cos_d) * 6400
    return d_from_mins


def _around_mean(prmsl, i, j):
    sum_data = 0
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if i == 0 and j == 0:
                continue
            sum_data += prmsl[i+i][j+i]
    return sum_data / 8


def judge_low_pressure(prmsl: np.ndarray, d_from_min: np.ndarray):
    min_around = np.where(d_from_min <= 300)
    n = np.argmin(prmsl[min_around])
    min_lat_index = min_around[0][n]
    min_lon_index = min_around[1][n]

    prmsl_min_around_mean = _around_mean(prmsl, min_lat_index, minlon_index)
    prmsl_min = prmsl[min_around].min()
    if prmsl_min_around_mean - prmsl_min >= 0.5:
        #return np.where(d <= 300, True, np.nan)
        return min_around
