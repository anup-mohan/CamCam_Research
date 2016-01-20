# Predict NiMax of other instances, given NiMax for an instance
# Initial values of a,b,c coefficients are used as given in paper
# Use Levenberg-Marquadt optimization technique to improve the accuracy of the results
# usage: predict_Nimax.py value num_cores

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

# Compute Nmax value using a,b,c parameters and no: of cores
def compute_nmax(a,b,c,cores):

	return (a * cores**2 + b * cores + c)

# Error function for LM optimization
def error_fun(init_estimate, a, b, c, Nmax_in, cores_in,index):

	# Calculate Nmax with preset a,b,c using ax^2 + bx + c
	if (index == 1):
		calc_nmax = compute_nmax(init_estimate[0],b,c,cores_in)
	elif (index == 2):
		calc_nmax = compute_nmax(a,init_estimate[0],c,cores_in)
	elif (index == 3):
		calc_nmax = compute_nmax(a,b,init_estimate[0],cores_in)
	
	# Compute the error
	err_val = Nmax_in - calc_nmax
	
	return err_val
	
# Minimize error in a,b,or c parameters using LM optimization
def LM_optimize(index,a,b,c,Nmax_in, cores_in):
	
	# Initial estimate for LM optimization
	init_estimate = []
	if (index == 1):
		init_estimate.append(a)
	elif (index == 2):
		init_estimate.append(b)
	elif (index == 3):
		init_estimate.append(c)
		
	# Compute the new value of the coefficient using LM optimization	
	coef_lsq = leastsq(error_fun,init_estimate,args=(a,b,c,Nmax_in, cores_in,index))
	
	return coef_lsq[0][0]
	

	

if __name__ == '__main__':

	# Known value of Nmax
	Nmax_in = int(sys.argv[1])

	# Known value of no: of cores
	cores_in = int(sys.argv[2])

	# Number of cores of instance types used
	num_cores = [1,2,4,8]
	
	# Threshold to select coefficients in the same order as num_cores
	threshold = np.array([1,5,10,15])

	# Preset a,b,c coefficients
	if (Nmax_in > threshold[num_cores.index(cores_in)]):
		a = -0.491
		b = 8.9011
		c = -5.1111
	else:
		a = -0.0421
		b = 1.2016
		c = -0.6111
	
	# Optimize a,b,c parameters
	a_final = a
	b_final = b
	c_final = c
	#a_final = LM_optimize(1,a,b,c,Nmax_in, cores_in)
	b_final = LM_optimize(2,a_final,b,c,Nmax_in, cores_in)
	#c_final = LM_optimize(3,a_final,b_final,c,Nmax_in, cores_in)
	
	# Predict Nmax values for all instance types
	for i in range(len(num_cores)):
		print num_cores[i] , int(compute_nmax(a_final,b_final,c_final,num_cores[i]))
	
	#print a,b,c
	#print a_final,b_final,c_final

