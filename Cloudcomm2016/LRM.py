# Implement hueristic solution for Location based Resource Management.
# Sort the cloud instance array based on cost/weight value in non decreasing order
# Add the first element to the solution
# Remove assigned cameras and recalculate the weight
# Sort the instances again and repeat these steps till all cameras are assigned

import sys
import numpy as np
import re
import VSBPP
import time

class loc_attr:

	def __init__(self, name, cost, cams, weight, ratio):
		self.name = name
		self.cost = cost
		self.cams = cams
		self.weight = weight
		self.ratio = ratio
		
class result_inst:

	def __init__(self, name, cams, cost):
		self.name = name
		self.cams = cams
		self.cost = cost

# Constant to avoid divide by zero
INF_DEN = 0.00001

# Types of cloud instance used
inst_type = ["m3.medium","m3.large","m3.xlarge","m3.2xlarge"]

# Size array with NiMax value for each type of cloud instance
Nmax = [1,5,12,15]

# Remove assigned cameras from candidate list
def remove_assigned_cams(candidate, cams, index):

	# List to store new candidate cameras
	new_candidate = []
	
	# Delete cameras allocated in the solution from the candidate list
	for elem in candidate:
		
		# Make a copy if the candidate element
		new_elem = [x for x in elem]
		
		# Delete the cameras given in solution
		for item in cams:
			
			# Check if the camera in solution is present in the candidate list
			if (item in elem):
				
				# Remove the camera from the list
				index = new_elem.index(item)
				del new_elem[index]

		# Add the new list of cameras
		if new_elem:		
			new_candidate.append(new_elem)
                else:
			new_candidate.append("e")

		
	return new_candidate

def alloc_cams(locations,cost,candidate):

	# List of objects holding attribute values of all locations used 
	loc_obj = []
	
	# Add values to objects
	for i in range(len(locations)):
		

		if ( len(candidate[i])== 0 or candidate[i] == "e"):
			loc_obj.append(loc_attr(locations[i],cost[i],candidate[i],len(candidate[i]), 1/float(INF_DEN)))
		else :
			_,typeCost = VSBPP.apply_heuristic_solution(len(candidate[i]),Nmax,inst_type,cost[i])
			loc_obj.append(loc_attr(locations[i],typeCost,candidate[i],len(candidate[i]), typeCost/len(candidate[i])))

	# Sort the objects based on the cost/weight ratio	
	sorted_loc_obj = sorted(loc_obj, key=lambda loc: loc.ratio) 
	
	return sorted_loc_obj
	
def apply_heuristic_solution(locations,cost,candidate,N):

	# List object to save the result
	result_obj = []	

	while (N > 0):
	
		# Find the best location
		obj = alloc_cams(locations,cost,candidate)
		# Add the best location and the accessible cameras to the solution
		result_obj.append(result_inst(obj[0].name, obj[0].cams, obj[0].cost))
		
		# Remove the cameras and location in the solution from the input list
		index = locations.index(obj[0].name)
		del locations[index]
		del cost[index]
		candidate = remove_assigned_cams(candidate, obj[0].cams,index)
		N = N - len(obj[0].cams)
		del candidate[index]

	return result_obj		

	

if __name__ == '__main__':

	# Total no: of input cameras
	N = 100
	
	# Locations used
	locations = ["virginia", "oregon", "frankfurt", "tokyo"]
	
	# Cost array with the cost of instances to be used in the same order as inst_type array
	cost = [[0.067,0.133,0.266,0.532],[0.067,0.133,0.266,0.532],[0.079,0.158,0.316,0.632],[0.096,0.193,0.385,0.770]]

	# Candidate camera list for each location
	#candidate = [["cam1","cam2","cam3","cam4","cam5","cam6","cam7","cam8"],["cam1","cam2","cam3","cam4","cam5"],["cam1","cam2","cam3","cam4","cam5","cam6","cam7","cam8","cam9","cam10"],["cam4","cam5","cam9","cam10"]]
	virginia = [str(x) for x in xrange(29,42)] + [str(x) for x in xrange(51,101)]
	oregon = [str(x) for x in xrange(41,80)]+['6'] 
	frankfurt = [str(x) for x in xrange(1,42)]+ ['47','52','59','62','69','71','76','77','78'] + [str(x) for x in xrange(80,101)]
	tokyo = ['7','15','22','23','41','48','49','50']
	candidate = []
	candidate.append(virginia)
	candidate.append(oregon)
	candidate.append(frankfurt)
	candidate.append(tokyo) 

	start_time = time.time()
	# Find the heuristic solution
	result = apply_heuristic_solution(locations,cost,candidate,N)
	total_cost = 0.0
	exec_time = time.time() - start_time
	
	for soln in result:
		print soln.name, len(soln.cams), soln.cams, soln.cost
		total_cost += float(soln.cost)
		
	print ("total cost = %f" %total_cost)
	print ("exec time = %s" %(exec_time))
	
