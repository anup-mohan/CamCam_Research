##############################################################################################################################
# Script to calculate the dependence of frame rate, cpu/memory/network utilizations on no:of cameras.
# The script will calculate the overall cpu and network utilization for streaming data from different cameras in parallel
# The no: of cameras to be analyzed in parallel is increased in steps of 1 and utilization for each step is noted.
# The utilization of individual cameras are recorded by the script get_utilization_single_cam.py
# The input file should contain the list of valid cameras to be analyzed
# The results would be saved in overall_util_results.txt. 
##############################################################################################################################

from multiprocessing import Process
from multiprocessing import cpu_count
import sys
import time
import signal
import threading
import datetime
import monitor
import get_mjpeg_single_cam


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
        get_mjpeg_single_cam.get_MJPEG_stream(self.ip_addr,self.trial)
        # print "Exiting " + self.name


# Define the process to call threads to analyze the camera
def cam_process(start_ptr, end_ptr):
    num_threads = end_ptr - start_ptr
    thread_ptr = [[] for x in range(num_threads + 1)]

    # Initialize the list for thread synchronization
    threads = []

    # Start streaming from 'i' number of cameras in parallel
    for j in xrange(start_ptr, end_ptr):

        thr_name = "Thread-" + str(j)
        thread_ptr[j] = CamThread(j, thr_name, line[j].split("\n")[0], i)
        thread_ptr[j].start()
        threads.append(thread_ptr[j])

        # Make sure all threads have finished execution
        for k in threads:
            k.join()


NUM_PROCS = cpu_count()
TIMEOUT_VALUE = 60  # time for which utilization is calculated and averaged
DOWNLOAD_IMAGE_TIMEOUT = TIMEOUT_VALUE * 3  # Timeout to detect the crashing of the program
SLEEP_TIMEOUT = 5 # Time to wait before starting next iteration

if __name__ == '__main__':

    # Input file
    ipfile = open(sys.argv[1], "r")
    line = ipfile.readlines()
    length = len(line)
    thread_ptr = [[] for x in range(length + 1)]

    # Output file
    resfile = open("overall_MJPEG_util_results.txt", "w")

    for i in xrange(1,length + 1):

        # Reset cpu util counters
        count = 0
        total_mem_util = 0.0

        proc_thread_cnt = [0 for x in range(NUM_PROCS)]

        # Initialize the list for process synchronization
        procs = []

        # Find num of procs and threads per process
        proc_count = min(NUM_PROCS, i)
        thread_count = int(proc_count / i)
        thread_rem = int(proc_count % i)
        proc_thread_cnt = [thread_count for x in range(NUM_PROCS)]

        # Allocate remaining threads equally among processes
        if (thread_rem != 0):
            k = 0
            for j in range(thread_rem):
                proc_thread_cnt[k] += 1
                k += 1

        # Start the download timer
        signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

        try:

            # Array to save all processes
            p = [[] for x in range(proc_count)]
            ip_index = 0

            # Start the processes
            for j in range(proc_count):
                p[j] = Process(target=cam_process, args=(ip_index, ip_index + proc_thread_cnt[j],))
                p[j].start()
                procs.append(p[j])
                ip_index += proc_thread_cnt[j]

            # Print the number of cameras being analyzed
            print ("%d\n" % i)

            # Set timeout for synchronization
            timeout = time.time() + TIMEOUT_VALUE

            # Define a monitor object to measure utilization
            util_object = monitor.Monitor()

            while time.time() < timeout:
                # Measure instantaneous memory utilization
                _, _, _, mem_util = monitor.Monitor.get_memory_usage()
                total_mem_util += mem_util
                count += 1

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

        # Make sure all processes have finished execution
        for k in procs:
            k.join()

        # Get average utilization values
        avg_cpu_util, avg_disk_consumption, avg_disk_read, avg_disk_write, avg_nw_in, avg_nw_out = \
            monitor.Monitor.get_all_stats(util_object)

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

        # Remove the utilization object
        del util_object

        # Wait before starting next iteration
        time.sleep(SLEEP_TIMEOUT)

    # Close input and Output files
    ipfile.close()
    resfile.close()

