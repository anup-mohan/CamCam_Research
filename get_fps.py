import urllib
import sys
import time

# File containing all the ip addresses
ipfile = open("valid_axis_cams.txt", "r")
# File to save fps for all cameras
fpsfile = open("axis_camera_fps.txt", "w")


for ip in ipfile:

	# Remove new line character
	ip_addr = ip.split("\n")[0]

	# Reset Error Flag
	error_flag=0

	# Flag to see if stream_mjpeg opened succesfully
	flag_stream_mjpeg =0

	#index for video frame
	cnt = 0

	try:
		#the url of the MJPEG stream"
		stream_mjpeg = urllib.urlopen("http://"+ip_addr+"/axis-cgi/mjpg/video.cgi")
		flag_stream_mjpeg =1
	except (ValueError, IOError, Exception):
		print("Error in IP: %s" %ip)
		flag_stream_mjpeg =0
		continue
	
	# Timeout value to be 60 seconds
	timeout = time.time() + 60
	
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
#        		f = open(name+repr(cnt)+".jpg","wb")
        		#empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
# 	      		f.write(data[2:])
#	      		f.close()
			except (ValueError, IOError, Exception):
				print("Error in IP: %s" %ip)
				error_flag=1
				break

        		cnt += 1

	# Get next IP in case of error
	if error_flag:
		error_flag=0
		continue

	# fps = no:of frames/time(seconds)
	fps = cnt/60.0
	
	# Write ip and fps to file
	fpsfile.write("%s\t" %ip_addr)
	fpsfile.write("%f" %fps)
	fpsfile.write("\n")

	if flag_stream_mjpeg:
		stream_mjpeg.close()

ipfile.close()
fpsfile.close()
