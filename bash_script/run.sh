#!/bin/bash

code_dir=~/codes/PycharmProjects/run_insar
cd $code_dir
svn up
cd -

# set ISCE environment
source ~/.isce/.isceenv
export PATH=${code_dir}:$PATH

# download orbit files
#/home/hlc/programs/anaconda3/bin/python3 ${code_dir}/S1_POE_Orbit_Download.py s1a_list.txt
#mv POE/* ../orbit/.

# InSAR
/usr/bin/python2 ${code_dir}/bash_run_topsApp.sh.py 

