import sys
import numpy as np
import matplotlib.pyplot as plt
import calcAveragePR

dimensions = ["10%","25%","30%","40%","50%","75%","100%"]
#dimensions = ["100%"]

parent_folder = sys.argv[1]
ds = sys.argv[2]

colors = ['0.9','0.75','0.4','0.1']
ht_ranges = ["50", "100", "150", "200", "250", "300", "350"] 
#ht_ranges = ["0-50", "51-100", "101-150", "151-200", "201-250"] 

cnt = 0

# Plot parameters
legend = ["Ground Truth","HoG", "FRCN", "ACF"]
plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()
n_groups = len(ht_ranges)
index = np.arange(1,n_groups+1)
offset = 0.2
#bar_width = (1.-3.*offset)/len(legend)
bar_width = 0.2

# Markers for the miss rate plot
colorP = ['k', 'k', 'k']
marker = ['x', '.' , '+']	

# To find miss rate vs height
total_gt = [0 for x in range(len(ht_ranges))]
total_HoG = [0 for x in range(len(ht_ranges))]
total_FRCN = [0 for x in range(len(ht_ranges))]
total_ACF = [0 for x in range(len(ht_ranges))]

for dim in dimensions:

	# List to store ground truth and measured heights
	gt_ht = []
	HoG_ht = []
	FRCN_ht = []
	ACF_ht = []
	num_ppl_gt_ht_range = [0 for x in range(len(ht_ranges))]
	num_ppl_HoG_ht_range = [0 for x in range(len(ht_ranges))]
	num_ppl_FRCN_ht_range = [0 for x in range(len(ht_ranges))]
	num_ppl_ACF_ht_range = [0 for x in range(len(ht_ranges))]

	# Read the ground truth and measured heights
	gt_htfilename = parent_folder + dim + "/" + "ht_" + dim + ".txt"
	gt_htfile = open(gt_htfilename,"r")
	HoG_htfilename = parent_folder + dim + "/" + "true_ht_" + dim + ".txt"
	HoG_htfile = open(HoG_htfilename,"r")
	FRCN_htfilename = parent_folder + dim + "/" + "true_ht_FRCN_" + ds + "_" + dim + ".txt"
	FRCN_htfile = open(FRCN_htfilename,"r")
	ACF_htfilename = parent_folder + dim + "/" + "true_ht_ACF_" + ds + "_" + dim + ".txt"
	ACF_htfile = open(ACF_htfilename,"r")
	
	# Save the height info as integers in the respective lists
	for line in gt_htfile.readlines():
	
		gt_ht.append(int(line.strip()))
		
	for line in HoG_htfile.readlines():
	
		HoG_ht.append(int(line.strip()))
		
	for line in FRCN_htfile.readlines():
	
		FRCN_ht.append(int(line.strip()))
		
	for line in ACF_htfile.readlines():
	
		ACF_ht.append(int(line.strip()))	
		
	# Group ground truth into ranges
	for ht in gt_ht:
		
		if (0 <= ht <= 50):
			num_ppl_gt_ht_range[0] += 1
		elif(51 <= ht <= 100):
			num_ppl_gt_ht_range[1] += 1
		elif(101 <= ht <= 150):
			num_ppl_gt_ht_range[2] += 1
		elif(151 <= ht <= 200):
			num_ppl_gt_ht_range[3] += 1
		elif(201 <= ht <= 250):
			num_ppl_gt_ht_range[4] += 1
		elif(251 <= ht <= 300):
			num_ppl_gt_ht_range[5] += 1
		elif(301 <= ht <= 350):
			num_ppl_gt_ht_range[6] += 1
	
	if (dim == "100%"):
		print num_ppl_gt_ht_range
		
	# Sum the total ground truth detections across dimensions for miss rate
	total_gt = [x + y for x, y in zip(total_gt, num_ppl_gt_ht_range)]
			
	# Group HoG height into ranges
	for ht in HoG_ht:
		
		if (0 <= ht <= 50):
			num_ppl_HoG_ht_range[0] += 1		
		elif(51 <= ht <= 100):
			num_ppl_HoG_ht_range[1] += 1
		elif(101 <= ht <= 150):
			num_ppl_HoG_ht_range[2] += 1
		elif(151 <= ht <= 200):
			num_ppl_HoG_ht_range[3] += 1
		elif(201 <= ht <= 250):
			num_ppl_HoG_ht_range[4] += 1
		elif(251 <= ht <= 300):
			num_ppl_HoG_ht_range[5] += 1
		elif(301 <= ht <= 350):
			num_ppl_HoG_ht_range[6] += 1
	
	# Sum the total HoG detections across dimensions for miss rate
	total_HoG = [x + y for x, y in zip(total_HoG, num_ppl_HoG_ht_range)]
	
	# Group FRCN height into ranges
	for ht in FRCN_ht:
		
		if (0 <= ht <= 50):
			num_ppl_FRCN_ht_range[0] += 1		
		elif(51 <= ht <= 100):
			num_ppl_FRCN_ht_range[1] += 1
		elif(101 <= ht <= 150):
			num_ppl_FRCN_ht_range[2] += 1
		elif(151 <= ht <= 200):
			num_ppl_FRCN_ht_range[3] += 1
		elif(201 <= ht <= 250):
			num_ppl_FRCN_ht_range[4] += 1
		elif(251 <= ht <= 300):
			num_ppl_FRCN_ht_range[5] += 1
		elif(301 <= ht <= 350):
			num_ppl_FRCN_ht_range[6] += 1
			
	# Adjust for bounding box errors
	for x in range(len(ht_ranges)):
	
		if (num_ppl_FRCN_ht_range[x] > num_ppl_gt_ht_range[x]):
			num_ppl_FRCN_ht_range[x] = num_ppl_gt_ht_range[x]

	# Sum the total FRCN detections across dimensions for miss rate
	total_FRCN = [x + y for x, y in zip(total_FRCN, num_ppl_FRCN_ht_range)]
	
	# Group ACF height into ranges
	for ht in ACF_ht:
		
		if (0 <= ht <= 50):
			num_ppl_ACF_ht_range[0] += 1		
		elif(51 <= ht <= 100):
			num_ppl_ACF_ht_range[1] += 1
		elif(101 <= ht <= 150):
			num_ppl_ACF_ht_range[2] += 1
		elif(151 <= ht <= 200):
			num_ppl_ACF_ht_range[3] += 1
		elif(201 <= ht <= 250):
			num_ppl_ACF_ht_range[4] += 1
		elif(251 <= ht <= 300):
			num_ppl_ACF_ht_range[5] += 1
		elif(301 <= ht <= 350):
			num_ppl_ACF_ht_range[6] += 1
			
	# Adjust for bounding box errors
	for x in range(len(ht_ranges)):
	
		if (num_ppl_ACF_ht_range[x] > num_ppl_gt_ht_range[x]):
			num_ppl_ACF_ht_range[x] = num_ppl_gt_ht_range[x]

	# Sum the total ACF detections across dimensions for miss rate
	total_ACF = [x + y for x, y in zip(total_ACF, num_ppl_ACF_ht_range)]
			
	#print num_ppl_gt_ht_range
	# Draw the height distribution	
	rect1 = plt.bar(index+offset+bar_width, num_ppl_gt_ht_range, bar_width, color=colors[0])
	rect2 = plt.bar(index+offset+(2*bar_width), num_ppl_HoG_ht_range, bar_width, color=colors[1])
	rect3 = plt.bar(index+offset+(3*bar_width), num_ppl_FRCN_ht_range, bar_width, color=colors[2])
	rect4 = plt.bar(index+offset+(4*bar_width), num_ppl_ACF_ht_range, bar_width, color=colors[3])
	
	# Configure the plot
	plt.xlabel('Range of Heights in Pixels',fontsize=34)
	plt.ylabel('Number of Pedestrians \n Detected',fontsize=34)
	plt.tick_params(axis='x',labelsize=24)
	plt.tick_params(axis='y',labelsize=24)
	
	plt.xticks(index + 4*bar_width, ht_ranges) 
			
	plt.legend(legend, loc='upper center',ncol = 2,bbox_to_anchor=(0.5, 1.4))
	plt.ylim((0,250))
	plt.tight_layout()
	#plt.show()

	imgfilename = ds + "_height_dist_"+ dim + ".pdf"

	# Save the plot in a separate file
	plt.savefig(imgfilename,bbox_inches='tight')
	# Close the plot
	plt.close()
	
	gt_htfile.close()
	HoG_htfile.close()
	
# Calculate miss rate Vs height
missRate_HoG = [0.0 for x in range(len(ht_ranges))]
missRate_FRCN = [0.0 for x in range(len(ht_ranges))]
missRate_ACF = [0.0 for x in range(len(ht_ranges))]

dr_HoG = [0.0 for x in range(len(ht_ranges))]
dr_FRCN = [0.0 for x in range(len(ht_ranges))]
dr_ACF = [0.0 for x in range(len(ht_ranges))]

for x in range(len(ht_ranges)):

	tp = float(total_FRCN[x])
	fn = float(total_gt[x] - total_FRCN[x])
	missRate_FRCN[x] = fn/(fn + tp) 
	dr_FRCN[x] = tp/float(tp + fn) * 100
	
	tp = float(total_HoG[x])
	fn = float(total_gt[x] - total_HoG[x])
	missRate_HoG[x] = fn/(fn + tp) 
	dr_HoG[x] = tp/float(tp + fn) * 100
	
	tp = float(total_ACF[x])
	fn = float(total_gt[x] - total_ACF[x])
	missRate_ACF[x] = fn/(fn + tp)
	dr_ACF[x] = tp/float(tp + fn) * 100

index = np.arange(1,len(ht_ranges) - 1)

rect1 = plt.bar(index+offset+bar_width, missRate_HoG[0:5], bar_width, color=colors[1])
rect2 = plt.bar(index+offset+(2*bar_width), missRate_FRCN[0:5], bar_width, color=colors[2])
rect3 = plt.bar(index+offset+(3*bar_width), missRate_ACF[0:5], bar_width, color=colors[3])

'''
rect1 = plt.bar(index+offset+bar_width, missRate_HoG, bar_width, color=colors[1])
rect2 = plt.bar(index+offset+(2*bar_width), missRate_FRCN, bar_width, color=colors[2])
rect3 = plt.bar(index+offset+(3*bar_width), missRate_ACF, bar_width, color=colors[3])
'''

'''
plt.plot(index+offset,missRate_HoG,c=colorP[0],marker=marker[0],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
#plt.plot(index+offset,missRate_HoG[0:5],c=colorP[0],marker=marker[0],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.hold(True)
plt.plot(index+offset,missRate_FRCN,c=colorP[1],marker=marker[1],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
#plt.plot(index+offset,missRate_FRCN[0:5],c=colorP[1],marker=marker[1],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.hold(True)
plt.plot(index+offset,missRate_ACF,c=colorP[2],marker=marker[2],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
#plt.plot(index+offset,missRate_ACF[0:5],c=colorP[2],marker=marker[2],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
'''

plt.xticks(index+3*offset, ht_ranges)
#plt.xticks(index+offset, ht_ranges[0:5])
plt.xlabel('Height in Pixels',fontsize=22)
plt.ylabel('Miss Rate',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend[1:len(legend)], loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
#plt.ylim((0,120))
plt.tight_layout()

imgfilename = "missRate_height_"+ ds + ".pdf"


# Save the plot in a separate file
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()

'''
#plt.plot(index+offset,dr_HoG,c=colorP[0],marker=marker[0],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.plot(index+offset,dr_HoG[0:5],c=colorP[0],marker=marker[0],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.hold(True)
#plt.plot(index+offset,dr_FRCN,c=colorP[1],marker=marker[1],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.plot(index+offset,dr_FRCN[0:5],c=colorP[1],marker=marker[1],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.hold(True)
#plt.plot(index+offset,dr_ACF,c=colorP[2],marker=marker[2],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')
plt.plot(index+offset,dr_ACF[0:5],c=colorP[2],marker=marker[2],markersize=20,markeredgewidth=2,linestyle = 'None',fillstyle='none')

#plt.xticks(index+offset, ht_ranges)
plt.xticks(index+offset, ht_ranges[0:5])
plt.xlabel('Height in Pixels',fontsize=40)
plt.ylabel('Precision (%)',fontsize=40)
plt.tick_params(axis='x',labelsize=28)
plt.tick_params(axis='y',labelsize=28)
plt.legend(legend[1:len(legend)], loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.3))
#plt.ylim((0,120))
plt.tight_layout()

imgfilename = "dr_height_"+ ds + ".pdf"

# Save the plot in a separate file
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()
'''

