# codng: utf-8
"""
Name: fetchtime.py

Read netcdf file "time" to make output name.

Usage: This is the module.

Author: Ryosuke Tomita
Date: 2021/12/20
"""
import datetime
import netCDF4


def fetch_time(ncfile: str) -> str:
    """fetch_time.
    from ncfile, read "time"

    Args:
        ncfile (str): ncfile

    Returns:
        str:
    """
    data_set = netCDF4.Dataset(ncfile, 'r')
    time = data_set.variables["time"]
    date_time = str(netCDF4.num2date(time[0], time.units)).replace(" ", "_")[:13]
    return date_time


def fix_datetime(date_time: str) -> str:
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
