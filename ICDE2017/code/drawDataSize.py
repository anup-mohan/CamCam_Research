import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Markers for the plot
colors = ['0.75','0.4','0.1']

# Data size as pixel dimensions
dsize = [10, 25, 30, 40, 50, 75, 100]

# Storage cost
#sc = [2.2, 5.5, 6.6, 8.8, 11, 16.5, 22]
sc = [.208, .521, .625, .834, 1.04, 1.56, 2.07]

# Analysis cost for different methods (reverse order) 
cost_HoG_IN = [44.36,29.59,26.60,24.21,22.21,21.28,21.28]
cost_FRCN_IN = [532,532,532,532,532,532,532]
cost_ACF_IN = [19.02,12.21,11.21,10.01,9.31,9.01,8.81]

cost_HoG_IN = cost_HoG_IN[::-1]
cost_FRCN_IN = cost_FRCN_IN[::-1]
cost_ACF_IN = cost_ACF_IN[::-1]

# Analysis cost for different methods
missRate_HoG = [0.77, 0.43, 0.42, 0.38, 0.31, 0.29, 0.23] 
missRate_FRCN = [0.32, 0.14, 0.12, 0.10, 0.09, 0.05, 0.05]
missRate_ACF = [0.58, 0.23, 0.19, 0.12, 0.11, 0.05, 0.05]

# Parameters for the plot
n_groups = len(dsize)
index = np.arange(1,n_groups+1)
offset = 0.2
legend = ["HoG", "FRCN", "ACF"]
bar_width = 0.2
marker = ['x', '.' , '+']
colorP = ['k', 'k', 'k']	

# Draw the sc plot
rect1 = plt.bar(index+offset+bar_width, sc, bar_width, color=colors[0])
rect2 = plt.bar(index+offset+(2*bar_width), sc, bar_width, color=colors[1])
rect3 = plt.bar(index+offset+(3*bar_width), sc, bar_width, color=colors[2])

# Label the axis
plt.xticks(index+3*offset, dsize)
plt.xlabel('Pixel Dimensions (%)',fontsize=22)
plt.ylabel('Storage Cost ($/month)',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
#plt.ylim((0,120))
plt.tight_layout() 	

# Save the plot in a separate file
imgfilename = "dsize_sc_INRIA.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()

# Draw the ac plot
rect1 = plt.bar(index+offset+bar_width, cost_HoG_IN, bar_width, color=colors[0])
rect2 = plt.bar(index+offset+(2*bar_width), cost_FRCN_IN, bar_width, color=colors[1])
rect3 = plt.bar(index+offset+(3*bar_width), cost_ACF_IN, bar_width, color=colors[2])

# Label the axis
plt.xticks(index+3*offset, dsize)
plt.xlabel('Pixel Dimensions (%)',fontsize=22)
plt.ylabel('Analysis Cost ($/hour)',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
#plt.ylim((0,120))
plt.tight_layout() 	

# Save the plot in a separate file
imgfilename = "dsize_ac_INRIA.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()

# Draw the missrate plot
rect1 = plt.bar(index+offset+bar_width, missRate_HoG, bar_width, color=colors[0])
rect2 = plt.bar(index+offset+(2*bar_width), missRate_FRCN, bar_width, color=colors[1])
rect3 = plt.bar(index+offset+(3*bar_width), missRate_ACF, bar_width, color=colors[2])

# Label the axis
plt.xticks(index+3*offset, dsize)
plt.xlabel('Pixel Dimensions (%)',fontsize=22)
plt.ylabel('Miss Rate',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
plt.ylim((0,1.0))
plt.tight_layout() 	

# Save the plot in a separate file
imgfilename = "dsize_mr_INRIA.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()


# Draw the missrate plot for network camera dataset

# miss rate data
missRate_HoG = [1.0, 0.91, 0.86, 0.8, 0.8, 0.72, 0.67] 
missRate_FRCN = [0.58, 0.28, 0.26, 0.26, 0.25, 0.24, 0.24]
missRate_ACF = [0.98, 0.8, 0.78, 0.73, 0.68, 0.54, 0.46]

rect1 = plt.bar(index+offset+bar_width, missRate_HoG, bar_width, color=colors[0])
rect2 = plt.bar(index+offset+(2*bar_width), missRate_FRCN, bar_width, color=colors[1])
rect3 = plt.bar(index+offset+(3*bar_width), missRate_ACF, bar_width, color=colors[2])

# Label the axis
plt.xticks(index+3*offset, dsize)
plt.xlabel('Pixel Dimensions (%)',fontsize=22)
plt.ylabel('Miss Rate',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
plt.ylim((0,1.0))
plt.tight_layout() 	

# Save the plot in a separate file
imgfilename = "dsize_mr_CAM2.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()


# Draw the time vs size for network camera dataset

# time data
time_HoG = [0.02, 0.04, .06, .08, .11, .12, .16] 
time_FRCN = [19.95, 19.96, 19.96, 19.96, 19.96, 19.96, 19.96]
time_ACF = [.017, .024, .034, .039, .047, .049, .068]

rect1 = plt.bar(index+offset+bar_width, time_HoG, bar_width, color=colors[0])
rect2 = plt.bar(index+offset+(2*bar_width), time_FRCN, bar_width, color=colors[1])
rect3 = plt.bar(index+offset+(3*bar_width), time_ACF, bar_width, color=colors[2])

# Label the axis
plt.xticks(index+3*offset, dsize)
plt.xlabel('Pixel Dimensions (%)',fontsize=22)
plt.ylabel('Miss Rate',fontsize=22)
plt.tick_params(axis='x',labelsize=22)
plt.tick_params(axis='y',labelsize=22)
plt.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
#plt.ylim((0,1.0))
plt.tight_layout() 	

# Save the plot in a separate file
imgfilename = "dsize_time.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()


'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(dsize, sc, missRate_HoG, c=colorP[0], marker=marker[0])
ax.scatter(dsize, sc, missRate_FRCN, c=colorP[1], marker=marker[1])
ax.scatter(dsize, sc, missRate_ACF, c=colorP[2], marker=marker[2])

ax.set_xlabel('Pixel Dimensions (%)')
ax.set_ylabel('Storage Cost')
ax.set_zlabel('Miss Rate')
ax.legend(legend, loc='upper center',ncol = 3,bbox_to_anchor=(0.5, 1.2))
# Save the plot in a separate file
imgfilename = "3D_pd_sc_mr.pdf"
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()
'''
