####################################################################################################################################
# Script to generate the rawfile to plot dup_ratio and drop_ratio vs ncams.
# The replace_newline.sh script is used to replace the newline character ^M with \n
# The results would be saved in total_efps_vs_ncams_$inst_type_.txt. 
# Where $instance_type is like A4_eus, which means an A4 instance at East US
# The result for individual cameras are also generated
# Usage: python gen_raw_dup_drop_ncams.py num_of_trials folder_name ipfile.txt
# Example: python gen_raw_dup_drop_ncams.py 29 A6_eus/result_10_28_14 base_ratio_sorted_ip.txt
####################################################################################################################################

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
import os
import linecache

# Input the no: of trials
trials = int(sys.argv[1])

# Input the instance type and subfolders
inst_folder = sys.argv[2]
inst_type = inst_folder.split("/")[0]

# Input the file containing ip address used for experiment
infile = sys.argv[3]

# Assign a position to each ip address for final lookup
ipfile = open(infile, "r")
lookup_table = []
for ip in ipfile:
	lookup_table.append(ip.split("\n")[0])

# Constants used
path_to_dir = "/home/anupmohan/Documents/Research/camcam/Result_Files/"+ str(inst_folder)+ "/"
string1 = "*_trial_"
string2 = "_*.log"

match1 = "frame="
match2 = "dup="
match3 = "drop="
len_match1 = len(match1)
len_match2 = len(match2)
len_match3 = len(match3)
LINE_OFFSET = 2

# Initializing Arrays
filenames = []
search_line = []
final_dup_value = np.zeros((trials,trials,1),float)
total_dup_ratio = np.zeros(trials,float)
final_drop_value = np.zeros((trials,trials,1),float)
total_drop_ratio = np.zeros(trials,float)

# Calculate the dup/frame ratio for each trial for all cameras
for index in xrange(1,trials+1):

	# Generate the search pattern
	search_pattern = path_to_dir + string1 + str(index) + string2

	# Get all the log files for the trial
	filenames = glob.glob(search_pattern)

	# Get number of files in the trial
	num_of_files = len(filenames)

	# Get the dup/frame ratio for each camera
	for fn in range(num_of_files):
		
		# Replace the new line character
		os.system("bash ./replace_newline.sh %s" %(filenames[fn]))

		# Read the log file
		logfile = open(filenames[fn], "r")

		# find ip address for lookup
		ip_temp = filenames[fn].split("_")[5]
		ip_addr = ip_temp.split("/")[2]
		
		posn = lookup_table.index(ip_addr)

		# Reset the count
		length = 0
		
		# Find number of lines in the file
		for line in logfile:
			length += 1

		# Read the line which has the required info
		search_line = linecache.getline(filenames[fn],length-LINE_OFFSET)
		
		# Get total frames, duplicate frames and dropped frames
		f_index = search_line.find(match1,0)
		if (f_index == -1):
			frame = 0.0
		else:
			index_end = search_line.find(" ",f_index+len_match1+4)
			frame = float(search_line[f_index+len_match1:index_end])

		dup_index = search_line.find(match2,0)
		if (dup_index == -1):
			dup = 0.0
		else:
			index_end = search_line.find(" ",dup_index+len_match2+1)
			dup = float(search_line[dup_index+len_match2:index_end])

		drop_index = search_line.find(match3,0)
		if (drop_index == -1):
			drop = 0.0
		else:
			index_end = search_line.find(" ",drop_index+len_match3+1)
			drop = float(search_line[drop_index+len_match3:index_end])

		final_dup_value[index-1,posn,0] = dup/frame

		total_dup_ratio[index-1] += dup/frame

		final_drop_value[index-1,posn,0] = drop/frame

		total_drop_ratio[index-1] += drop/frame

# Save the results for plotting
sum_filename = path_to_dir + "total_efps_vs_ncams_" + str(inst_type) + ".txt"
sum_file = open(sum_filename, "w")

for cam in xrange(0,trials):

	# Generate raw file to plot the graph for each camera
	rawfilename = path_to_dir + str(lookup_table[cam]) + "_" + str(inst_type)+"_efps_vs_ncams.txt"

	rawfile = open(rawfilename, "w")

	for trial in xrange(0,trials):

		rawfile.write("%d,%f,%f" %(trial,final_dup_value[trial,cam,0],final_drop_value[trial,cam,0]))
         	rawfile.write("\n")

	rawfile.close()

	# Generate raw file to plot the total dup/frame ratio vs ncams graph
	sum_file.write("%d,%f,%f" %(cam+1,total_dup_ratio[cam],total_drop_ratio[cam]))
	sum_file.write("\n")

sum_file.close()
