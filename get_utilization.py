##############################################################################################################################
# Script to calculate the dependence of frame rate, cpu/memory/network utilizations on no:of cameras.
# The script will calculate the overall cpu and network utilization for streaming data from different cameras in parallel
# The no: of cameras to be analyzed in parallel is increased in steps of 1 and utilization for each step is noted.
# The utilization of individual cameras are recorded by the script get_utilization_single_cam.py
# The input file should contain the list of valid cameras to be analyzed
# The results would be saved in overall_util_results.txt. 
##############################################################################################################################

import subprocess
import urllib
import sys
import time
import signal

# Input file
ipfile = open("test_769.txt", "r")
line = ipfile.readlines()
length = len(line)

# Output file
resfile = open("overall_util_results.txt", "w")

# To measure overall CPU utilization
command=["./get_total_cpu_util.sh"]


for i in range(length+1):

	# Reset cpu util counters
	count =0
	total_cpu_util = 0

	# Start Network Monitoring
	subprocess.Popen('./start_nw_monitor.sh',shell=True)

	# Wait for vnstat to initialize
	time.sleep(10)

	# Get initial cpu utilization value
	cpu_line = subprocess.Popen(["bash", 'get_total_cpu_util.sh'], stdout=subprocess.PIPE).communicate()[0]
	index = cpu_line.find("id",40)
	if float(cpu_line[index-5:index]) == 0.0:
		init_cpu_util = 0.0
	else:
		init_cpu_util = 100.0 - float(cpu_line[index-5:index])

	# Start streaming from 'i' number of cameras in parallel
	for j in range(i):
		subprocess.Popen(["python", 'get_utilization_single_cam.py',line[j].split("\n")[0],str(i)])
	
	# Print the number of cameras being analyzed
	print ("%d\n" %i)
	
	# Set timeout for synchronization
	timeout = time.time() + 55

	while time.time() < timeout:
		# Measure instantaneous cpu utilization
		cpu_line = subprocess.Popen(["bash", 'get_total_cpu_util.sh'], stdout=subprocess.PIPE).communicate()[0]
		index = cpu_line.find("id",40)
		total_cpu_util += 100.0 - float(cpu_line[index-5:index])
		count += 1
	
	# Get average cpu utilization
	avg_cpu_util = total_cpu_util/float(count)
	
	# Stop Network Monitoring
	subprocess.Popen('./stop_nw_monitor.sh',shell=True)
	# Wait for log file to be written
	time.sleep(5)
	
	# File containing network utilization
	nwfile = open("network_stat.log", "r")

	# Calculate average nw utilization
	for nw_line in nwfile:

		if 'average' in nw_line:
			nw_index = nw_line.find("Mbit/s")
			if (nw_index == -1):
				nw_index = nw_line.find("kbit/s")
				avg_nw_util = nw_line[nw_index-7:nw_index-1]
				break
			elif (nw_index > 0):
				avg_nw_util = nw_line[nw_index-7:nw_index-1]
				break 

	# Close network util file
	nwfile.close()

	# Write the results
	resfile.write("num_of_cams: %d init_cpu: %f avg_cpu: %f avg_nw: %s %s" %(i,init_cpu_util,avg_cpu_util,avg_nw_util,nw_line[nw_index:nw_index+6]))
	resfile.write("\n")

	# Wait before starting next iteration
	time.sleep(5)

# Close input and Output files
ipfile.close()
resfile.close()
