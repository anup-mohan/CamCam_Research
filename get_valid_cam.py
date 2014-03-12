####################################################################################################################
# Script to find all valid axis cameras.
# Script will deem a camera to be invalid if it causes a Value Error, IO Error or a Timeout
# The script needs an input text file containing the list of IP address of all axis cameras 
# The input file can be obtained by running get_camera_list.py
####################################################################################################################

import urllib
import sys
import time
import signal
import os

# timeout for single snapshot download
DOWNLOAD_IMAGE_TIMEOUT = 10


def timeout_handler(signum, frame):
	""" This function handles the timeout for downloading an image.
	"""
	raise Exception()


# register the timout handler
signal.signal(signal.SIGALRM, timeout_handler)


# File containing all the ip addresses
ipfile = open("axis_camera_list_all.txt", "r")
# File to save fps for all cameras
fpsfile = open("valid_axis_cams_all.txt", "w")

# Flag to see if stream_mjpeg opened succesfully
flag_stream_mjpeg =0

#number of frames wanted
des_frame = 2

for ip in ipfile:

	# Remove new line character
	ip_addr = ip.split("\n")[0]

	#index for video frame
	cnt = 0
	
	# start the download timer
	signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

	try:
		#the url of the MJPEG stream"
		stream_mjpeg = urllib.urlopen("http://"+ip_addr+"/axis-cgi/mjpg/video.cgi")
		flag_stream_mjpeg =1
	except (ValueError, IOError, Exception):
		print("Error in IP: %s" %ip)
		signal.alarm(0)
		flag_stream_mjpeg =0
		continue

	signal.alarm(0)

	# start the download timer
	signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

	try:
		# Stream data for given no: of frames
		while cnt < des_frame:
			if stream_mjpeg.readline().startswith("--myboundary"):
	     			#the second line is useless
	       			stream_mjpeg.readline()
		
				try:
					#get frame size
					img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
					#read in the empty line and binary image data
					data = stream_mjpeg.read(img_size+2)
				except (ValueError, IOError, Exception):
					print("Error in IP: %s" %ip)
					signal.alarm(0)
					break

				cnt += 1
	except (ValueError, IOError, Exception):
		print("Error in IP: %s" %ip)
		signal.alarm(0)
		continue

	# Reset the timer
	signal.alarm(0)

	# Write ip and fps to file
	fpsfile.write("%s" %ip_addr)
	fpsfile.write("\n")

ipfile.close()
fpsfile.close()

if flag_stream_mjpeg:
	stream_mjpeg.close()

