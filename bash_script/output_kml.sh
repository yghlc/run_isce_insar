#!/bin/bash

code_dir=~/codes/PycharmProjects/run_insar
cd $code_dir
svn up
cd -

# set ISCE environment
source ~/.isce/.isceenv
export PATH=${code_dir}:$PATH

rm -r result_kml
mkdir result_kml

cd result
python ${code_dir}/convert_isce_out_to_kml.py
mv *.kml ../result_kml/.
mv *.png ../result_kml/.

cd ..

#for pair in $(ls -d ????????_????????); do
#
#   echo $pair
#
#   cd result
#
#   # output kml
#   python ${code_dir}/convert_isce_out_to_kml.py
#   mv *.kml ../result_kml/.
#   mv *.png ../result_kml/.
#   cd ..
#
#done


