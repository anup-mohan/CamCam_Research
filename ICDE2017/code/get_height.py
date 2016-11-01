import sys

infile = open(sys.argv[1],"r")
htfile = open("ht_"+sys.argv[2],"w")
true_htfile = open("true_ht_"+sys.argv[2],"w")

for line in infile.readlines():

	# Get the height data from the result file
	ht = line.split("ht:")[1].split("[")[1].split("]")[0]
	true_ht = line.split("trueht:")[1].split("[")[1].split("]")[0]
	
	# Get individual ground truth heights
	for i in range(len(ht.split(","))):
		tmp = ht.split(",")[i]
		if (tmp):
			htfile.write(tmp)
			htfile.write("\n")
	
	# Get individual true pos heights	
	for j in range(len(true_ht.split(","))):
		tmp = true_ht.split(",")[j]
		if (tmp):
			true_htfile.write(tmp)
			true_htfile.write("\n")

htfile.close()
true_htfile.close()
