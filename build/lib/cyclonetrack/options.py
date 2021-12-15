# coding: utf-8
import argparse


def parse_args() -> dict:
    """parse_args.
    From stdin, set ambiguous cycloen formation location(lat, lon)
        ncfile's root_dir path, cyclone formation time.

    Args:

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y", "--lat", help="Center of low pressure latitude", type=float)
    parser.add_argument(
        "-x", "--lon", help="Center of low pressure longitude", type=float)
    parser.add_argument(
        "-d", "--dir", help="set directory name. This is the initial time.", type=str)
    parser.add_argument(
        "-t", "--time", help="set starttime. Format is yy-mm-dd_hh.", type=str)
    p = parser.parse_args()
    args = {"lat": p.lat, "lon": p.lon, "dir": p.dir, "time": p.time}
    return args
