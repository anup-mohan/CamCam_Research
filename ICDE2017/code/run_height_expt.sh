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
		result_file=$method$us$ds$us$dim$ext
		outfile=$dim$ext
		
		# Calculate height distribution
		echo "python ../../../get_height.py $result_file $outfile"	
		python ../../../get_height.py $result_file $outfile
		
		# Go back one folder
		cd ../
		
		echo "$target_folder done"
		
	done
	
	# Go back one folder
	cd ../
	
	# Increment to next dataset
	count=${count+1}
	
done
