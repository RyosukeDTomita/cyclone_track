# coding: utf-8
"""
Name: mk_file_list.py

make netcdf file list.

Usage: module

Author: Ryosuke Tomita
Date: 2021/12/18
"""
import os
from os.path import abspath, join
from cyclonetrack import fetchtime
import copy
import netCDF4


def mk_file_list(data_root_dir: str) -> dict:
    """mk_prmsl_file_list.
    data_root_dir should be consisted by only prmsl netcdf file.

    This function use fix_datetime().

    Args:
        data_root_dir (str): data_root_dir
        start_date (datetime): start_date

    Returns:
        list:
    """
    prmsl_file_list = [
            abspath(join(data_root_dir, file_))
            for file_ in sorted(os.listdir(data_root_dir))
    ]

    datetime_list = []
    for file_ in copy.copy(prmsl_file_list):
        if "prmsl" not in file_:
            prmsl_file_list.remove(file_)
            continue

        date_time = fetchtime.fetch_time(file_)

        if date_time in datetime_list:
            date_time = fetchtime.fix_datetime(date_time)

        datetime_list.append(date_time)
    return dict(zip(datetime_list, prmsl_file_list))


