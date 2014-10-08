####################################################################################################################################
# Script to calculate the cpu/memory/network utilizations on no:of cameras while streaming videos.
# The script will calculate the overall cpu, memory and network utilization for streaming video from different cameras in parallel
# The no: of cameras to be analyzed in parallel is increased in steps of 3 and utilization for each step is noted.
# The utilization of individual cameras are recorded by the script get_h264_video.sh
# The input file should contain the list of valid cameras to be analyzed
# The results would be saved in overall_video_util_results_$date.txt. 
####################################################################################################################################

import subprocess
import urllib
import sys
import time
import signal
import threading
import os
import datetime


# Defining the thread to analyze the camera
class myThread(threading.Thread):
        def __init__(self, threadID, name, ip_addr, trial):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.ip_addr = ip_addr
                self.trial = trial
		self.date = datetime.date.today()
		self.filename = "trial_"+str(trial)+"_"+str(self.date)
        def run(self):
                #print "Starting " + self.name
                os.system("bash ./get_h264_video_single_cam.sh %s %s" %(self.ip_addr,self.filename))
                #print "Exiting " + self.name


def timeout_handler(signum, frame):
	""" This function handles the timeout for downloading an image.
	"""
	raise Exception()

# register the timout handler
signal.signal(signal.SIGALRM, timeout_handler)

# Constants for the program

SLEEP_TIME = 60 # sleep for 1 minute
NW_WAIT_TIME = 5 # sleep for 5 seconds
TIMEOUT_VALUE = 60 # time for which utilization is calculated and averaged
CPU_UTIL_FIND = 40 # index required to find cpu utilization
CPU_UTIL_OFFSET = 5 # offset required to get the cpu utilization
NW_UTIL_OFFSET = 7 # offset required to get the network utilization
NW_UTIL_PRINT_OFFSET = 6 # offset required to print the network utilization
DOWNLOAD_IMAGE_TIMEOUT = TIMEOUT_VALUE * 3 # Timeout to detect the crashing of the program
FULL_UTIL = 100.0
NO_MATCH = -1


# Input file
ipfile = open(sys.argv[1], "r")
line = ipfile.readlines()
length = len(line)
thread_ptr = [[] for x in range(length+1)]

# Output file
resfile = open("overall_video_util_results.txt", "w")

# To measure overall CPU utilization
command=["./get_total_cpu_util.sh"]


for i in xrange(1,length+1):

	# Reset cpu and mem util counters
	count =0
	total_cpu_util = 0
	mem_used = 0
	swap_used = 0
	
	# Initialize the list for thread synchronization
	threads = []

	# Start Network Monitoring
	subprocess.Popen('./start_nw_monitor.sh',shell=True)

	# Wait for vnstat to initialize
	time.sleep(NW_WAIT_TIME)

	# Get initial cpu utilization value
	cpu_line = subprocess.Popen(["bash", 'get_total_cpu_mem_util.sh'], stdout=subprocess.PIPE).communicate()[0]
	index = cpu_line.find("id",CPU_UTIL_FIND)
	if float(cpu_line[index-CPU_UTIL_OFFSET:index-1]) == 0.0:
		init_cpu_util = 0.0
	else:
		init_cpu_util = FULL_UTIL - float(cpu_line[index-5:index-1])
	
	# Get total available memory
	index = cpu_line.find("Mem",CPU_UTIL_FIND)
	index = index + 10
	index = cpu_line.find("total",index)
	mem_total = float(cpu_line[index-9:index-2])
	index = cpu_line.find("Swap",index)
	index = index + 10
	index = cpu_line.find("total",index)
	swap_total = float(cpu_line[index-9:index-2])	

	# start the download timer
	signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

	try:

		# Start streaming from 'i' number of cameras in parallel
		for j in range(i):
			#subprocess.Popen(["python", 'get_utilization_single_cam.py',line[j].split("\n")[0],str(i)])
			thr_name = "Thread-" + str(j)
		        thread_ptr[j] = myThread(j, thr_name, line[j].split("\n")[0],i)
		        thread_ptr[j].start()
		        threads.append(thread_ptr[j])	
	
		# Print the number of cameras being analyzed
		print ("%d\n" %i)
	
		# Set timeout for synchronization
		timeout = time.time() + TIMEOUT_VALUE

		while time.time() < timeout:
			# Measure instantaneous cpu utilization
			cpu_line = subprocess.Popen(["bash", 'get_total_cpu_mem_util.sh'], stdout=subprocess.PIPE).communicate()[0]
			index = cpu_line.find("id",CPU_UTIL_FIND)
			total_cpu_util += FULL_UTIL - float(cpu_line[index-CPU_UTIL_OFFSET:index-1])
			index = cpu_line.find("used",index)
			mem_used += float(cpu_line[index-9:index-2])
			index = cpu_line.find("Swap",index)
			index = cpu_line.find("used",index)
			swap_used += float(cpu_line[index-9:index-2])
			count += 1

		# Make sure all threads have finished execution
		#for k in threads:
		 #       k.join()
	except (MemoryError):
		print "Exiting the program due to Memory error"
		signal.alarm(0)
		sys.exit(1)
	except (Exception):
		print "Exiting the program due to Timeout"
                signal.alarm(0)
                sys.exit(1)

	# Reset the download timer
	signal.alarm(0)

	# Make sure all threads have finished execution
        for k in threads:
        	k.join()

	# Get average cpu utilization
	avg_cpu_util = total_cpu_util/float(count)

	# Get average memory utilization
	avg_mem_used = mem_used/count
	avg_swap_used = swap_used/count
	avg_mem_util = (avg_mem_used/mem_total)*FULL_UTIL
	avg_swap_util = (avg_swap_used/swap_total)*FULL_UTIL
	
	# Stop Network Monitoring
	subprocess.Popen('./stop_nw_monitor.sh',shell=True)
	# Wait for log file to be written
	time.sleep(NW_WAIT_TIME)
	
	# File containing network utilization
	nwfile = open("network_stat.log", "r")

	# Calculate average nw utilization
	for nw_line in nwfile:

		if 'average' in nw_line:
			nw_index = nw_line.find("Mbit/s")
			if (nw_index == NO_MATCH):
				nw_index = nw_line.find("kbit/s")
				avg_nw_util = nw_line[nw_index-NW_UTIL_OFFSET:nw_index-1]
				break
			elif (nw_index > 0):
				avg_nw_util = nw_line[nw_index-NW_UTIL_OFFSET:nw_index-1]
				break 

	# Close network util file
	nwfile.close()

	# Write the results
	resfile.write("num_of_cams: %d init_cpu: %f avg_cpu: %f avg_nw: %s %s avg_mem: %f avg_swap: %f" %(i,init_cpu_util,avg_cpu_util,avg_nw_util,nw_line[nw_index:nw_index+NW_UTIL_PRINT_OFFSET],avg_mem_util,avg_swap_util))
	resfile.write("\n")

	resfile.flush()
	os.fsync(resfile)

	# Wait before starting next iteration
	time.sleep(SLEEP_TIME)

# Close input and Output files
ipfile.close()
resfile.close()
