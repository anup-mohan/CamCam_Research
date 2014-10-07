####################################################################################################################
# Calculate and return the average cpu and memory utilization of the given process
####################################################################################################################

#!/usr/bin/bash

pid=$1	# get process id as input

echo `ps -p $pid -o %cpu,%mem` # return the average cpu and memory utilization of the given process
