# Implement hueristic solution for Variable size bin packing problem.
# Sort the cloud instance array based on cost/NiMax value in non decreasing order
# Find Ki = N/N1Max and add Ki number of cloud instance of type V1 to the solution
# For remaining N find Vi with minimum cost SUM(Ki*Ci)

import sys
import numpy as np

ATTRIBUTES = 4 # type, cost, Nmax, cost/Nmax

class inst_attr:

	def __init__(self, name, cost, nmax, ratio):
		self.name = name
		self.cost = cost
		self.nmax = nmax
		self.ratio = ratio

# Types of cloud instance used
inst_type = ["m3.2xlarge","m3.xlarge","m3.large","m3.medium"]

# Cost array with the cost of instances to be used in the same order as inst_type array
C = [0.532,0.266,0.133,0.067]

# Size array with NiMax value for each type of cloud instance in the same order as inst_type array
Nmax = [11,6,5,1]

# Total no: of input cameras
N = sys.argv[1]

# List of objects holding attribute values of all instances used 
inst_obj = []

# Add values to objects
for i in range(len(inst_type)):
	inst_obj.append(inst_attr(inst_type[i],C[i],Nmax[i], C[i]/float(Nmax[i])))

# Sort the objects based on the Ci/NiMax ratio	
sorted_inst_obj = sorted(inst_obj, key=lambda inst: inst.ratio)

# Find Ki, no: of instances needed of the best type
K1 = int(N)/int(sorted_inst_obj[0].nmax)

# If the best type of instance can hold more than N
if (K1 == 0):
	K1 = 1

# Find the remaining no: of cameras to be assigned
rem_N = int(N)%int(sorted_inst_obj[0].nmax)
rem_min_cost = 0

# Assign the remaining cameras to instances
if (rem_N > 0):
	
	# First assign the remaining cameras to the best instance type
	K2 = 1
	rem_min_cost = int(K2) * float(sorted_inst_obj[0].cost)
	rem_inst_name = sorted_inst_obj[0].name
	
	# Iterate and check if assigning remaining cameras to any other instance results in a lower cost
	
	for i in xrange(1,len(inst_type)):
	
		# Find no: of instances needed of the next type
		count = int(rem_N)/int(sorted_inst_obj[i].nmax)
		# If there is a remainder increment the count
		rem_count = int(rem_N)%int(sorted_inst_obj[i].nmax)
		if (rem_count > 0):
			count += 1
		# Find the total cost for assigning remaining cameras using this instance type
		cost = count * sorted_inst_obj[i].cost
		
		# If total cost is less than the min cost, update the result values for next iteration
		if (cost < rem_min_cost):
			K2 = count
			rem_min_cost = cost
			rem_inst_name = sorted_inst_obj[i].name	 

# Find the total cost
total_cost = int(K1) * float(sorted_inst_obj[0].cost) + rem_min_cost

#print K1,sorted_inst_obj[0].name, K2, rem_inst_name, total_cost
for i in range(len(inst_type)):
	print sorted_inst_obj[i].name , sorted_inst_obj[i].ratio
 


