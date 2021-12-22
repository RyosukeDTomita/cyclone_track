#!/bin/bash
#for i in $(find ~/data_ini/prmsl/ -type f | sort); do python3 low_pressure_detecter.py -f $i --type GPV ; done
for i in $(find ~/jra55/anl_surf125/202012 -type f | grep _nc | sort); do python3 ../analyze_tool/low_pressure_detecter.py -f $i --type jra55 ; done
for i in $(find ~/jra55/anl_surf125/202101 -type f | grep _nc | sort); do python3 ../analyze_tool/low_pressure_detecter.py -f $i --type jra55 ; done
