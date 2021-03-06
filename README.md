![日本語版README.md](./README-ja.md)
# INDEX
- [EXAMPLE](#EXAMPLE)
- [ABOUT](#ABOUT)
- [HOWTOUSE](#HOWTOUSE)
- [ENVIRONMENT](#ENVIRONMENT)
- [INSTALATION](#INSTALATION)

# EXAMPLE
![example_graph](./example_fig/0106_jra.png)
![example_track](./example_fig/JRA-55.png)
![example_track_compare](./example_fig/0106_hikaku.png)

# ABOUT
- Track cyclone center position.
- This project is created as [爆弾低気圧データベース](http://fujin.geo.kyushu-u.ac.jp/meteorol_bomb/algorithm/index.php) and [pytrack](https://github.com/tenomoto/pytrack)
- output format is csv.

## Algorithm

### 1. Find cyclone formation position and datetime.
1. Find local minima by scipy.ndimage.filters.minimum_filter() assuming a cyclic boundary conditon in longitude.
2. Find the grid of the minimum closest to the initial guess lat lon(seted by stdin). This minimum is candidate of cyclone center.
3. If cyclone center presure is 0.5 hPa less than around area pressure, define it low pressure and continue 1,2 step for 6h ago's data. If cannot find low pressure, define cyclone formation datetime is 6h ago.
### 2. Track cyclone
1. Find local minima by scipy.ndimage.filters.minimum_filter() assuming a cyclic boundary conditon in longitude.
2. Find the grid of the minimum closest to the initial guess lat lon(seted by stdin). This minimum is candidate of cyclone center.
3. Generate nine point stencil with the minimum on grid at the centre
4. Interpolate for the minimum in-between grid using biquadratic interpolation. If interpolation fails use the minimum on grid

## Data
- I used [GPV](http://database.rish.kyoto-u.ac.jp/arch/glob-atmos/) data.

- GPV netcdf files have the diffrent datetime data and pressure's unit is Pa. So, I use cdo to split and convert to Pa to hPa.
[see sample shell script](./getPrmsl.bash)
******


# HOWTOUSE
## data set construction.

```shell
ls ~/data_ini/prmsl
surface-2020-12-01_00-prmsl_hPa
surface-2020-12-01_06-prmsl_hPa
surface-2020-12-01_12-prmsl_hPa
surface-2020-12-01_18-prmsl_hPa
surface-2020-12-02_00-prmsl_hPa
surface-2020-12-02_06-prmsl_hPa
surface-2020-12-02_12-prmsl_hPa
surface-2020-12-02_18-prmsl_hPa
surface-2020-12-03_00-prmsl_hPa
surface-2020-12-03_06-prmsl_hPa
```

## run

```shell
python3 -m cyclonetrack -x 135 -y 37 --dir ~/data_ini/prmsl -t 2021-01-06_12 --filetype GPV
python3 -m cyclonetrack -x 135 -y 37 --dir ~/jra55/anl_surf125/202101 -t 2021-01-06_12 --filetype jra55
```
******


# INSTALATION
## install library

```shell
pip install -r requirements.txt
```

## build (not necessary)

### build from source cord.

```shell
git clone https://github.com/RyosukeDTomita/cyclone_track.git
cd cyclone_track
python3 setup.py install
```

### build from tar.gz(sometime flozen file is not up to date.)

```shell
wget https://github.com/RyosukeDTomita/cyclone_track/blob/master/dist/cyclone-track-0.0.1.tar.gz
pip install cyclone-track-0.0.1.tar.gz
```

 make cyclone-track-0.0.1.tar.gz

```shell
git clone https://github.com/RyosukeDTomita/cyclone_track.git
cd cyclone_track
python3 setup.py sdist
pip install ./dist/cyclone-track-0.0.1.tar.gz
```

## uninstall

```shell
python setup.py develop -u
pip uninstall cycloen-track
```
******


# ENVIRONMENT
I tested the following environment.
- Python3.8
- Ubuntu 20.04 LTS
about library, see [requirement.txt](./requirements.txt)
******


# ANARYSINGTOOL
Anarysing tool are saved in [analyze_tool/](./analyze_tool).See [README.md](analyze_tool/README.md)


# OTHER PROGRAM
[Calcureate Local Deeping Rate](https://github.com/RyosukeDTomita/cyclone_ldr)
