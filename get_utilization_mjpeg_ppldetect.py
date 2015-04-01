##############################################################################################################################
# Script to calculate the dependence of frame rate, cpu/memory/network/IO utilizations on no:of cameras.
# The script will calculate the overall cpu and network utilization for streaming data from different cameras in parallel
# The no: of cameras to be analyzed in parallel is increased in steps of 1 and utilization for each step is noted.
# The utilization of individual cameras are recorded using psutil with the Monitor class
# The peopledetect code from OpenCV samples is run on each frame
# The input file should contain the list of valid cameras to be analyzed
# The results would be saved in overall_util_results.txt.
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
import get_mjpeg_ppl_single_cam


# Global variable to keep track of the trial count
trial = 0

# Defining the thread to analyze the camera
class CamThread(threading.Thread):
    def __init__(self, threadID, name, ip_addr, trial):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip_addr = ip_addr
        self.trial = trial
        self.date = datetime.date.today()
        self.filename = "trial_" + str(trial) + "_" + str(self.date)

    def run(self):
        # print "Starting " + self.name
        get_mjpeg_ppl_single_cam.get_MJPEG_stream(self.ip_addr, self.trial)
        # print "Exiting " + self.name


# Define the process to call threads to analyze the camera
def cam_process(start_ptr, end_ptr):
    num_threads = int(end_ptr) - int(start_ptr)
    thread_ptr = [[] for x in range(num_threads + 1)]

    # Initialize the list for thread synchronization
    threads = []

    # Start streaming from 'i' number of cameras in parallel
    for j in range(num_threads):

        thr_name = "Thread-" + str(j)
        thread_ptr[j] = CamThread(j, thr_name, line[int(start_ptr) + j].split("\n")[0], trial)
        thread_ptr[j].start()
        threads.append(thread_ptr[j])

    # Make sure all threads have finished execution
    for k in threads:
        k.join()

# Constants used in the program
NUM_PROCS = cpu_count()
STREAM_TIME = 300 # time for which each camera is streamed
TIME_STOP_MEASUREMENT = STREAM_TIME * 3/5 # time for which utilization is calculated and averaged
DOWNLOAD_IMAGE_TIMEOUT = STREAM_TIME * 3  # Timeout to detect the crashing of the program
SLEEP_TIMEOUT = 60  # Time to wait before starting next iteration
TIME_START_MEASUREMENT = 0  # Start measurement after a minute to avoid initial jitters
LOOP_INCREMENT = 1 # Loop increment value

# Input file
ipfile = open(sys.argv[1], "r")
line = ipfile.readlines()
length = len(line)

if __name__ == '__main__':

    # Output file
    resfile = open("overall_MJPEG_util_results.txt", "w")

    for i in xrange(1, length + 1,LOOP_INCREMENT):

        # Reset cpu util counters
        count = 0
        total_mem_util = 0.0

        # Set the global variable for trial
        trial = i

        proc_thread_cnt = [0 for x in range(NUM_PROCS)]

        # Initialize the list for process synchronization
        procs = []

        # Find num of procs and threads per process
        proc_count = min(NUM_PROCS, i)
        thread_count = int(i / proc_count)
        thread_rem = int(i % proc_count)

        # Allocate threads equally among processes
        for j in range(proc_count):
            proc_thread_cnt[j] = thread_count

        # Allocate remaining threads equally among processes
        if (thread_rem != 0):
            k = 0
            for j in range(thread_rem):
                proc_thread_cnt[k] += 1
                k += 1

        # print proc_thread_cnt
        # print proc_count
        # print thread_count
        # print thread_rem
        # continue

        # Update the timeout value as threads are executed in serial
        # DOWNLOAD_IMAGE_TIMEOUT = TIMEOUT_VALUE * proc_thread_cnt[0] + SLEEP_TIMEOUT

        # Start the download timer
        signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

        try:

            # Array to save all processes
            # p = [[] for x in range(proc_count)]
            ip_index = 0

            # Initialize the processes
            for j in range(proc_count):
                p = Process(target=cam_process, args=(ip_index, ip_index + proc_thread_cnt[j],))
                procs.append(p)
                ip_index += proc_thread_cnt[j]

            # Start all the processes
            for pr in procs:
                pr.start()

            # Print the number of cameras being analyzed
            print ("%d\n" % i)

            # Set timeout for measuring utilization
            timeout = time.time() + TIME_STOP_MEASUREMENT

            # Wait to avoid initial jitters
            time.sleep(TIME_START_MEASUREMENT)

            # Define a monitor object to measure utilization
            util_object = monitor.Monitor()

            while time.time() < timeout:
                # Measure instantaneous memory utilization
                _, _, _, mem_util = monitor.Monitor.get_memory_usage()
                total_mem_util += mem_util
                count += 1

            # Get average utilization values
            avg_cpu_util, avg_disk_consumption, avg_disk_read, avg_disk_write, avg_nw_in, avg_nw_out = \
            monitor.Monitor.get_all_stats(util_object)

            # Make sure all processes have finished execution
            for k in procs:
                k.join()


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

        # Get final cpu utilization value
        avg_cpu_util = float(avg_cpu_util)

        # Get average memory utilization
        avg_mem_util = float(total_mem_util) / float(count)

        # Write the results
        resfile.write("num_of_cams: %d avg_cpu: %f avg_disk_consumption: %s avg_disk_read: %s avg_disk_write: %s \ "
                      "avg_nw_in: %s avg_nw_out: %s avg_mem: %f" % (i, avg_cpu_util, \
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

        # Wait before starting next iteration
        time.sleep(SLEEP_TIMEOUT)

        # Remove the JPG files before the next iteration
        os.system("rm -rf *.jpg")

        # Wait before starting next iteration
        time.sleep(SLEEP_TIMEOUT/6)

    # Close input and Output files
    ipfile.close()
    resfile.close()

