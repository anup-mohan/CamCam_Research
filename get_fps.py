import urllib
import sys
import time

# File containing all the ip addresses
ipfile = open("axis_camera_list.txt", "r")
# File to save fps for all cameras
fpsfile = open("axis_camera_fps.txt", "w")

name="cam1"

for ip in ipfile:

	# Remove new line character
	ip_addr = ip.split("\n")[0]

	#index for video frame
	cnt = 0

	#the url of the MJPEG stream"
	stream_mjpeg = urllib.urlopen("http://"+ip_addr+"/axis-cgi/mjpg/video.cgi")
	
	# Timeout value to be 60 seconds
	timeout = time.time() + 60
	
	# Stream data for 60 seconds
	while time.time() < timeout:
		if stream_mjpeg.readline().startswith("--myboundary"):
     			#the second line is useless
       			stream_mjpeg.readline()
        		#get frame size
        		img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
        		#read in the empty line and binary image data
        		data = stream_mjpeg.read(img_size+2)
#        		f = open(name+repr(cnt)+".jpg","wb")
        		#empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
# 	      		f.write(data[2:])
#	      		f.close()
        		cnt += 1

	# fps = no:of frames/time(seconds)
	fps = cnt/60.0
	
	# Write ip and fps to file
	fpsfile.write("%s\t" %ip_addr)
#	fpsfile.write("\t")
	fpsfile.write("%f" %fps)
	fpsfile.write("\n")

ipfile.close()
fpsfile.close()
