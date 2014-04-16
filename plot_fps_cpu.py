#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys

# File containing all the ip addresses
resfile = open("cam.txt", "r")
fpsfile = open("fps_03_18_2014.txt", "r")

# Array to store x and y axis
num_of_cams = []
cpu_util = []
fps = []
act_fps = []

ip_addr = "128.10.29.20"
for line in fpsfile:
	ip = line.split("\t")[0]
	if ip_addr == ip:
		fps_ip = line.split("\t")[1]
		break

for line in resfile:

	values = line.split(" ")
	num_of_cams.append(values[1])
	fps.append(values[3])
	cpu_util.append(values[5])
	act_fps.append(fps_ip)

# Create the plot
plt.plot(num_of_cams,fps,'ro')
plt.hold(True)
plt.plot(num_of_cams,cpu_util,'g^')
plt.title('Dependence of FPS on CPU Utilization for 128.19.29.20')
plt.xlabel('Num_of_cams')
plt.legend(['FPS','CPU used(%)'])

# Save the figure in a separate file
plt.savefig('fps_cpu_vs_ncams_3_18_2014.png')

plt.close()

cpu_util, fps = zip(*sorted(zip(cpu_util, fps)))

plt.plot(cpu_util,fps,'b^')
plt.title('FPS vs CPU Used for 128.19.29.20')
plt.xlabel('CPU Used(%)')
plt.ylabel('FPS')
plt.hold(True)
plt.plot(cpu_util,act_fps,'r--')
plt.legend(['FPS vs CPU used','Actual FPS'],loc='lower right')

# Save the figure in a separate file
plt.savefig('fps_vs_cpu_3_18_2014.png')

# Draw the plot to the screen
#plt.show()

resfile.close()


