# Find the NiMax value given 5 readings of cpu utilization.
# First solve the system of linear equations to obtain the a,b,c coefficients
# Use Levenberg-Marquadt optimization technique to improve the accuracy of the results
# Find the Ni value such that UTIL <= 95.0

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

MAX_UTIL = 95.0
DIMENSION = 3
MAX_Ni = 50

dataset = [1,5,7,2,6,7]

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
	


def error_fun(init_estimate, posn, values):

	# Length of data
	length = len(values)
	
	# Get the Ni values of corresponding input data
	xval = []
	for i in range(num_values):
		xval.append(posn[i][0])
	
	# Initialize matrix and list to store result
	est_val = np.zeros((length,1),float)
	err_val = []

	# Compute the error matrix
	for i in range(length):
		val = 0.0
		for j in range(DIMENSION):
			val += np.power(xval[i],DIMENSION-j-1)*init_estimate[j]
		est_val[i] = values[i] - val
	
	# Convert Matrix to list
	for i in range(len(est_val)):
		err_val.append(est_val[i][0])

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
	


# Fill in the CPU utilization values
num_values = int(sys.argv[1])
values = np.zeros((num_values,1),float)
posn = np.zeros((num_values,1),float)

for i in range(num_values):
	posn[i] = sys.argv[2*i+2]
	values[i] = sys.argv[2*i+3]
	

#print weighted_mov_avg(dataset[0:3])
coef = poly_solver(num_values,posn,values,DIMENSION) 

# Running LM optimization to minimize error
coef_lsq = leastsq(error_fun,coef,args=(posn,values))
print coef
print coef_lsq[0]

# Plot the curve
#plot_compare(coef_lsq[0],num_values,posn,values,DIMENSION)
#plot(coef_lsq[0],DIMENSION,MAX_Ni)

NiMax = get_NiMax(coef_lsq[0],1)

print NiMax

