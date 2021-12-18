# coding: utf-8
"""
Name: cyclone_loc.py



Usage:

Author: Ryosuke Tomita
Date: 2021/12/17
"""
import argparse
import os
from os.path import abspath, join
import re
from typing import Tuple
import pandas as pd
import japanmap


def parse_args() -> dict:
    """parse_args.
    set file path or dir path.
    Not allowded file path and dir path same time.

    Args:

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="csvfile path", type=str)
    group.add_argument("-d","--dir", help="csvfile directory path", type=str)

    g = parser.parse_args()
    args = {"file": g.file, "dir": g.dir}
    return args


def mk_csv_list(dir_: str) -> list:
    csv_list = [
            abspath(join(dir_, file_))
            for file_ in sorted(os.listdir(dir_))
            if ("csv" in file_) and ("initialdata" not in file_)
    ]
    return csv_list


def mk_label(csvfile: str) -> str:
    csvfile_has_datetime = re.search("[0-9]{10}", csvfile)
    if csvfile_has_datetime:
        return csvfile_has_datetime.group()
    else:
        return "initial_data"


def read_csv(csvfile: str) -> Tuple[pd.Series, pd.Series, pd.Series]:
    #read cycloen center location, pressure(prmsl), deepingrate.
    df = pd.read_csv(csvfile, header=0)
    lat = df["lat"]
    lon = df["lon"]
    prmsl = df["prmsl"]
    return lat, lon, prmsl


def main():
    args = parse_args()
    if   args["dir"] is not None:
        csv_list = mk_csv_list(args["dir"])
        initialdata = abspath(join(args["dir"], "initialdata.csv"))

        lat, lon, prmsl = read_csv(initialdata)

        label = mk_label(initialdata)
        jp_map = japanmap.JpMap(color=True)
        jp_map.color_list.insert(0, '#696969')
        jp_map.plot_data(lat, lon, str(label))
        jp_map.plot_prmsl_circle(lat, lon, prmsl)

        for csvfile in csv_list:
            lat, lon, prmsl = read_csv(csvfile)

            label = mk_label(csvfile)
            jp_map.plot_data(lat, lon, str(label))
            jp_map.plot_prmsl_circle(lat, lon, prmsl)

        outname = "compare_track"
        jp_map.save_fig(outname, None)

    elif args["file"] is not None:

        lat, lon, prmsl = read_csv(args["file"])
        label = mk_label(args["file"])

        jp_map = japanmap.JpMap(color=True)
        jp_map.color_list.insert(0, '#696969')
        jp_map.plot_data(lat, lon, str(label))
        jp_map.plot_prmsl_circle(lat, lon, prmsl)
        jp_map.plot_value(lat, lon, prmsl)
        outname = label
        jp_map.save_fig(outname, None)


if __name__ == "__main__":
    main()
