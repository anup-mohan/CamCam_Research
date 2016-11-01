import sys
import numpy as np
import matplotlib.pyplot as plt


# Markers for the miss rate plot
colors = ['Aquamarine','MidnightBlue']
colorP = ['k', 'k', 'k']
marker = ['x', '.' , '+']
legend = ["INRIA", "Network Cameras"]	

plt.rcParams.update({'font.size': 20})

cost_HoG = [0,0,0,0,0,0,29.59,26.60,21.28]
cost_HoG_IN = [0,0,26.60,24.21,21.28,21.28,21.28,21.28,21.28]
missRate_HoG = [0.1,0.2,0.3,0.4,0.5,0.64,0.72,0.8,0.9] 

cost_FRCN = [0,0,532,532,532,532,532,532,532]
cost_FRCN_IN = [532,532,532,532,532,532,532,532,532]
missRate_FRCN = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

cost_ACF = [0,0,0,0,19.02,12.21,11.21,9.01,9.01]
cost_ACF_IN = [11.21,9.31,9.01,9.01,9.01,9.01,8.81,8.81,8.81]
missRate_ACF = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

n_groups = len(missRate_FRCN)
index = np.arange(1,n_groups+1)
bar_width = 0.4

plt.bar(index+bar_width,cost_HoG_IN,bar_width, color=colors[0])
plt.hold(True)
plt.bar(index+2*bar_width,cost_HoG,bar_width, color=colors[1])

plt.ylabel('Analysis Cost ($/hour)',fontsize=34)
plt.xlabel('Miss Rate',fontsize=34)
plt.tick_params(axis='x',labelsize=24)
plt.tick_params(axis='y',labelsize=24)
plt.xticks(index + 2*bar_width, missRate_FRCN)
plt.ylim((0,50))
plt.legend(legend, loc='upper center',ncol = 2,bbox_to_anchor=(0.5, 1.2))
plt.tight_layout()
imgfilename = "cost_HoG.pdf"
# Save the plot in a separate file
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()



plt.bar(index+bar_width,cost_FRCN_IN,bar_width, color=colors[0])
plt.hold(True)
plt.bar(index+2*bar_width,cost_FRCN,bar_width, color=colors[1])

plt.ylabel('Analysis Cost ($/hour)',fontsize=34)
plt.xlabel('Miss Rate',fontsize=34)
plt.tick_params(axis='x',labelsize=24)
plt.tick_params(axis='y',labelsize=24)
plt.xticks(index + 2*bar_width, missRate_FRCN)
#plt.ylim((0,120))
plt.legend(legend, loc='upper center',ncol = 2,bbox_to_anchor=(0.5, 1.2))
plt.tight_layout()
imgfilename = "cost_FRCN.pdf"
# Save the plot in a separate file
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()



plt.bar(index+bar_width,cost_ACF_IN,bar_width, color=colors[0])
plt.hold(True)
plt.bar(index+2*bar_width,cost_ACF,bar_width, color=colors[1])

plt.ylabel('Analysis Cost ($/hour)',fontsize=34)
plt.xlabel('Miss Rate',fontsize=34)
plt.tick_params(axis='x',labelsize=24)
plt.tick_params(axis='y',labelsize=24)
plt.xticks(index + 2*bar_width, missRate_FRCN)
plt.ylim((0,25))
plt.legend(legend, loc='upper center',ncol = 2,bbox_to_anchor=(0.5, 1.2))
plt.tight_layout()

imgfilename = "cost_ACF.pdf"

# Save the plot in a separate file
plt.savefig(imgfilename,bbox_inches='tight')
# Close the plot
plt.close()

