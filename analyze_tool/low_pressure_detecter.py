# coding: utf-8
"""
Name: low_pressure_detecter.py

detecting low pressure.

Usage: python3 low_pressure_detecter.py

Author: Ryosuke Tomita
Date: 2021/12/19
"""
import argparse
from os.path import abspath, dirname, join
import sys
import numpy as np
from scipy import ndimage
import netCDF4
import japanmap
sys.path.append(join(abspath(dirname(__file__)), "../cyclonetrack"))
import readnc
import fetchtime


def parse_args() -> dict:
    """parse_args.
    set file path.

    Args:

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="set ncfile.", type=str)
    parser.add_argument("-t", "--type", help="GPV or jra55", type=str)
    p = parser.parse_args()
    args = {"file": p.file, "type": p.type}
    return args


def d_from_filterd_min(prmsl: np.ndarray, lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """d_from_filterd_min.

    Args:
        prmsl (np.ndarray): prmsl
        lat (np.ndarray): lat
        lon (np.ndarray): lon

    Returns:
        np.ndarray:
    """
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

    d_from_min = np.arccos(cos_d) * 6400
    return d_from_min


def _around_mean(prmsl, i: int, j: int):
    """_around_mean.

    Args:
        prmsl:
        i:
        j:
    """
    sum_data = 0
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if i == 0 and j == 0:
                continue
            sum_data += prmsl[i+i][j+i]
    return sum_data / 8


def define_low_prmsl(prmsl: np.ndarray, d: np.ndarray) -> np.ndarray:
    """define_low_prmsl.

    Args:
        prmsl (np.ndarray): prmsl
        d (np.ndarray): d

    Returns:
        np.ndarray:
    """
    min_around = np.where(d <= 300)
    n = np.argmin(prmsl[min_around])
    min_lat_index = min_around[0][n]
    min_lon_index = min_around[1][n]

    prmsl_min_around_mean = _around_mean(prmsl, min_lat_index, min_lon_index)
    prmsl_min = prmsl[min_around].min()
    if prmsl_min_around_mean - prmsl_min >= 0.5:
        return np.where(d <= 300, True, np.nan)


def output_name(ncfile: str) -> str:
    """output_name.

    Args:
        ncfile (str): ncfile

    Returns:
        str:
    """
    #data_set = netCDF4.Dataset(ncfile, 'r')
    #time = data_set.variables["time"]
    #date_time = str(netCDF4.num2date(time[0], time.units)).replace(" ", "_")[:13]
    date_time = fetchtime.fetch_time(ncfile)
    if "_06" in ncfile or "_18" in ncfile:
        date_time = fetchtime.fix_datetime(date_time)
    outname = (date_time + "low_pressure")
    return outname


def main():
    """main.
    """
    args = parse_args()
    ncfile = args["file"]

    calc_phys = readnc.CalcPhysics(ncfile, args["type"])
    jp_lat, jp_lon = calc_phys.get_lat_lon()
    if args["type"] == "GPV":
        prmsl = calc_phys.get_parameter("prmsl")
    else:
        prmsl = calc_phys.get_parameter("msl") / 100

    d_from_min = d_from_filterd_min(prmsl, jp_lat, jp_lon)

    jp_map = japanmap.JpMap()
    jp_map.contour_plot(jp_lon, jp_lat, prmsl, contour_type="pressure")
    for d in d_from_min:
        min_around = define_low_prmsl(prmsl, d)
        if min_around is not None:
            jp_map.hatch_plot(jp_lon, jp_lat, min_around)

    outname = output_name(ncfile)
    jp_map.save_fig(outname, None)


if __name__ == "__main__":
    main()
