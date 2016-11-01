import sys
import xml.etree.ElementTree as ET
from glob import glob
import itertools as it

outfolder = sys.argv[1]

x_scale = float(sys.argv[2])
y_scale = float(sys.argv[3])

for fn in it.chain(*map(glob, sys.argv[4:])):

	# Create output xml file and write the header
	outfname = outfolder + fn
	outfile = open(outfname, "w")
	header = '<?xml version="1.0"?>\n<ObjectList>\n'
	outfile.write(header)
	
	root = ET.parse(fn).getroot()
	
	
	for child in root:
		# Scale the bounding box values
		x1 = int(float(child[0].attrib['x'])/x_scale)
		y1 = int(float(child[0].attrib['y'])/y_scale)
		width = int(float(child[0].attrib['width'])/x_scale)
		height = int(float(child[0].attrib['height'])/y_scale)
		
		outfile.write('\t\t<Object>\n' + '\t\t\t<Rect x="' + str(x1) + '"' +
                    ' y="' + str(y1) + '"' + ' width="' + str(width) + '"' +
                    ' height="' + str(height) + '"/>' +
                    '\n' + '\t\t</Object>\n')
        outfile.write('</ObjectList>')
            

outfile.close()
