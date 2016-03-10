# Find the NiMax value given 4 readings of cpu utilization.
# First solve the system of linear equations to obtain the a,b,c coefficients
# Find the Ni value such that UTIL <= 95.0

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

MAX_UTIL = 95.0
DIMENSION = 3
MAX_Ni = 50

def weighted_mov_avg(values):

	# Weights Used
	w1 = 0.1
	w2 = 0.3
	w3 = 0.6
	
	# Predict the next value
	next_val = values[0]*w1 + values[1]*w2 + values[2]*w3
	
	return next_val

def plot_compare(x,num_values,posn,values,dim):

	# Generate x axis values
	xval = []
	for i in range(num_values):
		xval.append(posn[i][0])
	
	#Generate y axis values
	yval = []
	yin = []
	
	# Y values are generate using the polynomial coefficients
	for i in range(num_values):
		val = 0.0
		for j in range(dim):
			val += np.power(xval[i],dim-j-1)*x[j]
		yval.append(val)
		
		yin.append(values[i][0])
	
	# Plot the graph	
	plt.plot(xval,yval,'ro')
	plt.hold(True)
	plt.plot(xval,yin,'g*')
	plt.show()

def plot(x,dim,length):

	# Generate x axis values
	xval = [i for i in xrange(1,length+1)]
	
	#Generate y axis values
	yval = []
	# Y values are generate using the polynomial coefficients
	for i in range(length):
		val = 0.0
		for j in range(dim):
			val += np.power(xval[i],dim-j-1)*x[j]
		yval.append(val)
	
	plt.plot(xval,yval,'ro')
	plt.show()
	
	
def poly_solver(num_values,posn,b,dim):

	# Initialize arrays to solve system of linear equations
	A = np.zeros((num_values,dim),float)
	#b = np.zeros((num_values,1), float)
	x = np.zeros((dim,1), float)
	coef = []

	# Fill the coefficients of A matrix 
	for i in range(num_values):
		for j in range(dim):
			A[i,j] = np.power(posn[i][0],dim-j-1)


	# Solve the matrix equation
	x = np.linalg.lstsq(A,b)
	
	# Convert Matrix to list
	for i in range(dim):
		coef.append(x[0][i])
	
	return coef
	


def error_fun(init_estimate, a,c,posn, value):

	# Length of data
	length = len(values)
	
	# Initialize matrix and list to store result
	#est_val = np.zeros((length,1),float)
	#err_val = []

	# Compute the error value
	calc_val = a * int(posn)**2 + float(init_estimate[0]) * int(posn) + c
	#for j in range(DIMENSION):
		#calc_val += np.power(int(posn),DIMENSION-j-1)*init_estimate[j]
		
	
		
	err_val = float(value) - calc_val
	
	# Convert Matrix to list
	#for i in range(len(est_val)):
		#err_val.append(est_val[i][0])

	return err_val


def get_NiMax(coef,start_value):
	
	NiMax = 0
	
	# Compute the function value
	for i in xrange(start_value,MAX_Ni):
		val = 0.0
		for j in range(DIMENSION):
			val += np.power(i,DIMENSION-j-1)*coef[j]
				
		# If utilization is greater than max value NiMax has reached
		if (val >= MAX_UTIL):
			NiMax = i-1
			break

	return NiMax
	

# Function to calculate the NiMax value
def calc_NiMax(util_file):

	# Read the utilization file
	line = util_file.readlines()
	num_values = len(line)
	
	# Flag to determine is NiMax need to be calculated
	calc_flag = 0
	
	# Fill in the CPU utilization values
	values = np.zeros((num_values,1),float)
	posn = np.zeros((num_values,1),float)
	index = 0 # array index
	
	# Parse the data in util file
	for entry in line:
		# Parse the data in each line
		items = entry.split(" ")
		for i in range(len(items)):
		
			if (items[i] == "num_of_cams:"):
				posn[index] = items[i+1]
				
			if (items[i] == "top_cpu:"):
				values[index] = items[i+1]
		
		# Increment Array index
		index += 1
	
	# Check if NiMax value is already obtained in test phase
	for i in range(len(values)):
		if (values[i][0] >= MAX_UTIL):
			NiMax = int(posn[i-1][0])
			calc_flag = 1
			break 
			
	if (calc_flag == 0):
		
		# Solve the polynomial equation to find coefficients
		coef = poly_solver(num_values,posn,values,DIMENSION) 

		# Find the NiMax value
		NiMax = get_NiMax(coef,1)
		
	# Find the loop increment for prediction purpose
	#loop_inc = int(posn[1][0] - posn[0][0])
	
	plot(coef,3,18)

	return NiMax
	

if __name__ == "__main__":

	# Read the utilization file
	util_file = open(sys.argv[1], "r")
	
	# Calculate the NiMax value
	NiMax = calc_NiMax(util_file)
	
	print NiMax

