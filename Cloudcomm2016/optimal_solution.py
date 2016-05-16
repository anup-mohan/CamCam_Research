import sys

iter_count = 0

# Function to rotate the list
def rotate(l,n):
    return l[-n:] + l[:-n]

# Recursively called function to find the minimum cost
def find_optimal_cost(instances, cost, size, items, N, min_cost, inst_count):

	# To keep track of the number of iterations
	global iter_count	
	iter_count += 1
	rem_cost = 0.0
	rem_inst_count = {'m3.medium':0, 'm3.large':0, 'm3.xlarge':0, 'm3.2xlarge':0}
	sum_items = sum(items)

	# Iterate over all instance types
	for inst in range(len(instances)):

		# For the head of the list, find the required number of instances
		req_num_inst = sum_items/int(size[0])

		# Find remaining cameras
		rem_N = sum_items % int(size[0])

		# If cameras are remaining, use another instance of the same type 	
		if (rem_N > 0):
			req_num_inst += 1
	
		# Iterate over the required number of instances
		for i in xrange(req_num_inst, 0 , -1):
			
			# Compute the remaining cameras
			size_items = sum(items[0:int(N)])
			rem_N = 0
			while (size_items > i * int(size[0])):
				rem_N += 1
				size_items = sum(items[0:int(N)-rem_N])

					
			if (rem_N > 0):
				# Find cost to analyze remaining cameras	
				rem_cost,rem_inst_count = find_optimal_cost(instances[1: len(instances)], cost[1: len(instances)], size[1: len(instances)], items[int(N)-rem_N: int(N)], rem_N, min_cost,inst_count)
				
			# Find total cost
			total_cost = (float(cost[0]) * i) + rem_cost
	
			# Update min_cost if applicable
			if (total_cost < min_cost):			
					min_cost = total_cost
					# Get the number of instances resulting in min_cost
					inst_count = rem_inst_count
					inst_count[instances[0]] = i 
	
		# Rotate the lists
		instances = rotate(instances,-1)
		cost = rotate(cost, -1)
		size = rotate(size, -1)
		
	
	return min_cost, inst_count


if __name__ == '__main__':

	# Initial Values
	instances = ["m3.medium","m3.large","m3.xlarge","m3.2xlarge"]
	cost = [0.067,0.133,0.266,0.532]
	size = [2,5,10,21]
	inst_count = {'m3.medium':0, 'm3.large':0, 'm3.xlarge':0, 'm3.2xlarge':0}
	N = sys.argv[1]
	items = [1 for x in range(int(N))]

	min_cost = 1000000.0
	
	# Find optimal solution
	overall_cost,inst_count = find_optimal_cost(instances, cost, size, items, N, min_cost,inst_count)
	
	print overall_cost
	print inst_count
	print iter_count
