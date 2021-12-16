# coding: utf-8
"""
Name: analyze_trackdata.py

detect rapid deeping rate, minimup prmsl.

Usage: python3 analyse_trackdata.py

Author: Ryosuke Tomita
Date: 2021/12/15
"""
import argparse
import pandas as pd
import dataclasses


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


@dataclasses.dataclass
class MeteoData:
    csvfile: str

    def __post_init__(self):
        self.df = pd.read_csv(self.csvfile, header=0)
        print(f"-----{self.csvfile}-----")

        self.rapid_deeping_rate_time = None
        self.min_prmsl_time = None
        self.min_prmsl_index: int
        self.rapid_deeping_rate_index: int

    def find_rapid_deepingrate(self):
        self.rapid_deeping_rate_index = self.df["deeping_rate"].idxmax()

        event_day = self.df["date"][self.rapid_deeping_rate_index]
        lat = self.df["lat"][self.rapid_deeping_rate_index]
        lon = self.df["lon"][self.rapid_deeping_rate_index]
        event_dict = {"rapid_dr": self.df["deeping_rate"][self.rapid_deeping_rate_index]}

        self.rapid_deeping_rate_time = EventDatetime(event_day, lat, lon, event_dict)

    def find_min_prmsl(self):
        self.min_prmsl_index = self.df["prmsl"].idxmin()

        event_day = self.df["date"][self.min_prmsl_index]
        lat = self.df["lat"][self.min_prmsl_index]
        lon = self.df["lon"][self.min_prmsl_index]
        event_dict = {"min_prmsl": self.df["prmsl"][self.min_prmsl_index]}

        self.min_prmsl_time = EventDatetime(event_day, lat, lon, event_dict)

    def __str__(self):
        rapid_dr = f'rapid_deeping_rate'
        rapid_dr_value = f'{self.rapid_deeping_rate_time.event_dict["rapid_dr"]}'
        rapid_dr_time = f'{self.rapid_deeping_rate_time.event_day}'
        rapid_dr_lat = f'{self.rapid_deeping_rate_time.lat}'
        rapid_dr_lon = f'{self.rapid_deeping_rate_time.lon}'

        min_prmsl_value = f'{self.min_prmsl_time.event_dict["min_prmsl"]}'
        min_prmsl_time = f'{self.min_prmsl_time.event_day}'
        min_prmsl_lat = f'{self.min_prmsl_time.lat}'
        min_prmsl_lon = f'{self.min_prmsl_time.lon}'

        return f'{rapid_dr}, {rapid_dr_value}, {rapid_dr_time}, {rapid_dr_lat}, {rapid_dr_lon}\n\
min_prmls, {min_prmsl_value}hPa, {min_prmsl_time}, {min_prmsl_lat}, {min_prmsl_lon}'


@dataclasses.dataclass
class EventDatetime:
    event_day: str
    lat: float
    lon: float
    event_dict: dict


def main():
    args = parse_args()
    if args["dir"] is not None:
        #csvfile_list = g
        exit()
    else:
        csvfile = args["file"]

        meteo_data = MeteoData(csvfile)
        meteo_data.find_rapid_deepingrate()
        meteo_data.find_min_prmsl()
        print(meteo_data)


if __name__ == "__main__":
    main()
