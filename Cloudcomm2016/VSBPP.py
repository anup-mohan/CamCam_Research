# Implement hueristic solution for Variable size bin packing problem.
# Sort the cloud instance array based on cost/NiMax value in non decreasing order
# Find Ki = N/N1Max and add Ki number of cloud instance of type V1 to the solution
# For remaining N find Vi with minimum cost MIN(Ki*Ci)

import sys
import numpy as np

# Denominatore to generate large value on division
INF_DEN = 0.0001

class inst_attr:

	def __init__(self, name, cost, nmax, ratio):
		self.name = name
		self.cost = cost
		self.nmax = nmax
		self.ratio = ratio
		
class result_inst:

	def __init__(self, name, count, ncams):
		self.name = name
		self.count = count
		self.ncams = ncams


def alloc_cams(inst_type,C,Nmax,N):

	# List of objects holding attribute values of all instances used 
	inst_obj = []

	# Add values to objects
	for i in range(len(inst_type)):
		if (Nmax[i] == 0):
			inst_obj.append(inst_attr(inst_type[i],C[i],Nmax[i], C[i]/float(INF_DEN)))
		elif (Nmax[i] > int(N)):		
			inst_obj.append(inst_attr(inst_type[i],C[i],N, C[i]/float(N)))
		else :
			inst_obj.append(inst_attr(inst_type[i],C[i],Nmax[i], C[i]/float(Nmax[i])))

	# Sort the objects based on the Ci/NiMax ratio	
	sorted_inst_obj = sorted(inst_obj, key=lambda inst: inst.ratio)

	# Find Ki, no: of instances needed of the best type
	K1 = int(N)/int(sorted_inst_obj[0].nmax)

	# If the best type of instance can hold more than N
	if (K1 == 0):
		K1 = 1

	# Find the remaining no: of cameras to be assigned
	if (sorted_inst_obj[0].nmax > N):
		rem_N = 0
	else:
		rem_N = int(N)%int(sorted_inst_obj[0].nmax)

	
	return (K1, rem_N,sorted_inst_obj[0].name,sorted_inst_obj[0].cost,sorted_inst_obj[0].nmax)	 
	
def apply_heuristic_solution(N,Nmax,inst_type, C):

	# Initialize remaining camera count
	rem_N = N
	
	# Initialize total cost
	total_cost = 0.0
	
	# List object to save the result
	result_obj = []	
	
	# Allocate instances for all cameras
	while (rem_N > 0):
		
		# Find best instances for given no: of cameras
		K1, rem_N, inst_name, inst_cost, inst_ncams = alloc_cams(inst_type,C,Nmax,rem_N)
	
		# Find the total cost
		total_cost += int(K1) * float(inst_cost)
	
		# Save Result
		result_obj.append(result_inst(inst_name,K1,inst_ncams))


	return result_obj, total_cost


if __name__ == '__main__':

	# Total no: of input cameras
	N = int(sys.argv[1])
	
	# Size array with NiMax value for each type of cloud instance
	Nmax = [1,5,12,15]
	
	# Types of cloud instance used
	inst_type = ["m3.medium","m3.large","m3.xlarge","m3.2xlarge"]

	# Cost array with the cost of instances to be used in the same order as inst_type array
	cost_sel = int(sys.argv[2])
	if (cost_sel == 2):
		C = [0.079,0.158,0.316,0.632]
	else:
		C = [0.067,0.133,0.266,0.532]
	# Find the heuristic solution
	result_obj, total_cost = apply_heuristic_solution(N,Nmax,inst_type,C)
	
	# Print Results
	for item in result_obj:
		print item.name, item.count, item.ncams		
	print total_cost
	


	 


