########################################################################################################################
# Script to calculate and save the frame rate, CPU and Memory utilization of a given camera.
# The streams from the camera will be analyzed for a minute and average fps and cpu/mem utilization will be computed
# The script will call the bash script get_cpu_mem_util.sh to calculate the cpu/mem utilization
# The results would be saved in "ip_address_of_camera".txt file
# Change the path of the result file according to the system being used
########################################################################################################################

import urllib
import sys
import time
import subprocess
import os
import signal

# Timeout for single image
DOWNLOAD_IMAGE_TIMEOUT = 10

# Timeout for a minute of download
DOWNLOAD_IMAGE_TIMEOUT2 = 70

# Duration of stream
STREAM_TIME = 60

def timeout_handler(signum, frame):
        """ This function handles the timeout for downloading an image.
        """
        raise Exception()


# register the timout handler
signal.signal(signal.SIGALRM, timeout_handler)


# To measure CPU and Memory utilization
command=["./get_cpu_mem_util.sh"]
proc_id=[str(os.getpid())]
command.extend(proc_id)
cpu_util = 0.0
mem_util = 0.0

# Get IP of the camera
ip_addr = sys.argv[1]
# Get trial number
trial = sys.argv[2]

# File to save the results
path_to_file = "/home/anupmohan/Documents/Research/camcam/Results/"
filename = path_to_file+ip_addr+".txt"
resfile = open(filename, "a")

# Reset Error Flag
error_flag=0

# Flag to see if stream_mjpeg opened succesfully
flag_stream_mjpeg =0

#index for video frame
cnt = 0

# Start the download timer
signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

try:
	#the url of the MJPEG stream"
	stream_mjpeg = urllib.urlopen("http://"+ip_addr+"/axis-cgi/mjpg/video.cgi")
	flag_stream_mjpeg =1
except (ValueError, IOError, Exception):
	print("Error in IP: %s" %ip)
	flag_stream_mjpeg =0
	signal.alarm(0)

	
# Reset the timer
signal.alarm(0)
	
# Timeout value to be 60 seconds
timeout = time.time() + STREAM_TIME

# Start the download timer
signal.alarm(DOWNLOAD_IMAGE_TIMEOUT2)

try:
	# Stream data for 60 seconds
	while time.time() < timeout:
		if stream_mjpeg.readline().startswith("--myboundary"):
			#the second line is useless
			stream_mjpeg.readline()

			try:
				#get frame size
	       			img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
	       			#read in the empty line and binary image data
	       			data = stream_mjpeg.read(img_size+2)
				# Measure CPU/Mem utilization
				output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
				cpu_util += float(output.split(" ")[2])
				mem_util += float(output.split(" ")[3])
	#        		f = open(name+repr(cnt)+".jpg","wb")
				#empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
	# 	      		f.write(data[2:])
	#	      		f.close()
			except (ValueError, IOError, Exception):
				print("Error in IP: %s" %ip)
				error_flag=1
				break

	       		cnt += 1

except (ValueError, IOError, Exception):
	print("Error in IP at pt3: %s" %ip)
	error_flag=1

# Reset the timer
signal.alarm(0)

if error_flag == 0:
	# fps = no:of frames/time(seconds)
	fps = cnt/float(STREAM_TIME)

	# Average CPU/Mem utilization
	cpu_util = cpu_util/cnt	
	mem_util = mem_util/cnt	

	# Return fps, cpu and memory utilization
	#print("fps: %f cpu_util: %f mem_util: %f" %(fps,cpu_util,mem_util))
	resfile.write("trial:%s fps:%f cpu:%f mem:%f" %(trial,fps,cpu_util,mem_util))
	resfile.write("\n")

if flag_stream_mjpeg:
	stream_mjpeg.close()

resfile.close()
