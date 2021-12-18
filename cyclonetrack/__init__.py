# coding: utf-8
"""
Usage: python3 -m cyclonetrack -x <first cyclone longitute> -y <first cyclone latitude>
    -d <directory> -t yy-mm-dd-hh

Authore: Ryosuke Tomita
Date: 2021/12/14
"""
import sys
import math
import os
from os.path import abspath, join
import re
from datetime import datetime
import csv
from cyclonetrack import mk_file_list
from cyclonetrack import readnc
from cyclonetrack import track
from .options import parse_args


def to_datetime(datetime_str: str) -> datetime:
    """to_datetime.
    convert str to datetime.

    Args:
        datetime_str (str): datetime_str

    Returns:
        datetime:
    """
    try:
        datetime_part = datetime.strptime(datetime_str, "%Y-%m-%d_%H")
        return datetime_part
    except ValueError:
        print(f"{datetime_str} is not valid format %Y-%m-%d_%H")
        sys.exit()


def cal_deeping_rate(prmsl_tracks):
    """cal_deeping_rate.

    Args:
        prmsl_tracks:
    """
    for i, center_info in enumerate(prmsl_tracks):
        if i == 0 or i == len(prmsl_tracks) - 1:
            continue
        prmsl_6hago = prmsl_tracks[i-1].prmsl
        prmsl_6hlater = prmsl_tracks[i+1].prmsl
        now_lat_rad = math.radians(center_info.lat)
        rad_45 = math.radians(45)
        center_info.deeping_rate = (
                ((prmsl_6hago - prmsl_6hlater) / 12)
                * (math.sin(rad_45) / math.sin(now_lat_rad))
        )


def to_csv(prmsl_tracks: list, outname: str):
    """to_csv.

    Args:
        prmsl_tracks (list): prmsl_tracks
        outname (str): outname
    """
    with open(outname, "w+", newline="") as csvfile:
        try:
            writer = csv.writer(csvfile)
            writer.writerow(('date', 'lat', 'lon', 'prmsl', 'deeping_rate'))
            for center_info in prmsl_tracks:
                writer.writerow((
                    center_info.date, center_info.lat, center_info.lon,
                    center_info.prmsl, center_info.deeping_rate
                ))
        finally:
            print(f"save to --> {outname}")

def main():
    """main.
    1. get stdin argument using parse_args().
    2. make "prmsl_file_dict" using mk_prmsl_file_list().
    3. find cyclone formed datetime and update "start_date".
    4. cyclone track.
    5. calcureta cyclone deeping_rate.
    6. save to csv.
    """
    args = parse_args()
    start_date = to_datetime(args["time"])
    lat0, lon0 = args["lat"], args["lon"]

    prmsl_file_dict = mk_file_list.mk_file_list(args["dir"])

    calc_phys = readnc.CalcPhysics(prmsl_file_dict[args["time"]], args["filetype"])
    jp_lat, jp_lon = calc_phys.get_lat_lon()

    # find cyclone formed datetime to update "start_date".
    formed_date = args["time"]
    for i, date in enumerate(sorted(prmsl_file_dict.keys(), reverse=True)):
        if start_date < to_datetime(date):
            continue

        if   args["filetype"] == "GPV":
            prmsl = calc_phys.get_parameter("prmsl", ncfile=prmsl_file_dict[date])
        else:
            prmsl = calc_phys.get_parameter("msl", ncfile=prmsl_file_dict[date])

        cyclone_center_lat, cyclone_center_lon = track.find_closest_min(prmsl, jp_lat, jp_lon, lat0, lon0)
        formed_date = date
        if cyclone_center_lat is None:
            print(f"cyclone formed time = {formed_date}")
            start_date = to_datetime(formed_date)
            break
        lat0 = cyclone_center_lat
        lon0 = cyclone_center_lon

    # From "start_date", track cyclone.
    prmsl_tracks = []
    for date in sorted(prmsl_file_dict.keys()):

        if start_date > to_datetime(date):
            continue

        if   args["filetype"] == "GPV":
            prmsl = calc_phys.get_parameter("prmsl", prmsl_file_dict[date])
        else:
            prmsl = calc_phys.get_parameter("msl", ncfile=prmsl_file_dict[date]) / 100

        center_info = track.track_min(prmsl, jp_lat, jp_lon, lat0, lon0, date)
        lat0 = center_info.lat
        lon0 = center_info.lon
        print(center_info)
        prmsl_tracks.append(center_info)
        if lat0 >= 60.0 or lon0 >= 180.0:
            break

    cal_deeping_rate(prmsl_tracks)

    # output
    root_dir_has_datetime = re.search('[0-9]{10}', args["dir"])
    if root_dir_has_datetime:
        outname = root_dir_has_datetime.group() + ".csv"
    else:
        outname = "initialdata.csv"
    to_csv(prmsl_tracks, outname)


__all__ = ["main", "to_datetime", "to_csv", "cal_deeping_rate"]
