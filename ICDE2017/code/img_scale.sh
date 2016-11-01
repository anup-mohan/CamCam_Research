#!/bin/bash

# Write the folder name containing images
files=$1
res_files=$2
rel_path="../"
resn=$3
format=$4

#Move to that directory
cd $files

for filename in `ls` 
do
	test=`echo $filename | cut -d"." -f2`	# Look at the extention
	if [ "$test" == "$format" ]; then	# change here to resize different image extentions
		res_fname=$rel_path$res_files$filename
		convert $filename -adaptive-resize $resn $res_fname # Specify the size here eg:110x110
		#echo $res_files$filename
	fi
done


