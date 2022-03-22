#!/bin/bash
#-----2021/01/06----------
python3 -m cyclonetrack -x 135 -y 37 --dir ~/data_ini/prmsl -t 2021-01-06_12 --filetype GPV
#python3 -m cyclonetrack -x 135 -y 37 --dir /media/tomita/480/0106/2020122712 -t 2021-01-06_12 --filetype GPV
#python3 -m cyclonetrack -x 140 -y 45 --dir /media/tomita/480/0106/2020122812 -t 2021-01-06_12 --filetype GPV
python3 -m cyclonetrack -x 135 -y 37 --dir ~/jra55/anl_surf125/202101 -t 2021-01-06_12 --filetype jra55

#dir_list=($(find /media/tomita/480/0106/ -type d | sort))
#for i in ${!dir_list[@]};
#do
#    echo ${dir_list[$i]}
#    python3 -m cyclonetrack -x 135 -y 37 --dir ${dir_list[$i]} -t2021-01-06_12 --filetype GPV
#done

#-----2020/12/12----------
#python3 -m cyclonetrack -x 142 -y 36 --dir ~/data_ini/prmsl -t 2020-12-12_12 --filetype GPV
#python3 -m cyclonetrack -x 115 -y 40 --dir /media/tomita/480/1212/2020120612 -t 2020-12-12_06 --filetype GPV
#python3 -m cyclonetrack -x 150 -y 35 --dir /media/tomita/480/1212/2020120712 -t 2020-12-12_18 --filetype GPV
#python3 -m cyclonetrack -x 120 -y 40 --dir /media/tomita/480/1212/2020120712 -t 2020-12-12_12 --filetype GPV
#python3 -m cyclonetrack -x 130 -y 40 --dir /media/tomita/480/1212/2020120812 -t 2020-12-12_18 --filetype GPV
#python3 -m cyclonetrack -x 130 -y 40 --dir /media/tomita/480/1212/2020120900 -t 2020-12-12_18 --filetype GPV
#python3 -m cyclonetrack -x 145 -y 35 --dir /media/tomita/480/1212/2020121100 -t 2020-12-12_06 --filetype GPV
#python3 -m cyclonetrack -x 145 -y 35 --dir /media/tomita/480/1212/2020121112 -t 2020-12-12_06 --filetype GPV

#python3 -m cyclonetrack -x 142 -y 36 --dir ~/jra55/anl_surf125/202012 -t 2020-12-12_00 --filetype jra55

#dir_list=($(find /media/tomita/480/1212/ -type d | sort))
#for i in ${!dir_list[@]};
#do
#    echo ${dir_list[$i]}
#    python3 -m cyclonetrack -x 142 -y 36 --dir ${dir_list[$i]} -t 2020-12-12_00 --filetype GPV
#done
