import subprocess
import time


def get_cpu_util():

	
	out,err = subprocess.Popen(["bash", "get_top_cpu_util.sh"],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	cpu_percent = out.split(" ")[1]
	cpu_util = float(cpu_percent.split("%")[0])

	return cpu_util
	


if __name__ == "__main__":

	cpu_util = 0.0

	# Do Processing
	curr_time = time.time()
	while(time.time() < int(curr_time) + int(10)):

		i=0
		cpu_util += get_cpu_util()

	print cpu_util
