#!/bin/bash

# Input variables
dataset=("CAM2" "INRIA")
dimensions=("75%" "50%" "40%" "30%" "25%" "10%" "100%")
frcn_path=$1
tpfilename="true_positives.csv"
fpfilename="false_positives.csv"
fnfilename="false_negatives.csv"
slash="/"
parent_folder="../../"
all_imgs=("*.jpg" "*.png")
count=0

for ds in "${dataset[@]}"
do
	# Change directory to the database
	cd $ds
	
	for dim in "${dimensions[@]}"
	do
		# Change directory to the dimension
		cd $dim
		
		# Generate file names
		tpfile=$parent_folder$frcn_path$ds$slash$dim$slash$tpfilename
		fpfile=$parent_folder$frcn_path$ds$slash$dim$slash$fpfilename
		fnfile=$parent_folder$frcn_path$ds$slash$dim$slash$fnfilename
		imgs=${all_imgs[$count]}
		
		# Generate accuracy and height information
		echo "python ../../../calcCaffePR.py $tpfile $fpfile $fnfile $dim $ds $imgs"	
		python ../../../calcCaffePR.py $tpfile $fpfile $fnfile $dim $ds $imgs
		
		# Go back one folder
		cd ../
		
		echo "$target_folder done"
		
	done
	
	# Go back one folder
	cd ../
	
	# Increment to next dataset
	count=${count+1}
	
done
