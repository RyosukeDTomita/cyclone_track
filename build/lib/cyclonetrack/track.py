# coding: utf-8
"""track.py
"""
from typing import Optional, Tuple
import dataclasses
import numpy as np
from scipy import ndimage
from cyclonetrack import biquadratic


def _around_mean(prmsl, i: int, j: int) -> float:
    """_around_mean.
    calcurate adjacent grid mean.

    Args:
        prmsl:
        i (int): i
        j (int): j

    Returns:
        float:
    """
    sum_data = 0
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if i == 0 and j == 0:
                continue
            sum_data += prmsl[i+i][j+i]
    return sum_data / 8


def find_closest_min(prmsl: np.ndarray, lat: np.ndarray, lon: np.ndarray,
            lat0: float, lon0: float) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """find_closest_min.
    find pressure center candidate.
    If candidate is found, check center pressure is 0.5 hPa
        less than adjacent grid mean(calcurated by _around_mean()).

    Args:
        prmsl (np.ndarray): prmsl
        lat (np.ndarray): lat
        lon (np.ndarray): lon
        lat0 (float): lat0
        lon0 (float): lon0

    Returns:
        Tuple[np.ndarray, np.ndarray]:
    """
    # minimum value filter
    filterd_prmsl = np.where(
            ndimage.filters.minimum_filter(
                prmsl, size=(9, 9), mode=('nearest', 'wrap')
            ) == prmsl
    )

    # spherical trigonometry (球面三角法)
    dx = np.deg2rad(lon[filterd_prmsl[1]] - lon0)
    y1 = np.deg2rad(lat[filterd_prmsl[0]])
    y0 = np.deg2rad(lat0)
    range_from_cyclone_center = np.arccos(
            np.sin(y0) * np.sin(y1) + np.cos(y0) * np.cos(y1) * np.cos(dx)) * 6400

    if range_from_cyclone_center.min() <= 300:
        n = np.argmin(range_from_cyclone_center)
        lon_cyclone_center_index = filterd_prmsl[1][n]
        lat_cyclone_center_index = filterd_prmsl[0][n]

        # check filterd min is low pressure center.
        center_prmsl = prmsl[lat_cyclone_center_index][lon_cyclone_center_index]
        around_center_prmsl_mean = _around_mean(
                prmsl, lat_cyclone_center_index, lon_cyclone_center_index
        )

        if around_center_prmsl_mean - center_prmsl >= 0.5:
            return float(lat[lat_cyclone_center_index]), float(lon[lon_cyclone_center_index])
    else:
        return None, None


def track_min(prmsl: np.ndarray, lat: np.ndarray, lon: np.ndarray, lat0: float, lon0: float, datedata: str):
    """track_min.
    track cyclone center position and
    save data to CenterInfo class.

    Args:
        prmsl (np.ndarray): prmsl
        lat (np.ndarray): lat
        lon (np.ndarray): lon
        lat0 (float): lat0
        lon0 (float): lon0
        datedata (str): datedata
    """
    # minimum value filter
    filterd_prmsl = np.where(
            ndimage.filters.minimum_filter(
                prmsl, size=(12, 12), mode=('nearest', 'wrap')
            ) == prmsl
    )

    # spherical trigonometry (球面三角法)
    dx = np.deg2rad(lon[filterd_prmsl[1]] - lon0)
    y1 = np.deg2rad(lat[filterd_prmsl[0]])
    y0 = np.deg2rad(lat0)
    range_from_center = np.arccos(
            np.sin(y0) * np.sin(y1) + np.cos(y0) * np.cos(y1) * np.cos(dx)
    )
    closest_min_index = np.argmin(range_from_center)
    lon_center_index = filterd_prmsl[1][closest_min_index]
    lat_center_index = filterd_prmsl[0][closest_min_index]
    f = biquadratic.set_stencil(prmsl, lon_center_index, lat_center_index)
    # bicubic interpolation
    x, y, prmsl_min = biquadratic.interpolate(f) # 補完前の中心座標から見て補完後のずれを単位あたりで返す

    dlon = lon[1] - lon[0]
    lon_center = (lon[lon_center_index] + y * dlon) % 360
    dlat = 0.5 * (lat[min(lat_center_index + 1, lat.size-1)] - lat[max(lat_center_index - 1, 0)])
    lat_center = min(max(lat[lat_center_index] + x * dlat, -90), 90)
    center_info = CenterInfo(lat_center, lon_center, prmsl_min,
                             lat_center_index, lon_center_index, datedata)
    return center_info


@dataclasses.dataclass
class CenterInfo:
    """CenterInfo.
    save cyclone center data made by track_min()
    """
    lat: float
    lon: float
    prmsl: float
    lat_center_index: int
    lon_center_lat: int
    date: str

    def __post_init__(self):
        """__post_init__.
        """
        self.deeping_rate = None

    def __str__(self):
        """__str__.
        """
        date = f'{self.date} UTC'
        lat = f'lat={self.lat:.2f}'
        lon = f'lon={self.lon:.2f}'
        prmsl = f'pressure={self.prmsl:7.2f}'
        return f'{date}, {lat}, {lon}, {prmsl}'
