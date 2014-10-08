#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import datetime

dir_path = "/home/anupmohan/Documents/Research/CamCam_Research/Results"
fpsfilename="fps_2014-04-10.txt"

# File containing all the fps values
fpsfile = open(fpsfilename, "r")
rawfile = open("total_fps_vs_ncams.txt", "w")

nfiles = len([filename for filename in os.listdir(dir_path)])
num_of_files = len(fpsfile.readlines())
fpsfile.close()

# Array to store x and y axis
num_of_cams = [x for x in range(num_of_files+1)]
total_fps = [0.0 for x in range(num_of_files+1)]
obt_fps = [0.0 for x in range(num_of_files+1)]

ncams = 0

for filename in os.listdir(dir_path):

	ip_addr = filename.split(".txt")[0]

	# File containing all the fps values
	fpsfile = open(fpsfilename, "r")	

	for line in fpsfile:

		if ip_addr in line:
			fps = line.split("\t")[1]
			break

	filepath = dir_path + "/" + filename
	ipfile = open(filepath, "r")

	for line in ipfile:
		
		values = line.split(" ")
		ncams = int(values[1])
#	        print ip_addr
#		print ncams
		obt_fps[ncams] = obt_fps[ncams] + float(values[3])
		total_fps[ncams] = total_fps[ncams] + float(fps)
	
	ipfile.close()
	fpsfile.close()

for count in range(1, nfiles):
	 rawfile.write("%s,%s" %(num_of_cams[count],total_fps[count]))
         rawfile.write("\n")


# Create the plot
plt.plot(num_of_cams,total_fps,'ro')
plt.hold(True)
plt.plot(num_of_cams,obt_fps,'g^')
plt.title('Frame rate Vs No: of cameras')
plt.xlabel('Num_of_cams')
plt.ylabel('Frames_Per_Second')
plt.legend(['Ideal FPS','FPS obtained'], loc='upper left')

date=datetime.date.today()
imgfilename="total_fps_vs_ncams_"+ str(date) + ".png"

# Save the figure in a separate file
plt.savefig(imgfilename)

plt.close()

# Draw the plot to the screen
#plt.show()
