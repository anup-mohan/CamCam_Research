####################################################################################################################
# Script to calculate and save the frame rate of all active axis cameras.
# The script needs an input text file containing the list of IP address of all active axis cameras 
# The input file can be obtained by running get_valid_cam.py
####################################################################################################################

import urllib
import sys
import time
import signal
import datetime

ipfilename = "axis_high_ip.txt"
fpsfilename = "fps_" + str(datetime.date.today()) + ".txt"

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


# File containing all the ip addresses
ipfile = open(ipfilename, "r")
# File to save fps for all cameras
fpsfile = open(fpsfilename, "w")

index=0

for ip in ipfile:

	# Remove new line character
	ip_addr = ip.split("\n")[0]

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
		continue
	
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
#        				f = open(name+repr(cnt)+".jpg","wb")
        				#empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
# 	      				f.write(data[2:])
#	      				f.close()
				except (ValueError, IOError, Exception):
					print("Error in IP: %s" %ip)
					error_flag=1
					signal.alarm(0)
					break

        			cnt += 1
	except (ValueError, IOError, Exception):
		print("Error in IP at pt3: %s" %ip)
		error_flag=1

	# Reset the timer
	signal.alarm(0)

	# Get next IP in case of error
	if error_flag:
		error_flag=0
	        if flag_stream_mjpeg:
		        stream_mjpeg.close()
		continue

	# fps = no:of frames/time(seconds)
	fps = cnt/float(STREAM_TIME)
	
	# Write ip and fps to file
	fpsfile.write("%s\t" %ip_addr)
	fpsfile.write("%f" %fps)
	fpsfile.write("\n")

	index += 1

        print("success=%d\n" %index)

	if flag_stream_mjpeg:
		stream_mjpeg.close()

ipfile.close()
fpsfile.close()
