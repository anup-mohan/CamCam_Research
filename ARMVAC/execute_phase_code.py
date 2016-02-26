##############################################################################################################################
# Script to calculate the dependence of frame rate, cpu/memory/network/IO utilizations on no:of cameras.
# The script will calculate the overall cpu and network utilization for streaming data from different cameras in parallel
# The no: of cameras to be analyzed in parallel is increased in steps of 1 and utilization for each step is noted.
# The utilization of individual cameras are recorded using psutil with the Monitor class
# The input file should contain the list of valid cameras to be analyzed
# The utilization results would be saved in the file name specified
# The frame rate information would be present in the text file having the same name as camera ip address
# Usage: python get_utilization_mjpeg_me.py module_fname ip_fname out_fname fps num_cams stream_time total_analysis_time 
##############################################################################################################################

from multiprocessing import Process
from multiprocessing import cpu_count
import sys
import os
import time
import signal
import threading
import datetime
import monitor
import get_mjpeg_sift_single_cam
import top_cpu_util
import importlib

# Threshold for CPU Utilization
CPU_THRESHOLD = 99.0

# Defining the thread to analyze the camera
class CamThread(threading.Thread):
    def __init__(self, threadID, name, ip_addr, analysis_mod, trial, des_fps,fps_method,STREAM_TIME):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip_addr = ip_addr
        self.trial = trial
        self.date = datetime.date.today()
        self.filename = "trial_" + str(trial) + "_" + str(self.date)
        self.fps = des_fps
        self.method = fps_method
        self.time = STREAM_TIME

    def run(self):
        # print "Starting " + self.name
        analysis_mod.get_MJPEG_stream(self.ip_addr, self.trial, self.fps, self.method, self.time)
        # print "Exiting " + self.name


# Define the process to call threads to analyze the camera
def cam_process(analysis_mod,start_ptr, end_ptr, line, trial,des_fps,fps_method,STREAM_TIME):
    num_threads = int(end_ptr) - int(start_ptr)
    thread_ptr = [[] for x in range(num_threads + 1)]

    # Initialize the list for thread synchronization
    threads = []

    # Start streaming from 'i' number of cameras in parallel
    for j in range(num_threads):

        thr_name = "Thread-" + str(j)
        thread_ptr[j] = CamThread(j, thr_name, line[int(start_ptr) + j].split("\n")[0], analysis_mod,trial,des_fps,fps_method,STREAM_TIME)
        thread_ptr[j].start()
        threads.append(thread_ptr[j])

    # Make sure all threads have finished execution
    for k in threads:
        k.join()



# Routine to stream and analyze data from cameras
def run_analysis_on_cameras(analysis_mod,ipfilename,resfilename,des_fps,num_cams,STREAM_TIME,TOTAL_TIME):

	# Read input ip address file 
	ipfile = open(ipfilename, "r")
	line = ipfile.readlines()
	length = len(line)

	# Output file for writing results
	resfile = open(resfilename, "w")

	# Constants used in the program
	NUM_PROCS = cpu_count()
	TIME_STOP_MEASUREMENT = int(STREAM_TIME) * 3/5 # time for which utilization is calculated and averaged
	DOWNLOAD_IMAGE_TIMEOUT = int(STREAM_TIME) * 3  # Timeout to detect the crashing of the program
	SLEEP_TIMEOUT = 60  # Time to wait before starting next iteration
	TIME_START_MEASUREMENT = 0  # Start measurement after a minute to avoid initial jitters
        fps_method = 0 # 0: Ensure frame rate using delay, 1: Ensure frame tate using command
	trial = 0 # keep track of number of times analysis is done

	# Get the current time
	curr_time = time.time()

	# Stream and analyze for the given duration
	while (time.time() < curr_time + int(TOTAL_TIME)):
		
		# Reset cpu util counters
		count = 0
		total_mem_util = 0.0

		# Set the trial number
		trial += 1 

		proc_thread_cnt = [0 for x in range(NUM_PROCS)]

		# Initialize the list for process synchronization
		procs = []

		# Find num of procs and threads per process
		proc_count = min(NUM_PROCS, num_cams)
		thread_count = int(num_cams / proc_count)
		thread_rem = int(num_cams % proc_count)

		# Allocate threads equally among processes
		for j in range(proc_count):
			proc_thread_cnt[j] = thread_count

		# Allocate remaining threads equally among processes
		if (thread_rem != 0):
			k = 0
			for j in range(thread_rem):
				proc_thread_cnt[k] += 1
				k += 1

		ip_index = 0

		# Initialize the processes
		for j in range(proc_count):
			p = Process(target=cam_process, args=(analysis_mod, ip_index, ip_index + proc_thread_cnt[j],line,trial,des_fps,fps_method,STREAM_TIME))
			procs.append(p)
			ip_index += proc_thread_cnt[j]

		# Start all the processes
		for pr in procs:
			pr.start()

		# Set timeout for measuring utilization
		timeout = time.time() + TIME_STOP_MEASUREMENT

		# Wait to avoid initial jitters
		time.sleep(TIME_START_MEASUREMENT)

		# Define a monitor object to measure utilization
		util_object = monitor.Monitor()

		# Intialize counter to measure CPU utilization
		avg_top_cpu_util = 0.0

		while time.time() < timeout:
			# Measure instantaneous memory utilization
			_, _, _, mem_util = monitor.Monitor.get_memory_usage()
			total_mem_util += mem_util
			avg_top_cpu_util += top_cpu_util.get_cpu_util()
			count += 1

		# Get average utilization values
		#avg_cpu_util, avg_disk_consumption, avg_disk_read, avg_disk_write, avg_nw_in, avg_nw_out = \
		stats = util_object.get_all_stats()
		avg_cpu_util = stats.cpu_percent
		avg_disk_consumption = stats.disk_consumption
		avg_disk_read = stats.read_rate
		avg_disk_write = stats.write_rate
		avg_nw_in = stats.in_rate
		avg_nw_out = stats.out_rate


		# Make sure all processes have finished execution
		for k in procs:
			k.join()

		# Print the number of cameras being analyzed
		print ("No: cameras: %d\n" % num_cams)

		# Get final cpu utilization value
		avg_cpu_util = float(avg_cpu_util)

		# Get average memory utilization
		avg_mem_util = float(total_mem_util) / float(count)
		avg_top_cpu_util = float(avg_top_cpu_util) / float(count)

		# Increment the data point counter if cpu util is non zero
		if (avg_top_cpu_util > 0.0):
			num_data_points += 1

		# Write the results
		resfile.write("num_of_cams: %d avg_cpu: %f top_cpu: %f avg_disk_consumption: %s avg_disk_read: %s avg_disk_write: %s \ "
				      "avg_nw_in: %s avg_nw_out: %s avg_mem: %f" % (i, avg_cpu_util, avg_top_cpu_util, \
				                                                    avg_disk_consumption, \
				                                                    avg_disk_read, \
				                                                    avg_disk_write, \
				                                                    avg_nw_in, avg_nw_out, avg_mem_util))
		resfile.write("\n")

		# Flush the data to the result file
		resfile.flush()
		os.fsync(resfile)

		# Remove the utilization object
		del util_object

		# Exit if enough data points are obtained
		if (avg_top_cpu_util > CPU_THRESHOLD):
			break

		# Wait before starting next iteration
		time.sleep(SLEEP_TIMEOUT)

		# Remove the JPG files before the next iteration
		#os.system("find . -maxdepth 1 -name 'feat_*.txt' -print0 | xargs -0 rm")


    # Close input and Output files
	ipfile.close()
	resfile.close()
	
	

if __name__ == '__main__':

	# Analysis module
	mod_file_name = sys.argv[1]
	mod_name = mod_file_name.split(".")[0]
	analysis_mod = importlib.import_module(mod_name)

	# Input file name
	ipfilename = sys.argv[2]

	# Output file name
	resfilename = sys.argv[3]

	# Desired Frame Rate (Global Variable)
	des_fps = sys.argv[4]

	# Number of cameras to be analyzed in the instance
	num_cams = int(sys.argv[5])

	# Time for which each camera is streamed
	STREAM_TIME = sys.argv[6]

	# Total analysis time
	TOTAL_TIME = sys.argv[7]

	# Run the analysis on cameras
	run_analysis_on_cameras(analysis_mod,ipfilename,resfilename,des_fps,num_cams,STREAM_TIME,TOTAL_TIME)

    

