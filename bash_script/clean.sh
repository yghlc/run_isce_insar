#!/bin/bash

rm processLog.txt

for pair in $(ls -d ????????_????????); do

	echo $pair
	rm -r $pair
	rm -r result/${pair}*
done	

#rm -r 20171222_20180103 
#rm -r result/20171222_20180103*
