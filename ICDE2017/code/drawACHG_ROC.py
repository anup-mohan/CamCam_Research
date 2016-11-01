import sys
import numpy as np
import matplotlib.pyplot as plt
import calcAveragePR
from operator import itemgetter

# Markers for the plot
colorP = ['k', 'c', 'y','m','r','g','b']
marker = ['o', 's' , '+','None','x','None','None']
lstyle = ['solid','dashed','solid','dashed','solid','dashed','dashed']

scores = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

dimensions = ["100%","75%","50%","40%","30%","25%","10%"]
legend = ["10%","25%","30%","40%","50%","75%","100%"]

parent_folder = sys.argv[1]
method = sys.argv[2]
ds = sys.argv[3]

count = 0

#plt.rcParams.update({'font.size': 12})

for dim in dimensions:

	# Read the caffe result files
	tp_infile = open(parent_folder + dim + "/" + "true_positives.csv",'r')
	fp_infile = open(parent_folder + dim + "/" + "false_positives.csv",'r')
	fn_infile = open(parent_folder + dim + "/" + "false_negatives.csv",'r')

	# Read the data
	tp_lines = [line.split(",") for line in tp_infile]
	fp_lines = [line.split(",") for line in fp_infile]
	fn_lines = [line.split(",") for line in fn_infile]

	# Sort the false positives based on the score
	fp_lines.sort(key=itemgetter(5),reverse=True)
	tp_lines.sort(key=itemgetter(5),reverse=True)
	
	fppi = []
	missRate = []
	tpr = []

	for score in reversed(scores):

		countTP = 0.0
		countFP = 0.0
		countFN = 0.0
		countImg = 0.0
		countFN_TP = 0.0
		fn_names = []
		tp_names = []
		all_names=[]
		
		# Find number of false negatives
		for fn_line in fn_lines:
			countFN += float(fn_line[1])
			# Save image names
			fn_names.append(fn_line[0])
		
		# Find the number of false positives
		for fp_line in fp_lines:	
			if (float(fp_line[5]) >= float(score)):
				countFP += 1
				
			elif (float(fp_line[5]) < float(score)):
				break
		
		# Find number of true positives
		for tp_line in tp_lines:
			if (float(tp_line[5]) >= float(score)):
				countTP += 1
			elif (float(tp_line[5]) < float(score)):
				countFN_TP += 1

			# Save image names
			tp_names.append(tp_line[0])
								
		# To find the number of images 
		all_names.extend(tp_names)
		all_names.extend(fn_names)
		countImg = len(set(all_names))
		#print countImg		
		
		# Calculate the false positive per image
		fppi.append(countFP/countImg)
		
		# Calculate the tpr rate
		tpr.append(countTP/(countTP + countFP))
		
		#print score, fppi, missRate, tpr, countFN_TP
		
		
	# Plot the data
	#plt.plot(fppi,missRate,c=colorP[count],marker=marker[count],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
	plt.figure(1)
	plt.plot(fppi,tpr,c=colorP[count],marker=marker[count],markeredgewidth=2,linestyle = lstyle[count],lw=2,fillstyle='none')

	count += 1
	
	tp_infile.close()
	fp_infile.close()
	fn_infile.close()

colorP = ['b','g','r','m','y','c','k']	
marker = ['None', 'None' , 'x','None','+','s','o']
lstyle = ['dashed','dashed','solid','dashed','solid','dashed','solid']
count = 0
	
for dim in legend:

	# Read the caffe result files
	tp_infile = open(parent_folder + dim + "/" + "true_positives.csv",'r')
	fp_infile = open(parent_folder + dim + "/" + "false_positives.csv",'r')
	fn_infile = open(parent_folder + dim + "/" + "false_negatives.csv",'r')

	# Read the data
	tp_lines = [line.split(",") for line in tp_infile]
	fp_lines = [line.split(",") for line in fp_infile]
	fn_lines = [line.split(",") for line in fn_infile]

	# Sort the false positives based on the score
	fp_lines.sort(key=itemgetter(5),reverse=True)
	tp_lines.sort(key=itemgetter(5),reverse=True)
	
	fppi = []
	missRate = []
	tpr = []

	for score in reversed(scores):

		countTP = 0.0
		countFP = 0.0
		countFN = 0.0
		countImg = 0.0
		countFN_TP = 0.0
		fn_names = []
		tp_names = []
		all_names=[]
		
		# Find number of false negatives
		for fn_line in fn_lines:
			countFN += float(fn_line[1])
			# Save image names
			fn_names.append(fn_line[0])
		
		# Find the number of false positives
		for fp_line in fp_lines:	
			if (float(fp_line[5]) >= float(score)):
				countFP += 1
				
			elif (float(fp_line[5]) < float(score)):
				break
		
		# Find number of true positives
		for tp_line in tp_lines:
			if (float(tp_line[5]) >= float(score)):
				countTP += 1
			elif (float(tp_line[5]) < float(score)):
				countFN_TP += 1

			# Save image names
			tp_names.append(tp_line[0])
								
		# To find the number of images 
		all_names.extend(tp_names)
		all_names.extend(fn_names)
		countImg = len(set(all_names))
		#print countImg		
		
		# Calculate the false positive per image
		fppi.append(countFP/countImg)
		
		# Calculate the miss rate
		missRate.append((countFN+ countFN_TP)/(countTP + countFN + countFN_TP))
		
		#print score, fppi, missRate, tpr, countFN_TP
		
		
	# Plot the data
	#plt.plot(fppi,missRate,c=colorP[count],marker=marker[count],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
	plt.figure(2)
	plt.plot(fppi,missRate,c=colorP[count],marker=marker[count],markeredgewidth=2,linestyle = lstyle[count],lw=2,fillstyle='none')

	count += 1
	
	tp_infile.close()
	fp_infile.close()
	fn_infile.close()


plt.figure(1)	
plt.xlabel('false positive per image',fontsize=34)
plt.ylabel('precision',fontsize=34)
plt.tick_params(axis='x',labelsize=24)
plt.tick_params(axis='y',labelsize=24)
plt.ylim(0,1.0)
plt.grid()
plt.legend(dimensions,loc='lower right')
plt.tight_layout()
img_name = method+"_"+ds + "_tprROC.pdf"
plt.savefig(img_name)

	
plt.figure(2)	
plt.xlabel('false positive per image',fontsize=34)
plt.ylabel('miss rate',fontsize=34)
plt.tick_params(axis='x',labelsize=24)
plt.tick_params(axis='y',labelsize=24)
plt.ylim(0,1.0)
plt.grid()
plt.legend(legend,loc='upper right')
plt.tight_layout()
img_name = method+"_"+ds + "_missROC.pdf"
plt.savefig(img_name)



