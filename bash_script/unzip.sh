#!/bin/bash

for zip in $(ls *.zip); do
    echo $zip
   unzip $zip 

done
