# coding: utf-8
import os
from os.path import abspath, join
import datetime
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
    datetime_list = []
    prmsl_file_list = [
            abspath(join(data_root_dir, file_))
            for file_ in sorted(os.listdir(data_root_dir))
    ]
    for file_ in prmsl_file_list:
        #if "prmsl" not in file_:
        #    continue
        ds = netCDF4.Dataset(file_, 'r')
        time = ds.variables["time"]
        date_time = str(netCDF4.num2date(time[0], time.units)).replace(" ", "_")[:13] # convert units
        if date_time in datetime_list:
            date_time = _fix_datetime(date_time)
        datetime_list.append(date_time)
    return dict(zip(datetime_list, prmsl_file_list))


def _fix_datetime(date_time: str) -> str:
    """fix_datetime.
    Used in mk_file_list()

    GPV data timedelta is 12 hours.
    So, I used gpv_mk_prmsl_average.py to make average 6 hours.
        (saved in analyze_tool/)
    But, it cannot replace netcdf "time" values.
    This function can datetime + 6 hours
        to prevent using dictionary () use same key.

    Args:
        date_time (str): date_time

    Returns:
        str:
    """
    date_time_obj = datetime.datetime.strptime(date_time, "%Y-%m-%d_%H")
    fixed_date_time_obj = date_time_obj + datetime.timedelta(hours=6)
    return fixed_date_time_obj.strftime("%Y-%m-%d_%H")


#print(mk_file_list("/home/tomita/data_ini/prmsl"))

