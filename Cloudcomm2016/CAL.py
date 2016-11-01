import sys
import VSBPP
import time


class result_inst:

	def __init__(self, name, cams, cost):
		self.name = name
		self.cams = cams
		self.cost = cost

# Types of cloud instance used
inst_type = ["m3.medium","m3.large","m3.xlarge","m3.2xlarge"]

# Size array with NiMax value for each type of cloud instance
Nmax = [1,5,12,15]


def find_unassigned_cams(candidate,solution_cams):

	cams = []
	
	# Add cameras not present in the solution to the result
	for item in candidate:
	
		if ( not(item in solution_cams)):
			cams.append(item)
			
	return cams

def find_CAL(locations,cost,candidate,N):

	# List object to save the result
	result_obj = []
	solution_cams = []	

	for loc in range(len(locations)):
	
		# Assign all cameras in candidate list to virginia
		if (loc == 0):
		
			_,typeCost = VSBPP.apply_heuristic_solution(len(candidate[loc]),Nmax,inst_type,cost[loc])			
			result_obj.append(result_inst(locations[loc], candidate[loc], typeCost))
			solution_cams.extend(candidate[loc])
			
		else:
			# Assign only cameras which are not present in the solution
			cams = find_unassigned_cams(candidate[loc],solution_cams)
			_,typeCost = VSBPP.apply_heuristic_solution(len(cams),Nmax,inst_type,cost[loc])
			result_obj.append(result_inst(locations[loc], cams, typeCost))
			solution_cams.extend(cams)
			
				
	return result_obj

if __name__ == '__main__':

	# Total no: of input cameras
	N = 50
	
	# Locations used
	locations = ["virginia", "oregon", "frankfurt", "tokyo"]
	
	# Cost array with the cost of instances to be used in the same order as inst_type array
	cost = [[0.067,0.133,0.266,0.532],[0.067,0.133,0.266,0.532],[0.079,0.158,0.316,0.632],[0.096,0.193,0.385,0.770]]

	# Candidate camera list for each location
	#candidate = [["cam1","cam2","cam3","cam4","cam5","cam6","cam7","cam8"],["cam1","cam2","cam3","cam4","cam5"],["cam1","cam2","cam3","cam4","cam5","cam6","cam7","cam8","cam9","cam10"],["cam4","cam5","cam9","cam10"]]
	
	virginia = [str(x) for x in xrange(29,42)]
	oregon = [str(x) for x in xrange(41,51)]+['6'] 
	frankfurt = [str(x) for x in xrange(1,42)]+ ['47'] 
	tokyo = ['9','10']
	candidate = []
	candidate.append(virginia)
	candidate.append(oregon)
	candidate.append(frankfurt)
	candidate.append(tokyo) 
	
	start_time = time.time()
	# Sort the locations and candidates based on cost
	cost_loc_cand = zip(cost,locations,candidate)
	sorted_list = sorted(cost_loc_cand, key=lambda val: val[0][0])
	locations = [b for a, b, c in sorted_list]
	candidate = [c for a, b, c in sorted_list]
	cost = [a for a, b, c in sorted_list]

	# Find the heuristic solution
	result = find_CAL(locations,cost,candidate,N)
	total_cost = 0.0
	exec_time = time.time() - start_time
	
	for soln in result:
		print soln.name, len(soln.cams), soln.cams, soln.cost
		total_cost += float(soln.cost)
		
	print ("total cost = %f" %total_cost)
	print ("exec time = %s" %(exec_time))
