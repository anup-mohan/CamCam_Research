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
method="HoG"
ext=".txt"


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
		htfile=$dim$ext
		
		# Calculate accuracy
		echo "python ../../../calcAccuracy.py $gt_folder $result_file $dim $imgs"	
		python ../../../calcAccuracy.py $gt_folder $result_file $dim $imgs
		
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
