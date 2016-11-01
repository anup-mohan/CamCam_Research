#!/bin/bash

# Input variables
dataset=("CAM2" "INRIA")
#dataset=("CAM2")
dimensions=("75%" "50%" "40%" "30%" "25%" "10%" "100%")
#dimensions=("75%")
slash="/"
us="_"
all_imgs=("*.jpg" "*.png")
gt="gt"
count=0
method="ACF"
ext=".txt"
parent="../"
datafn1="output_detection_"
datafn2="per.txt"

for ds in "${dataset[@]}"
do
	# Change directory to the database
	cd $ds
	
	for dim in "${dimensions[@]}"
	do
		# Change directory to the dimension
		cd $dim
		
		# Generate file and folder names	
		gt_folder=$gt$slash
		imgs=${all_imgs[$count]}
		result_file=$method$us$ds$us$dim$ext
		htfile=$method$us$ds$us$dim$ext
		dim_val=`echo $dim | cut -d"%" -f 1`
		datafile=$parent$parent$method$slash$ds$slash$dim$slash$datafn1$dim_val$datafn2
		
		# Calculate accuracy
		echo "python ../../../calcACFaccuracy.py $gt_folder $datafile $result_file $dim $imgs"	
		python ../../../calcACFaccuracy.py $gt_folder $datafile $result_file $dim $imgs
		
		# Calculate height distribution
		echo "python ../../../get_height.py $result_file $htfile"	
		python ../../../get_height.py $result_file $htfile
		
		# Go back one folder
		cd ../
		
		echo "$target_folder done"
		
	done
	
	# Go back one folder
	cd ../
	
	# Increment to next dataset
	count=${count+1}
	
done
