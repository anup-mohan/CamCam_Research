import sys
import VSBPP
import time

# Types of cloud instance used
inst_type = ["m3.medium","m3.large","m3.xlarge","m3.2xlarge"]

# Size array with NiMax value for each type of cloud instance
Nmax = [1,5,12,15]

# Global variable for total number of cameras
total_cams = 100

# Remove assigned cameras from candidate list
def remove_assigned_cams(candidate, cams,cam_rem_index,locations,cost):
	#print "inside rem", candidate, cams, locations, cam_rem_index
	# List to store new candidate cameras
	new_candidate = []
	# Position variable to delete the location and cost corresponding to empty candidate
	posn = 0
	# Position variable to skip the camera corresponding to cam_rem_index
	count = 0
	
	# Delete cameras allocated in the solution from the candidate list
	for elem in candidate:

		if elem:
		
			# Make a copy of the candidate element
			new_elem = [x for x in elem]
			
			# Delete the cameras given in solution
			for item in cams:
				
				# Skip the camera in the cam_index position
				if (not(count in cam_rem_index)):
					# Check if the camera in solution is present in the candidate list
					if (item in elem):
					
						# Remove the camera from the list
						index = new_elem.index(item)
						del new_elem[index]
				
				count += 1

			# Add the new list of cameras
			if new_elem:		
				new_candidate.append(new_elem)
				posn += 1
			else:
				#print "inside rem", posn
				del(locations[posn])
				del(cost[posn])

	#print "rem out:",new_candidate,locations		
	return new_candidate,locations,cost

def find_exclusive_cams(loc,candidate):
	#print "inside ex", loc, candidate
	# Count of exclusive cameras
	count = 0
	
	# Cameras being searched
	search_cams = candidate[loc]
	
	# Array to keep track of match count
	match_cams = [0 for x in range(len(search_cams))]
	#print ("length = %d" %len(match_cams))	
	# Find exclusive cameras
	for i in range(len(candidate)):
	
		# Avoid the same location
		if ( i != loc):
			
			# Compare with candidate cameras of all other locations
			for cam in candidate[i]:
			
				# Compare all the cameras being searched
				for j in range(len(search_cams)):
					
					# Increment count if a match is found
					if (cam == search_cams[j]):
						
						match_cams[j] += 1
	
	# Cameras are exclusive if their match count is zero
	for i in range(len(match_cams)):
		
		if (match_cams[i] == 0):
			
			count += 1
	#print "match_cams", match_cams	
	return count, match_cams

def find_optimal_cost(locations, cost, candidate, N, min_cost,loc_count,total_min_cost,final_loc_count):

	if (len(locations) > 0 and len(candidate) > 0):
	
		for loc in range(len(locations)):
			#print "start", loc, locations, candidate		
			# Assign all candidate cameras to the first location
			#print "outer:",locations[loc]
			assigned_cameras = len(candidate[loc])
			
			# Create a copy of candidate list
			candidate_copy = candidate[:]
			locations_copy = locations[:]
			cost_copy = cost[:]
			
			if (assigned_cameras > 0):
			
				# Find exclusive and overlapping cameras
				min_cameras, match_cams = find_exclusive_cams(loc,candidate_copy)				
				cam_rem_index = [-1 for x in range(len(match_cams))]
				
				#print "before for", min_cameras,match_cams,locations
				for cams in xrange(assigned_cameras, min_cameras-1, -1):
					#print "inside for",cams, min_cameras,match_cams
					#print candidate_copy,locations
					#print "inner:", cams, locations[loc], match_cams, min_cameras
					# Find the cost of assigning the given cameras to the current location
					_,curr_cost = VSBPP.apply_heuristic_solution(cams,Nmax,inst_type,cost_copy[loc])

					# Cameras to be assigned
					rem_cameras = N - cams
					
					# Initialize the cost for assigning rem cameras
					rem_cost = 0
					rem_loc_count = {'virginia':0, 'oregon':0, 'frankfurt':0, 'tokyo':0}
					
					if (rem_cameras > 0):
						
						# Remove assigned cameras and location and calculate cost
						tmp_locations = locations_copy[:]
						tmp_candidate = candidate_copy[:]
						tmp_cost = cost_copy[:]
						del(tmp_locations[loc])
						del(tmp_candidate[loc])
						del(tmp_cost[loc])
						
						# Remove assigned cameras from the candidate list
						tmp_candidate,tmp_locations,tmp_cost = remove_assigned_cams(tmp_candidate, candidate_copy[loc], cam_rem_index, tmp_locations,tmp_cost)
						
						# Find remaining cost				
						rem_cost,rem_loc_count,total_min_cost,_ = find_optimal_cost(tmp_locations, tmp_cost, tmp_candidate, rem_cameras, min_cost,loc_count,total_min_cost,final_loc_count)
						
					# Find total cost
					total_cost = curr_cost + rem_cost
					
					# Update min_cost if applicable
					if (total_cost < min_cost):	
					
						# Get the assignment resulting in min_cost
						loc_count = rem_loc_count.copy()
						#print loc_count
						loc_count[locations[loc]] = cams
						min_cost = total_cost

						if (sum(loc_count.values()) == total_cams):	
							total_min_cost = total_cost
							final_loc_count = loc_count.copy()
							#print "inside opt:", final_loc_count, total_min_cost
					
					#print "inside opt1:", loc_count,rem_loc_count,curr_cost, rem_cost, total_cost, total_min_cost	
					# Assign a non-exclusive camera to another location
					for k in range(len(match_cams)):
						#print "inside match",candidate_copy, match_cams,loc,k
						if (match_cams[k] > 0):
							cam_rem_index[k] = k
							match_cams[k] = -1
							#print cam_rem_index, match_cams
							break
					
					#if (cams == 5):
					#	sys.exit(1)
					#print locations[loc], cams 
				
				'''			
				if (assigned_cameras == min_cameras):
				
					_,curr_cost = VSBPP.apply_heuristic_solution(assigned_cameras,Nmax,inst_type,cost[loc])
									
					# Find total cost
					total_cost = curr_cost
					
					# Update min_cost if applicable
					if (total_cost < min_cost):	
					
						min_cost = total_cost
						# Get the assignment resulting in min_cost
						loc_count[locations[loc]] = assigned_cameras
						
						if (sum(loc_count.values()) == total_cams):	
							total_min_cost = total_cost
							final_loc_count = loc_count.copy()
					
					print "inside opt2:", loc_count,curr_cost, total_cost, total_min_cost
				'''	
						
	return min_cost, loc_count, total_min_cost, final_loc_count
					
if __name__ == '__main__':

	#Total no: of input cameras
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
	
	# Initial value for minimum cost
	min_cost = 1000000.0
	total_min_cost = 1000000.0
	
	# Format of solution, location:number of cameras
	loc_count = {'virginia':0, 'oregon':0, 'frankfurt':0, 'tokyo':0}
	final_loc_count = {'virginia':0, 'oregon':0, 'frankfurt':0, 'tokyo':0}

	start_time = time.time()
	# Find optimal solution
	min_cost,loc_count,overall_cost,final_loc_count = find_optimal_cost(locations, cost, candidate, N, min_cost,loc_count,total_min_cost,final_loc_count)
	exec_time = time.time() - start_time

	print final_loc_count
	print overall_cost
	print ("exec time = %s" %(exec_time))
