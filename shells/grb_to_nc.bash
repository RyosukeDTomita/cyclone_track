#!/bin/bash
##########################################################################
# Name: grb_to_nc.bash
#
# convert grib file to netcdf.
#
# Usage: ./grb_to_nc.bash <directory>
#
# Author: Ryosuke Tomita
# Date: 2021/12/18
##########################################################################
DIR=$1
grib_list=($(find $DIR -type f))
for i in ${!grib_list[@]};
do
    cdo -f nc copy ${grib_list[$i]} "${grib_list[$i]}_prmsl_nc"
done
