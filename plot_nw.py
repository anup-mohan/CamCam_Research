#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime

# File containing all the ip addresses
resfile = open("result.txt", "r")
resfile.readline()

# Array to store x and y axis
num_of_cams = []
nw_util = []

for line in resfile:

	nw_index = line.find("Mbit/s")
	if nw_index == -1:
		continue

        nwutil = line[nw_index-7:nw_index-1]
	nwvar=nwutil.split(" ")[0]
	if nwvar == "":
		nwvar=nwutil.split(" ")[1]
		if nwvar == "":
			nwvar=nwutil.split(" ")[2]
	nw_util.append(nwvar)
	ncams = line.split(" ")[1]
	num_of_cams.append(ncams)

# Create the plot
plt.plot(num_of_cams,nw_util)
plt.title('N/W Utilization vs Num_of_Cams')
plt.xlabel('Num_of_cams')
plt.ylabel('N/W Utilization(Mbits/s)')

date=datetime.date.today()
imgfilename="nw_vs_ncams_"+ str(date) + ".png"

# Save the figure in a separate file
plt.savefig(imgfilename)

# Draw the plot to the screen
#plt.show()

resfile.close()

