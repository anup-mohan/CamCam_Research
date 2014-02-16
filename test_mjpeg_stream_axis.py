'''This is a program to demostrate how to parse MJPEG streams from axis-cameras

The Format of MJPEG stream is:

--myboundary
Content-Type: image/jpeg
Content-Length: [size of image in bytes]
 [empty line]
  .....binary data.....
 [empth line]
--myboundary
Content-Type: image/jpeg
Content-Length: [size of image in bytes]
 [empty line]
  .....binary data.....
 [empty line]
.......
'''


import urllib
import sys

#ip of the target axis-camera"
#ip = "128.10.29.33"
ip = sys.argv[1]
name=sys.argv[2]

#desired frame rate
options = "?des_fps=1"

#the url of the MJPEG stream"
stream_mjpeg = urllib.urlopen("http://"+ip+"/axis-cgi/mjpg/video.cgi"+options)

#index for video frame
cnt = 0
#number of frame wanted
des_frame = 100

#while cnt < des_frame:
while cnt >= 0:
    #locate boundary
    if stream_mjpeg.readline().startswith("--myboundary"):
        #the second line is useless
        stream_mjpeg.readline()
        #get frame size
        img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
        #read in the empty line and binary image data
        data = stream_mjpeg.read(img_size+2)
        f = open(name+repr(cnt)+".jpg","wb")
        #empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
        f.write(data[2:])
        f.close()
        cnt += 1

stream_mjpeg.close()
            
