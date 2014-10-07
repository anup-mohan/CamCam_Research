####################################################################################################################
# Calculate and return the instantaneous cpu utilization of the whole system
####################################################################################################################

#!/usr/bin/bash

result=`top -b -n2 | fgrep "Cpu(s)"` # return the instantaneous cpu utilization of the whole system

echo $result
