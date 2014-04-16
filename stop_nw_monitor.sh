####################################################################################################################
# Stop the live network monitoring by sending a CTRL-C to the vnstat process ####################################################################################################################

#!/usr/bin/bash

# Find network monitoring process
pid=`ps -elf | grep "vnstat -l" | grep -v grep | cut -d" " -f4`

if [ "$pid" == "" ]; then
	pid=`ps -elf | grep "vnstat -l" | grep -v grep | cut -d" " -f5`
fi

# Kill the process by sending CTRL-C
/usr/bin/kill -INT $pid

