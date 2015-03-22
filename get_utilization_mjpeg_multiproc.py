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
import subprocess
import sys
import time
import signal
import threading
import os
import datetime


# Global variable to keep track of the trial count
trial = 0

# Defining the thread to analyze the camera
class camThread(threading.Thread):
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
                os.system("python /home/anupmohan/Documents/Research/CamCam_Research/CamCam_Research/get_utilization_single_cam.py %s %s" %(self.ip_addr,self.trial))
                #print "Exiting " + self.name

# Define the process to call threads to analyze the camera
def camProcess(start_ptr,end_ptr):

        num_threads = end_ptr - start_ptr
        thread_ptr = [[] for x in range(num_threads+1)]

        # Initialize the list for thread synchronization
        threads = []

        # Start streaming from 'i' number of cameras in parallel
        for j in xrange(start_ptr,end_ptr):

            thr_name = "Thread-" + str(j)
            thread_ptr[j] = camThread(j, thr_name, line[j].split("\n")[0],i)
            thread_ptr[j].start()
            threads.append(thread_ptr[j])

        # Make sure all threads have finished execution
            for k in threads:
                k.join()


NUM_PROCS = cpu_count()
TIMEOUT_VALUE = 60 # time for which utilization is calculated and averaged
DOWNLOAD_IMAGE_TIMEOUT = TIMEOUT_VALUE * 3 # Timeout to detect the crashing of the program



if __name__ == '__main__':

    # Input file
    ipfile = open(sys.argv[1], "r")
    line = ipfile.readlines()
    length = len(line)
    thread_ptr = [[] for x in range(length+1)]

    # Output file
    resfile = open("overall_util_results.txt", "w")

    # To measure overall CPU utilization
    command=["./get_total_cpu_util.sh"]


    for i in range(length+1):

            # Reset cpu util counters
            count =0
            total_cpu_util = 0

            proc_thread_cnt = [0 for x in range(NUM_PROCS)]

            # Initialize the list for process synchronization
            procs = []

            # Start Network Monitoring
            subprocess.Popen('./start_nw_monitor.sh',shell=True)

            # Wait for vnstat to initialize
            time.sleep(10)

            # Get initial cpu utilization value
            cpu_line = subprocess.Popen(["bash", 'get_total_cpu_util.sh'], stdout=subprocess.PIPE).communicate()[0]
            index = cpu_line.find("id",40)
            if float(cpu_line[index-5:index-1]) == 0.0:
                init_cpu_util = 0.0
            else:
                init_cpu_util = 100.0 - float(cpu_line[index-5:index-1])

            # Find num of procs and threads per process
            proc_count = min(NUM_PROCS, i)
            thread_count = int(proc_count/i)
            thread_rem = int(proc_count%i)
            proc_thread_cnt = [thread_count for x in range(NUM_PROCS)]

            # Allocate remaining threads equally among processes
            if(thread_rem != 0):
                k=0
                for j in range(thread_rem):
                    proc_thread_cnt[k]+=1
                    k+=1

            # Start the download timer
            signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

            try:

                # Array to save all processes
                p =[[] for x in range(proc_count)]
                ip_index=0

                # Start the processes
                for j in range(proc_count):

                    p[j] = Process(target=camProcess, args=(ip_index,ip_index+proc_thread_cnt[j],))
                    p[j].start()
                    procs.append(p[j])
                    ip_index += proc_thread_cnt[j]

                # Print the number of cameras being analyzed
                print ("%d\n" %i)

                # Set timeout for synchronization
                timeout = time.time() + 55

                while time.time() < timeout:
                    # Measure instantaneous cpu utilization
                    cpu_line = subprocess.Popen(["bash", 'get_total_cpu_util.sh'], stdout=subprocess.PIPE).communicate()[0]
                    index = cpu_line.find("id",40)
                    total_cpu_util += 100.0 - float(cpu_line[index-5:index-1])
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

