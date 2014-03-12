####################################################################################################################
# Stop the live network monitoring by sending a CTRL-C to the vnstat process ####################################################################################################################

#!/bin/bash

# Find network monitoring process
pid=`ps -elf | grep "vnstat -l" | grep -v grep | cut -d" " -f8`

if [ "$pid" == "" ]; then
	pid=`ps -elf | grep "vnstat -l" | grep -v grep | cut -d" " -f9`
fi

# Kill the process by sending CTRL-C
kill -INT $pid

