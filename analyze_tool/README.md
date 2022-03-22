# Analyze
- [analyze_trackdata.py](analyze_trackdata.py): analyze trackdata and find the biggest deeping rate, smallest pressure.

```shell
python3 analyze_trackdata.py --file ../result.csv.sample
-----../result.csv.sample-----
rapid_deeping_rate, 1.189240693415949, 2021-01-06_12, 37.96947695247193, 137.0121089085264
min_prmls, 952.0461161360952hPa, 2021-01-09_12, 52.12003425506129, 180.0032441690557
```
- [cyclone_loc.py](cyclone_loc.py): Plot cyclone center location.

```shell
python3 cyclone_loc.py --file ../result.csv.sample
```

- [low_pressure_detecter.py](low_pressure_detecter.py): low pressure detecter.

```shell
python3 low_pressure_detecter.py --file ../result.csv.sample
```
- [prmsl_dr.py](prmsl_dr.py)

```shell
python3 prmsl_dr.py --file ../result.csv.sample
```
- [japanmap.py](japanmap.py): japan map plot modules.
