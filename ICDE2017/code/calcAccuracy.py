import sys
import peopledetect
from glob import glob
import itertools as it
import cv2
import re
import string
import xml.etree.ElementTree as ET


resfile = open(sys.argv[2],"w")
#GT_PATH = "/home/anupmohan/Documents/Research/camcam/CamCam_Research/BigData2016/ffserver/img_dataset_1_640_360/gt/"
GT_PATH = sys.argv[1]
dim = sys.argv[3]


list_mode = ["25%", "10%"]

def computeAccuracy(bbox_img, bbox_gt):

	# Number of people detected
	num_ppl = 0
	
	# Height of people detected
	height=[]
	true_pos_ht = []
	
	# Extract values from string
	
	# Remove the square brackets in the string
	#bbox_gt = str(bbox_gt).replace('[','').replace(']','')
	bbox_img = str(bbox_img).replace('[','').replace(']','')
	
	# Remove the parantheses in the string
	#bbox_gt = str(bbox_gt).replace('(','').replace(')','')
	bbox_img = str(bbox_img).replace('(','').replace(')','')
	
	#print bbox_gt
	#print bbox_img
	
	# Find total detections
	total_ppl_gt = len(bbox_gt) / 4 
	total_ppl_img = len(bbox_img.split(",")) / 4
	
	# Get height of people in GT
	index2 = 0
	for j in range(total_ppl_gt):
		y11 = int(bbox_gt[index2+1])
		y12 = int(bbox_gt[index2+3])
		height.append(abs(y12 - y11))
		index2 += 4
	
	# Get coordinates x1: will be GT and x2: will be image 
	index1 = 0
	for i in range(total_ppl_img):
	
		x21 = int(bbox_img.split(",")[index1])
		y21 = int(bbox_img.split(",")[index1+1])
		x22 = int(bbox_img.split(",")[index1+2])
		y22 = int(bbox_img.split(",")[index1+3])
		
		index2 = 0
		
		for j in range(total_ppl_gt):
		
			x11 = int(bbox_gt[index2])
			y11 = int(bbox_gt[index2+1])
			x12 = int(bbox_gt[index2+2])
			y12 = int(bbox_gt[index2+3])
			
			#print x11,y11,x12,y12,x21,y21,x22,y22
					
			# Calculate overlap area, overlap area should be >= 0.5 for detection		
			x_overlap = max(0,min(x12,x22) - max(x11,x21))
			y_overlap = max(0,min(y12,y22) - max(y11,y21))
			intersectionArea = x_overlap * y_overlap
			unionArea = (abs(x11 - x12) * abs(y11 - y12)) + (abs(x21 - x22) * abs(y21 - y22)) - intersectionArea
			overlapArea = float(intersectionArea)/float(unionArea)
			
			#print intersectionArea, unionArea
					
			if (overlapArea >= 0.5):
				num_ppl += 1
				true_pos_ht.append(abs(y12 - y11))
				#break
			
			index2 += 4
			
		
		index1 += 4
		
	# Get values to calculate precision and recall
	true_pos = num_ppl
	
	if (total_ppl_img > num_ppl):
		false_pos = total_ppl_img - num_ppl
	else:
		false_pos = 0

	if (total_ppl_gt > num_ppl):
		false_neg = total_ppl_gt - num_ppl
	else:
		false_neg = 0

	#print true_pos, false_pos, false_neg, total_ppl_gt, total_ppl_img
	return true_pos, false_pos, false_neg, total_ppl_gt, total_ppl_img, height, true_pos_ht
		

def get_bbox_xml(xml_fname):

	bbox = []
	root = ET.parse(xml_fname).getroot()
	for child in root:
		x1 = int(child[0].attrib['x'])        
		y1 = int(child[0].attrib['y'])
		x2 = x1 + int(child[0].attrib['width'])
		y2 = y1 + int(child[0].attrib['height'])
		bbox.append(x1)
		bbox.append(y1)
		bbox.append(x2)
		bbox.append(y2) 
	
	#print bbox
	return bbox

if __name__ == '__main__':

	for fn in it.chain(*map(glob, sys.argv[4:])):

		    #try:
		    	# Read the image
		        img = cv2.imread(fn)
		        
		        
		        if ((fn.split("_")[0].split("/")[-1] == "msee") or ((dim in list_mode) and (fn.split("_")[0].split("/")[-1] == "cam2"))):
		        	mode = "small"
		        else:
		        	mode = "large"
		        
		        print fn, mode
		        		        
		        # Get bounding box from analysis program (peopledetect.py)
		        bbox_img = peopledetect.detect_people(img,mode)
		        
		        # Read the ground truth data
		   	xml_fname = GT_PATH + fn.split(".")[0] + ".gt.xml"		        
		        bbox_gt = get_bbox_xml(xml_fname)
		        
		        # Skip if there are no people
		        if not bbox_gt:
		        	continue
      
		        
		        # Calculate precision and recall
		        true_pos, false_pos, false_neg, total_ppl_gt, total_ppl_img,height,true_pos_ht = computeAccuracy(bbox_img, bbox_gt)
		        #print true_pos, false_pos, false_neg, total_ppl_gt, total_ppl_img
		        
		        if (true_pos + false_pos == 0):
		        	precision = 0
		        else:
		        	precision = float(true_pos)/float(true_pos + false_pos)*100
		        
		        if (true_pos + false_neg == 0):
		        	recall = 0
		        else:
		        	recall = float(true_pos)/float(true_pos + false_neg)*100
		        	
				# Write the results		        
		        resfile.write("img:%s total_gt:%d, total_img:%d, tp:%d, fp:%d, fn:%d, precision:%f, recall:%f, ht:%s, trueht:%s"%(fn,total_ppl_gt, total_ppl_img,true_pos, false_pos, false_neg, precision,recall,height,true_pos_ht))
		        resfile.write("\n")

		        

resfile.close()	    
	            
